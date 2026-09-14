# -*- coding: utf-8 -*-
"""deepskins.wallpaper —— 让 pip 包直接切换某套皮肤的壁纸。

皮肤仓库本身的合成逻辑在各自 `tools/skin_core.py` 里, 这里只是:
  1. 找到(必要时克隆)皮肤仓库;
  2. 动态加载它的 `skin_core`(不污染 sys.path、不按固定名字缓存);
  3. 合成目标模式并设为系统壁纸。

依赖 Pillow(由皮肤仓库的 install.py 或本包运行时自动补装)。
"""
import os
import subprocess
import sys
import uuid

ROOT_DIR = os.path.join(os.path.expanduser("~"), ".deepskin-suits")
GITHUB = "https://github.com/WPH666-py/%s.git"

# 素材张数未知时的单图候选(不同套件 1x2 是 2 张、2x2 是 4 张)
_SINGLE_FALLBACK = ["single1", "single2", "single3", "single4"]


def suit_dir(repo):
    return os.path.join(ROOT_DIR, repo)


def ensure_suit(repo, clone=True):
    """返回皮肤仓库目录; 缺失时克隆(--depth 1)。"""
    dst = suit_dir(repo)
    if os.path.exists(os.path.join(dst, "tools", "skin_core.py")):
        return dst
    if os.path.exists(os.path.join(dst, ".git")):
        subprocess.check_call(["git", "-C", dst, "pull", "--ff-only"],
                              stdout=subprocess.DEVNULL)
        return dst
    if not clone:
        return None
    os.makedirs(ROOT_DIR, exist_ok=True)
    subprocess.check_call(["git", "clone", "--depth", "1", GITHUB % repo, dst],
                          stdout=subprocess.DEVNULL)
    return dst


def load_skin_core(suit_path):
    """按路径加载该套件的 skin_core 模块(唯一模块名, 避免跨套件串味)。"""
    import importlib.util

    path = os.path.join(suit_path, "tools", "skin_core.py")
    if not os.path.exists(path):
        raise ImportError("缺少 %s" % path)
    name = "_deepskins_%s" % uuid.uuid4().hex[:8]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return mod


def list_modes(repo):
    """返回 [(模式键, 说明), ...]; 拿不到 skin_core 时给通用候选。"""
    try:
        sc = load_skin_core(ensure_suit(repo))
        return list(sc.MODES)
    except Exception:
        return [("grid", "拼贴壁纸(默认)")] + [
            (k, "单图 %s" % k[-1]) for k in _SINGLE_FALLBACK
        ]


def _modes_of(sc):
    try:
        return [k for k, _label in sc.MODES]
    except Exception:
        return None


def normalize_mode(mode):
    """把 CLI 简写转成套件内部模式名: "1" -> "single1"。"""
    mode = str(mode).strip()
    if mode.isdigit():
        return "single%s" % mode
    return mode


def apply_mode(repo, mode="random", size=None):
    """合成并设为系统壁纸, 返回壁纸文件路径。"""
    sc = load_skin_core(ensure_suit(repo))
    mode = normalize_mode(mode)
    if mode in ("", "random"):
        import random
        mode = random.choice(_modes_of(sc) or ["grid"] + _SINGLE_FALLBACK)
    try:
        out = sc.build(mode, size)
    except ValueError:
        keys = _modes_of(sc) or []
        raise SystemExit("该套件没有模式 %r, 可用: %s" % (mode, " | ".join(keys) or "grid"))
    sc.set_wallpaper(out)
    return out


def export_all(repo, out_dir=None, size=None):
    """导出该套件全部模式到目录(给 PyCharm 等手动设背景图用), 返回文件列表。"""
    sc = load_skin_core(ensure_suit(repo))
    out_dir = os.path.abspath(out_dir or os.path.join(ROOT_DIR, repo, "wallpapers"))
    os.makedirs(out_dir, exist_ok=True)
    made = []
    for key, _label in sc.MODES:
        img = sc.compose(key, size)
        path = os.path.join(out_dir, "%s.jpg" % key)
        img.save(path, quality=92)
        made.append(path)
    return made


def ensure_pillow():
    """确保 Pillow 可用, 缺失时自动 pip 安装(与各皮肤仓库 install.py 行为一致)。"""
    try:
        import PIL  # noqa: F401
        return True
    except ImportError:
        pass
    print("[deepskins] 未检测到 Pillow, 正在自动安装 ...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "pillow"])
    except subprocess.CalledProcessError:
        return False
    return True


def main(argv=None):
    """允许 `python -m deepskins.wallpaper <id|repo> [模式]`。"""
    import argparse

    from .cli import find_suit, load_catalog, prepare_console

    prepare_console()
    ap = argparse.ArgumentParser(prog="deepskins.wallpaper", description="切换/导出皮肤壁纸")
    ap.add_argument("key", help="皮肤 id 或仓库名, 如 deepseek-15")
    ap.add_argument("mode", nargs="?", default="random",
                    help="grid | 1 | 2 | 3 | 4 | random | all")
    ap.add_argument("--list", dest="list_modes", action="store_true", help="列出可用模式")
    ap.add_argument("--out", default=None, help="all 模式的导出目录")
    ap.add_argument("--size", default=None, help="尺寸, 如 1920x1080")
    args = ap.parse_args(argv)

    s = find_suit(load_catalog(), args.key)
    if not s:
        print("未找到 %r, 用 deepskins list 查看全部" % args.key, file=sys.stderr)
        return 1
    repo = s["repo"]

    if args.list_modes:
        for key, label in list_modes(repo):
            print("    %-8s %s" % (key, label))
        return 0

    if not ensure_pillow():
        print("[deepskins] Pillow 安装失败, 请手动 pip install pillow", file=sys.stderr)
        return 1

    size = None
    if args.size:
        try:
            w, h = args.size.lower().split("x")
            size = (int(w), int(h))
        except ValueError:
            print("尺寸格式应为 1920x1080", file=sys.stderr)
            return 1

    if args.mode == "all":
        made = export_all(repo, args.out, size)
        print("[deepskins] %s 导出 %d 张:" % (s["id"], len(made)))
        for p in made:
            print("  ✓ %s" % p)
        return 0

    out = apply_mode(repo, args.mode, size)
    print("[deepskins] 已切换壁纸: %s -> %s" % (s["id"], out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
