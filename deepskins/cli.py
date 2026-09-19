# -*- coding: utf-8 -*-
"""deepskins CLI: 列出 / 安装 / 切换壁纸 —— 大肥鱼 & AI 全家桶皮肤。

用法:
  deepskins                       # 不带参数 = 打印命令总览
  deepskins list                  # 列出全部皮肤
  deepskins url <id|repo>         # 打印仓库地址
  deepskins install <id|repo>     # 克隆到 ~/.deepskin-suits 并安装(生成+设置壁纸)
  deepskins wallpaper <id> [模式] # 直接切换某套的壁纸, 模式 grid|1..4|random|all
  deepskins doctor                # 体检: 代理探测 / 网络 / git / Python / Pillow
  deepskins mirror                # 国内镜像(清华/中科大/阿里)装包命令
  deepskins sync                  # 克隆全部(不安装)
  deepskins --version             # 看版本

兼容性: 支持 Python 3.8 ~ 3.13(3.8 上不使用 3.9+ 才有的 API, 见 package_text)。
"""
import argparse
import json
import os
import subprocess
import sys

from . import __version__, proxy

ROOT_DIR = os.path.join(os.path.expanduser("~"), ".deepskin-suits")

_PKG = __package__ or "deepskins"

# 国内 PyPI 镜像 —— 与 genshen-desktop-skin 的 mirror.py 用同一套地址。
# 都是 pypi.org 的只读镜像：自动同步、不能上传，发版只能发 PyPI 再等收录。
MIRRORS = (
    ("清华 TUNA", "https://pypi.tuna.tsinghua.edu.cn/simple"),
    ("中科大 USTC", "https://mirrors.ustc.edu.cn/pypi/simple"),
    ("阿里云", "https://mirrors.aliyun.com/pypi/simple"),
)


