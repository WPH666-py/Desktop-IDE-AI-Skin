# -*- coding: utf-8 -*-
"""deepskins 回归测试 —— 重点盯「不管用户用哪个 Python 3, 装完都能跑」。

背景: 0.11.0 在 Python 3.8 上 pip 装得成功, 但第一条命令就崩:
    AttributeError: module 'importlib.resources' has no attribute 'files'
因为 `importlib.resources.files()` 是 3.9+ 的 API, 而声明的是 `requires-python >= 3.8`。
本套测试 + CI 版本矩阵(3.8~3.13 × 三平台)就是防止这类问题复发。

跑法:
    python -m unittest discover -s tests -t . -v
"""
import io
import json
import os
import re
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from deepskins import __version__, cli  # noqa: E402


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _pyproject():
    return _read(os.path.join(ROOT, "pyproject.toml"))


class TestMetadata(unittest.TestCase):
    """版本号与 Python 下界声明必须自洽 —— 发布到 PyPI 后改不动, 错了很难看。"""

    def test_pyproject_version_matches_package_version(self):
        m = re.search(r'^version\s*=\s*"([^"]+)"', _pyproject(), re.M)
        self.assertIsNotNone(m, "pyproject.toml 里找不到 version")
        self.assertEqual(
            m.group(1), __version__,
            "pyproject.toml 与 deepskins/__init__.py 的版本号不一致")

    def test_requires_python_floor_is_satisfied_by_this_interpreter(self):
        m = re.search(r'requires-python\s*=\s*">=\s*(\d+)\.(\d+)"', _pyproject())
        self.assertIsNotNone(m, "pyproject.toml 里找不到 requires-python")
        floor = (int(m.group(1)), int(m.group(2)))
        self.assertGreaterEqual(
            sys.version_info[:2], floor,
            "当前解释器 %s 低于声明的下界 %s" % (sys.version_info[:2], floor))

    def test_classifiers_cover_the_floor_to_313(self):
        text = _pyproject()
        for minor in range(8, 14):
            self.assertIn(
                '"Programming Language :: Python :: 3.%d"' % minor, text,
                "classifiers 缺少 3.%d, PyPI 页面会显示不支持" % minor)


class TestDocsAreVersionAgnostic(unittest.TestCase):
    """护栏: 文档里不许写死某个 Python 版本的安装路径。

    `%LOCALAPPDATA%\\Programs\\Python\\Python311\\Scripts` 这种写法只在
    「用户恰好也装的 3.11」时才成立 —— 换 3.12 / 3.13 / conda 的用户照着抄就找不到文件。
    正确的写法是从当前解释器推导: python -c "import sys,os;print(os.path.dirname(sys.executable))"
    """

    BAD = re.compile(r"Python3\d{1,2}")

    def test_no_hardcoded_python_version_path_in_docs(self):
        offenders = []
        for name in sorted(os.listdir(ROOT)):
            if not name.lower().endswith(".md"):
                continue
            path = os.path.join(ROOT, name)
            for lineno, line in enumerate(_read(path).splitlines(), 1):
                if self.BAD.search(line):
                    offenders.append("%s:%d: %s" % (name, lineno, line.strip()))
        docs = os.path.join(ROOT, "docs")
        if os.path.isdir(docs):
            for name in sorted(os.listdir(docs)):
                if name.lower().endswith(".md"):
                    path = os.path.join(docs, name)
                    for lineno, line in enumerate(_read(path).splitlines(), 1):
                        if self.BAD.search(line):
                            offenders.append("docs/%s:%d: %s" % (name, lineno, line.strip()))
        self.assertEqual(
            [], offenders,
            "文档里写死了 Python 版本路径(换个版本的用户会照抄失败):\n" + "\n".join(offenders))


class TestCatalogLoading(unittest.TestCase):
    """catalog.json 的读取是「任何 Python 3 都能跑」的关键路径。"""

    def test_load_catalog_returns_suits(self):
        cat = cli.load_catalog()
        self.assertIn("suits", cat)
        self.assertGreater(len(cat["suits"]), 0)
        self.assertIn("family", cat)

    def test_every_suit_has_required_fields(self):
        for s in cli.load_catalog()["suits"]:
            for field in ("id", "repo", "url", "characters", "layout"):
                self.assertIn(field, s, "皮肤 %s 缺少字段 %s" % (s.get("id"), field))

    def test_fallback_without_resources_files(self):
        """模拟 Python 3.8: 没有 importlib.resources.files 也要能读到目录。"""
        import importlib.resources as res

        saved = getattr(res, "files", None)
        try:
            if saved is not None:
                del res.files
            self.assertFalse(hasattr(res, "files"))
            text = cli.package_text("catalog.json")
        finally:
            if saved is not None:
                res.files = saved
        self.assertIn("suits", json.loads(text))

    def test_fallback_without_pkgutil(self):
        """再退一层: files() 没有、pkgutil 也拿不到时, 按文件路径直读兜底。"""
        import importlib.resources as res

        saved = getattr(res, "files", None)
        try:
            if saved is not None:
                del res.files
            with mock.patch("pkgutil.get_data", return_value=None):
                text = cli.package_text("catalog.json")
        finally:
            if saved is not None:
                res.files = saved
        self.assertIn("suits", json.loads(text))

    def test_all_strategies_read_the_same_bytes(self):
        text = cli.package_text("catalog.json")
        path = os.path.join(ROOT, "deepskins", "catalog.json")
        self.assertEqual(json.loads(text), json.loads(_read(path)))

    def test_root_and_packaged_catalog_are_in_sync(self):
        root = json.loads(_read(os.path.join(ROOT, "catalog.json")))
        packaged = json.loads(_read(os.path.join(ROOT, "deepskins", "catalog.json")))
        self.assertEqual(root, packaged, "跑 python scripts/sync_catalog.py 同步这两份")


