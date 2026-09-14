# -*- coding: utf-8 -*-
"""deepskins CLI: 列出 / 安装 / 切换壁纸 —— 大肥鱼 & AI 全家桶皮肤。

用法:
  deepskins list                  # 列出全部皮肤
  deepskins url <id|repo>         # 打印仓库地址
  deepskins install <id|repo>     # 克隆到 ~/.deepskin-suits 并安装(生成+设置壁纸)
  deepskins wallpaper <id> [模式] # 直接切换某套的壁纸, 模式 grid|1..4|random|all
  deepskins sync                  # 克隆全部(不安装)
"""
import argparse
import json
import os
import subprocess
import sys
from importlib import resources

ROOT_DIR = os.path.join(os.path.expanduser("~"), ".deepskin-suits")


def prepare_console():
    """Windows GBK 控制台避免 Unicode 打印崩溃。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def load_catalog():
    text = resources.files("deepskins").joinpath("catalog.json").read_text(encoding="utf-8")
    return json.loads(text)


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
    if os.path.exists(os.path.join(dst, ".git")):
        print("[deepskins] %s 已存在, 拉取更新 ..." % repo)
        subprocess.check_call(["git", "-C", dst, "pull", "--ff-only"], stdout=subprocess.DEVNULL)
    else:
        print("[deepskins] 克隆 %s ..." % repo)
        subprocess.check_call(
            ["git", "clone", "--depth", "1",
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


def main(argv=None):
    prepare_console()
    ap = argparse.ArgumentParser(prog="deepskins", description="大肥鱼 & AI 全家桶 皮肤目录/安装器")
    sub = ap.add_subparsers(dest="cmd", required=True)
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
    sub.add_parser("sync", help="克隆全部皮肤(不安装)")
    args = ap.parse_args(argv)
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "url":
        return cmd_url(args)
    if args.cmd == "install":
        return cmd_install(args)
    if args.cmd == "wallpaper":
        return cmd_wallpaper(args)
    if args.cmd == "sync":
        return cmd_sync(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
