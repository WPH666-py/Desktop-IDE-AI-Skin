# -*- coding: utf-8 -*-
"""把根目录 catalog.json 同步进 Python 包(deepskins/catalog.json)。

包内那份是"发布副本": pip 安装后 importlib.resources 读的是它,
所以每次改动根目录 catalog.json 后必须同步, 否则 CLI 看到的是旧目录。

用法:
  python scripts/sync_catalog.py           # 同步
  python scripts/sync_catalog.py --check   # 只校验是否一致(不一致 exit 1)
"""
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "catalog.json")
DST = os.path.join(ROOT, "deepskins", "catalog.json")


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def suits(path):
    try:
        return len(load(path)["suits"])
    except Exception:
        return None


def same():
    """两份目录是否等价(按解析后的 JSON 比较, 忽略空白差异)。"""
    if not os.path.exists(DST):
        return False
    try:
        return load(SRC) == load(DST)
    except Exception:
        return False


def sync():
    shutil.copyfile(SRC, DST)
    print("[catalog] %s -> %s (%s 套)" % (
        os.path.relpath(SRC, ROOT), os.path.relpath(DST, ROOT), suits(SRC)))


def check(strict=False):
    if same():
        print("[catalog] OK: 包内目录与根目录一致 (%s 套)" % suits(SRC))
        return 0
    print("[catalog] 不一致: 根 %s 套 / 包 %s 套" % (suits(SRC), suits(DST)), file=sys.stderr)
    print("[catalog] 请运行: python scripts/sync_catalog.py", file=sys.stderr)
    return 1 if strict else 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--check" in argv:
        return check(strict=True)
    sync()
    return check(strict=True)


if __name__ == "__main__":
    sys.exit(main())