class TestCli(unittest.TestCase):
    """CLI 的对外行为(测试只跑不联网的子命令)。"""

    def _run(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_list_prints_every_suit(self):
        code, out, _ = self._run(["list"])
        self.assertEqual(0, code)
        for s in cli.load_catalog()["suits"]:
            self.assertIn(s["id"], out)

    def test_no_args_prints_command_overview(self):
        code, out, _ = self._run([])
        self.assertEqual(0, code)
        for word in ("list", "install", "wallpaper", "doctor"):
            self.assertIn(word, out)

    def test_commands_alias(self):
        for name in ("commands", "help"):
            code, out, _ = self._run([name])
            self.assertEqual(0, code)
            self.assertIn("deepskins", out)

    def test_version_flag(self):
        out = io.StringIO()
        with redirect_stdout(out):
            with self.assertRaises(SystemExit) as ctx:
                cli.main(["--version"])
        self.assertEqual(0, ctx.exception.code)
        self.assertIn(__version__, out.getvalue())

    def test_unknown_command_exits_nonzero(self):
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                cli.main(["nope"])
        self.assertNotEqual(0, ctx.exception.code)

    def test_missing_arg_exits_nonzero(self):
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                cli.main(["url"])
        self.assertNotEqual(0, ctx.exception.code)

    def test_url_unknown_key_reports_error(self):
        code, _out, err = self._run(["url", "根本没有这套皮肤"])
        self.assertEqual(1, code)
        self.assertIn("未找到", err)

    def test_find_suit_by_id_repo_and_character(self):
        cat = cli.load_catalog()
        first = cat["suits"][0]
        for key in (first["id"], first["repo"], first["repo"].lower() + ".git"):
            found = cli.find_suit(cat, key)
            self.assertIsNotNone(found, "找不到 %s" % key)
            self.assertEqual(first["id"], found["id"])

    def test_find_suit_unknown_returns_none(self):
        self.assertIsNone(cli.find_suit(cli.load_catalog(), "不存在的皮肤xyz"))


class TestProxyModule(unittest.TestCase):
    """代理模块要能在无网络、无注册表的环境下安全导入与降级。

    注意：这里一律 mock 掉 `proxy.detect()`。真去探测会依赖**跑测试的这台机器**
    （本机开着 Clash 就有代理、CI runner 上就没有），断言会随机红 ——
    实测踩过：CI 全矩阵 18 个任务因为这一条挂掉。
    """

    def test_normalize(self):
        from deepskins import proxy

        self.assertEqual("http://127.0.0.1:7897", proxy._normalize("127.0.0.1:7897"))
        self.assertEqual("http://a:1", proxy._normalize("  http://a:1/  "))
        self.assertIsNone(proxy._normalize(""))
        self.assertIsNone(proxy._normalize("   "))

    def test_env_with_proxy_injects_detected_proxy(self):
        from deepskins import proxy

        base = {"PATH": "x"}
        with mock.patch.object(proxy, "detect", return_value=("http://127.0.0.1:7897", "测试")):
            env = proxy.env_with_proxy(base)
        self.assertEqual("x", env["PATH"])
        self.assertEqual("http://127.0.0.1:7897", env["HTTP_PROXY"])
        self.assertEqual("http://127.0.0.1:7897", env["HTTPS_PROXY"])
        self.assertNotIn("HTTP_PROXY", base, "不应改动传进来的 dict")

    def test_env_with_proxy_without_proxy(self):
        """没探测到代理时不该凭空塞代理变量（无网 / CI 环境就是这种）。"""
        from deepskins import proxy

        with mock.patch.object(proxy, "detect", return_value=(None, "未探测到")):
            env = proxy.env_with_proxy({"PATH": "x"})
        self.assertEqual("x", env["PATH"])
        self.assertNotIn("HTTP_PROXY", env)

    def test_pip_and_git_args_without_proxy(self):
        from deepskins import proxy

        with mock.patch.object(proxy, "detect", return_value=(None, "未探测到")):
            self.assertEqual([], proxy.pip_args())
            # 没代理时不应因 git 是否安装而炸
            self.assertEqual([], proxy.git_config_args())

    def test_detect_respects_off_switch(self):
        """DEEPSKINS_NO_PROXY=1 时探测必须返回 None（用户显式关掉）。"""
        from deepskins import proxy

        with mock.patch.dict(os.environ, {"DEEPSKINS_NO_PROXY": "1"}):
            url, source = proxy.detect(force=True)
        self.assertIsNone(url)
        self.assertIn("DEEPSKINS_NO_PROXY", source)


if __name__ == "__main__":
    unittest.main()