def prepare_console():
    """Windows GBK 控制台避免 Unicode 打印崩溃。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def package_text(name):
    """读取包内文本资源 —— 兼容**全部 Python 3**(3.8 / 3.9 / … / 3.13 实测)。

    为什么不能直接用 `importlib.resources.files()`: 它是 **Python 3.9+** 的 API,
    而本包声明 `requires-python = ">=3.8"`。3.8 上它会在**第一条命令**就抛
    `AttributeError: module 'importlib.resources' has no attribute 'files'` ——
    用户看到的现象是「pip 明明装成功了, 一敲 deepskins 就崩」。

    三级回退, 任意 Python 3 都能拿到 catalog.json:
      1. `importlib.resources.files()` —— 3.9+ 的现代写法(3.13 仍推荐);
      2. `pkgutil.get_data()`         —— 3.0+ 通用, 对 zip 导入同样有效;
      3. 按文件路径直读                —— 兜底(解包安装一定有这个文件)。
    """
    try:
        from importlib import resources

        files = getattr(resources, "files", None)  # 3.9+; 3.8 上为 None
        if files is not None:
            return files(_PKG).joinpath(name).read_text(encoding="utf-8")
    except Exception:
        pass

    try:
        import pkgutil

        data = pkgutil.get_data(_PKG, name)
        if data is not None:
            return data.decode("utf-8")
    except Exception:
        pass

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_catalog():
    return json.loads(package_text("catalog.json"))


def find_suit(catalog, key):
    key = key.lower()
    for s in catalog["suits"]:
        if key in (s["id"].lower(), s["repo"].lower(), s["repo"].lower() + ".git"):
            return s
    for s in catalog["suits"]:
        if key in s["characters"].lower() or key in s["repo"].lower():
            return s
    return None


def cmd_list(args):
    cat = load_catalog()
    print("# %s" % cat["family"])
    print()
    for s in cat["suits"]:
        print("%-12s %-25s %-6s %s" % (s["id"], s["repo"], s["layout"], s["characters"]))
    return 0


def cmd_url(args):
    s = find_suit(load_catalog(), args.key)
    if not s:
        print("未找到 %r, 用 deepskins list 查看全部" % args.key, file=sys.stderr)
        return 1
    print(s["url"])
    return 0


def _clone(repo):
    os.makedirs(ROOT_DIR, exist_ok=True)
    dst = os.path.join(ROOT_DIR, repo)
    # 自动带上探测到的代理(用户 git 已自配代理时不覆盖)
    px = proxy.git_config_args()
    if os.path.exists(os.path.join(dst, ".git")):
        print("[deepskins] %s 已存在, 拉取更新 ..." % repo)
        subprocess.check_call(["git"] + px + ["-C", dst, "pull", "--ff-only"],
                              stdout=subprocess.DEVNULL)
    else:
        print("[deepskins] 克隆 %s ..." % repo)
        subprocess.check_call(
            ["git"] + px + ["clone", "--depth", "1",
                            "https://github.com/WPH666-py/%s.git" % repo, dst],
            stdout=subprocess.DEVNULL)
    return dst


def cmd_install(args):
    s = find_suit(load_catalog(), args.key)
    if not s:
        print("未找到 %r, 用 deepskins list 查看全部" % args.key, file=sys.stderr)
        return 1
    dst = _clone(s["repo"])
    print("[deepskins] 运行安装脚本 (%s) ..." % s["repo"])
    subprocess.check_call([sys.executable, os.path.join(dst, "tools", "install.py")], cwd=dst)
    print("[deepskins] 完成! 打开切换器: python %s" % os.path.join(dst, "tools", "switcher.py"))
    print("[deepskins] 启动桌宠:   python %s" % os.path.join(dst, "tools", "pet.py"))
    return 0


def cmd_sync(args):
    for s in load_catalog()["suits"]:
        _clone(s["repo"])
    print("[deepskins] 全部克隆到 %s" % ROOT_DIR)
    return 0


def cmd_wallpaper(args):
    """直接切换某套皮肤的壁纸, 无需用户自己找仓库/脚本。

    优先本地合成(Pillow 可用时), 否则调用该仓库的 tools/wallpaper.py。
    """
    s = find_suit(load_catalog(), args.key)
    if not s:
        print("未找到 %r, 用 deepskins list 查看全部" % args.key, file=sys.stderr)
        return 1
    try:
        from .wallpaper import apply_mode, list_modes
        if args.list_modes:
            print("[deepskins] %s (%s) 可用模式:" % (s["id"], s["repo"]))
            for key, label in list_modes(s["repo"]):
                short = key[6:] if key.startswith("single") and key[6:].isdigit() else key
                print("    %-8s %s   (简写: %s)" % (key, label, short))
            return 0
        out = apply_mode(s["repo"], args.mode)
        print("[deepskins] 已切换壁纸: %s -> %s" % (s["id"], out))
        return 0
    except ImportError:
        pass  # 没装 Pillow: 退回调用仓库自带脚本
    dst = _clone(s["repo"])
    script = os.path.join(dst, "tools", "wallpaper.py")
    if not os.path.exists(script):
        print("[deepskins] %s 缺少 tools/wallpaper.py" % s["repo"], file=sys.stderr)
        return 1
    print("[deepskins] 调用 %s" % script)
    from .wallpaper import normalize_mode
    return subprocess.call([sys.executable, script, normalize_mode(args.mode), "--set"], cwd=dst)


def cmd_doctor(args):
    """体检: 代理探测 / 网络可达性 / git / Python / Pillow。

    专治这一类问题: 桌面代理软件只设了 Windows 系统代理, git 能用而 pip 不能用,
    于是 pip 直连 pypi.org 报 SSL UNEXPECTED_EOF / Read timed out。
    """
    import platform
    import socket

    print("# deepskins 体检")
    print()
    print("Python      : %s (%s)" % (platform.python_version(), sys.executable))
    print("系统        : %s %s" % (platform.system(), platform.release()))

    # ---- git ----
    try:
        gv = subprocess.run(["git", "--version"], stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, timeout=10, text=True).stdout.strip()
        print("git         : %s" % (gv or "可用"))
        gp = subprocess.run(["git", "config", "--global", "--get", "http.proxy"],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            timeout=10, text=True).stdout.strip()
        print("git 代理    : %s" % (gp or "(未配置, 将走系统代理或自动探测)"))
    except Exception as e:
        print("git         : 不可用 (%s)" % e)

    # ---- Pillow ----
    try:
        import PIL  # noqa: F401
        print("Pillow      : 已安装")
    except ImportError:
        print("Pillow      : 未安装 (install/wallpaper 时会自动 pip 装)")

    # ---- 代理探测 ----
    print()
    print("— 代理 —")
    url, source = proxy.detect(force=True)
    if url:
        print("探测结果    : %s" % url)
        print("来源        : %s" % source)
    else:
        print("探测结果    : 未探测到代理 (%s)" % (source or "无"))
    print("说明        : pip/requests 只认 HTTP_PROXY/HTTPS_PROXY 环境变量,")
    print("              不读 Windows 系统代理; 本工具会把探测到的代理显式传给 git/pip。")
    print("关闭探测    : 设 DEEPSKINS_NO_PROXY=1   手动指定: DEEPSKINS_PROXY=http://host:port")

    # ---- 网络可达性 ----
    # 注意: 必须真做一次 HTTPS 请求(TCP 能连 != TLS 能握手)。
    # 有些网络会对特定域名在 TLS 握手阶段断开 —— 只测端口会误报"可连"。
    print()
    print("— 网络(HTTPS 实测) —")

    def _https_ok(url, timeout=10):
        import ssl
        import urllib.request
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": "deepskins-doctor"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return True, "HTTP %d" % r.status
        except Exception as e:
            msg = type(e).__name__
            reason = getattr(e, "reason", None)
            if isinstance(reason, ssl.SSLError):
                msg = "TLS 握手失败(%s)" % reason.__class__.__name__
            elif reason is not None:
                msg = str(reason)[:48]
            else:
                msg = str(e)[:48]
            return False, msg

    targets = [
        ("GitHub(克隆皮肤仓库)", "https://github.com"),
        ("PyPI 官方源(pip 装包)", "https://pypi.org/simple/"),
        ("PyPI CDN(下载包体)", "https://files.pythonhosted.org/"),
    ] + [("%s 镜像" % name, index + "/") for name, index in MIRRORS]
    results = {}
    for label, url in targets:
        ok, note = _https_ok(url)
        results[label] = ok
        print("  %-26s %-42s %s" % (label, note, "✅" if ok else "❌"))

    # ---- 结论 ----
    print()
    working = [(n, i) for n, i in MIRRORS if results.get("%s 镜像" % n)]
    if results.get("PyPI 官方源(pip 装包)"):
        print("结论: pypi.org 正常, `pip install deepskins` 可直接用。")
        if working:
            print("      国内网络想更快, 或用任一可用镜像:")
            for name, index in working:
                print("      pip install -i %s deepskins   # %s" % (index, name))
    elif working:
        print("结论: pypi.org 连不上(TLS 被中断), 但以下镜像可用 —— 任选一条装包:")
        for name, index in working:
            print("  pip install -i %s deepskins   # %s" % (index, name))
        print("  (已装好之后, 本包的 git/pip 调用会自动带上探测到的代理)")
    else:
        print("结论: pypi.org 与国内镜像都连不上, 请检查网络或代理设置。")
    return 0


def cmd_mirror(args):
    """打印可用的 PyPI 镜像与对应装包命令(国内网络用)。"""
    print("# deepskins %s —— PyPI 镜像" % __version__)
    print()
    print("国内装包(任选一条, 通常比直连 pypi.org 快很多):")
    for name, index in MIRRORS:
        print("  pip install -i %s deepskins   # %s" % (index, name))
    print()
    print("官方源:")
    print("  pip install deepskins")
    print()
    print("说明: 国内源都是 PyPI 的**只读镜像**, 自动从 pypi.org 同步; 作者只能发到 PyPI,")
    print("      镜像随后收录(通常几分钟内)。可打开下面的地址确认新版本是否已同步:")
    for name, index in MIRRORS:
        print("  %-50s %s" % (index + "/deepskins/", name))
    print()
    print("实测哪个源连得通: deepskins doctor")
    return 0


def print_overview():
    """不带任何参数时打印命令总览(与 genshen-skin 的行为保持一致)。"""
    print("# deepskins %s —— 大肥鱼 & AI 全家桶 皮肤大全" % __version__)
    print()
    print("看目录")
    print("  deepskins list                     列出全部皮肤")
    print("  deepskins url <id|仓库名>          打印该套的仓库地址")
    print()
    print("装 / 换")
    print("  deepskins install <id|仓库名>      克隆并安装(生成+设置壁纸)")
    print("  deepskins wallpaper <id> [模式]    只换壁纸: grid | 1 | 2 | 3 | 4 | random | all")
    print("  deepskins wallpaper <id> --list    看这套有哪些模式")
    print("  deepskins sync                     克隆全部(不安装)")
    print()
    print("诊断")
    print("  deepskins doctor                   体检: 代理探测 / 网络 / git / Pillow")
    print("  deepskins mirror                   国内镜像(清华 / 中科大 / 阿里)装包命令")
    print("  deepskins --version                看当前版本")
    print()
    print("例: deepskins list   →   deepskins install deepseek-1   →   deepskins wallpaper deepseek-1 2")


def main(argv=None):
    prepare_console()
    ap = argparse.ArgumentParser(
        prog="deepskins",
        description="大肥鱼 & AI 全家桶 皮肤目录/安装器(不带参数运行 = 看命令总览)")
    ap.add_argument("--version", action="version", version="deepskins %s" % __version__)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("list", help="列出全部皮肤")
    p = sub.add_parser("url", help="打印仓库地址")
    p.add_argument("key")
    p = sub.add_parser("install", help="克隆并安装指定皮肤(需 git)")
    p.add_argument("key")
    p = sub.add_parser("wallpaper", help="直接切换指定皮肤的壁纸")
    p.add_argument("key")
    p.add_argument("mode", nargs="?", default="random",
                   help="grid | 1 | 2 | 3 | 4 | random | all (默认 random)")
    p.add_argument("--list", dest="list_modes", action="store_true", help="只列出可用模式")
    sub.add_parser("doctor", help="体检: 代理探测 / 网络 / git / Pillow")
    sub.add_parser("mirror", help="PyPI 国内镜像与装包命令")
    sub.add_parser("sync", help="克隆全部皮肤(不安装)")
    sub.add_parser("commands", aliases=["help"], help="打印命令总览")
    args = ap.parse_args(argv)
    if not args.cmd:
        print_overview()
        return 0
    if args.cmd in ("commands", "help"):
        print_overview()
        return 0
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "url":
        return cmd_url(args)
    if args.cmd == "install":
        return cmd_install(args)
    if args.cmd == "wallpaper":
        return cmd_wallpaper(args)
    if args.cmd == "doctor":
        return cmd_doctor(args)
    if args.cmd == "mirror":
        return cmd_mirror(args)
    if args.cmd == "sync":
        return cmd_sync(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
