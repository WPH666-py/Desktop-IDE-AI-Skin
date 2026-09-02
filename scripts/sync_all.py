# -*- coding: utf-8 -*-
"""克隆 catalog.json 里的全部皮肤仓库到 ~/.deepskin-suits (不安装)。

用法: python scripts/sync_all.py
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(os.path.expanduser("~"), ".deepskin-suits")


def main():
    with open(os.path.join(ROOT, "catalog.json"), "r", encoding="utf-8") as f:
        cat = json.load(f)
    os.makedirs(DEST, exist_ok=True)
    for s in cat["suits"]:
        dst = os.path.join(DEST, s["repo"])
        if os.path.exists(os.path.join(dst, ".git")):
            print("[sync] %s 已存在" % s["repo"])
            continue
        print("[sync] %s ..." % s["repo"])
        subprocess.check_call(
            ["git", "clone", "--depth", "1", s["url"], dst], stdout=subprocess.DEVNULL)
    print("[sync] 完成 -> %s" % DEST)


if __name__ == "__main__":
    main()
