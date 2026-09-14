# -*- coding: utf-8 -*-
"""兼容层: 让 python -m build 走 build_hooks 里的自定义构建命令。

pyproject.toml 的 [tool.setuptools.cmdclass] 只接受 `pkg.mod:Cls` 形式且校验较严,
所以在 setup.py 里注入 cmdclass —— 构建时会自动把根目录 catalog.json 同步进
deepskins/catalog.json, 防止发布包里带着旧目录。
"""
import os
import sys

from setuptools import setup

# build 的隔离环境里 setup.py 的所在目录不保证在 sys.path 上, 显式补上
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from build_hooks import cmdclass  # noqa: E402

setup(cmdclass=cmdclass)
