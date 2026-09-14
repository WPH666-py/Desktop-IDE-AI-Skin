# -*- coding: utf-8 -*-
"""setuptools 构建钩子: 打包前同步并校验皮肤目录, 避免发布包内是旧 catalog.json。

没有这个钩子时, 改了根目录 catalog.json 却忘记同步 deepskins/catalog.json,
发布出去的 pip 包就会缺少新增皮肤(CLI 报「未找到」)。
"""
import os
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _sync_catalog():
    import importlib.util

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "sync_catalog.py")
    spec = importlib.util.spec_from_file_location("_deepskins_sync_catalog", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.sync()
    if mod.check(strict=True) != 0:
        raise SystemExit("catalog.json 与 deepskins/catalog.json 不一致, 已中止构建")


class BuildPyWithCatalog(_build_py):
    def run(self):
        _sync_catalog()
        super().run()


def _sdist_files():
    """sdist 额外文件(真正的包含规则见 MANIFEST.in)。"""
    extra = ["catalog.json", "README.md", "LICENSE", "setup.py", "build_hooks.py"]
    return [f for f in extra if os.path.exists(os.path.join(ROOT, f))]


class SdistWithCatalog(_sdist):
    def run(self):
        _sync_catalog()
        super().run()


# setup.py 从这里取 cmdclass(pyproject.toml 的 [tool.setuptools.cmdclass]
# 只接受 python-qualified-identifier, 用 setup.py 注入更兼容)
cmdclass = {"build_py": BuildPyWithCatalog, "sdist": SdistWithCatalog}
