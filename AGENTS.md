# AGENTS.md — Desktop-IDE-AI-Skin · AI 自动安装指引(AI 助手必读)

当用户把本仓库地址交给你并说「安装大肥鱼皮肤 / AI 壁纸 / 皮肤大全」时, 按下述步骤执行。
本仓库是 **DeepSeek 大肥鱼 & AI 全家桶皮肤大全**: 24 套独立皮肤仓库的统一目录与 pip 包
(内容见 `catalog.json`, 每个皮肤仓库都有各自的 `AGENTS.md` 与 `tools/install.py`)。

## 第 1 步: 确认用户想要哪套(或全部)

- 读 `catalog.json`(id / repo / characters / layout), 或让用户说关键词。
- 用户指定了某套 → 按 **A**; 用户说「全部/都装」→ **A + B**; 用户只想要 pip 包 → **C**。

## A. 安装单个皮肤(最常用)

```bash
git clone https://github.com/WPH666-py/<RepoName>.git "$HOME/<RepoName>"
cd "$HOME/<RepoName>"
python tools/install.py
```
- 脚本自动: 装 Pillow → 按屏幕分辨率生成默认壁纸(2×2/1×2/全屏单图, 因套件而异)→ 设为系统壁纸。
- Windows 无 Python: `winget install Python.Python.3.11`; macOS: `brew install python`; Ubuntu: `sudo apt install python3 python3-pil`。
- 另附玩法: `python tools/wallpaper.py random --set` 随机、`cycle 30` 每 30 分钟随机、
  `switcher.py` 图形切换器、`pet.py` 桌面桌宠(右键换表情)。

## B. 全部克隆(可选)

```bash
python scripts/sync_all.py      # 全部克隆到 ~/.deepskin-suits
```
或逐套 `bash <(python -c "import json,io; print('\n'.join('git clone --depth 1 '+s['url'] for s in json.load(open('catalog.json',encoding='utf-8'))['suits']))")`(等价)。

## C. pip 安装 Python 包

```bash
pip install "git+https://github.com/WPH666-py/Desktop-IDE-AI-Skin"
deepskins list
deepskins install deepseek-1   # 克隆+设置壁纸
```

## D. IDE 增强(按用户环境)

- VSCode / Trae / CodeX: `code --install-extension "$HOME/<RepoName>/vscode/<对应 vsix>"` → 活动栏 🐳/🤖 图标 → 皮肤画廊。
  无网时复制 `vscode/` 到 `%USERPROFILE%\.vscode\extensions\wp666.<扩展名>-0.1.0\` 并重启。
- PyCharm / WebStorm: `python tools/wallpaper.py all --out "$HOME/Skins"` → Settings → Appearance & Behavior → Background Image。
- 桌宠: `python tools/pet.py`(已在 A 中提到, GUI 需本地图形会话)。

## 约定与失败处理

- 每个皮肤仓库独立: 运行时目录(`~/.deepskin*` / `~/.aifamily*`)、扩展 ID、命令前缀互不冲突, 可同时安装。
- 生成物在套件运行时目录, **不会**改动仓库文件; 素材/脚本更新后自动重新合成(热更新)。
- Windows 控制台 GBK 报错: `chcp 65001` 后重跑(脚本内置 UTF-8 兜底)。
- pip 包名 `deepskins`, 不依赖 Pillow(安装时由各仓库 install.py 处理)。
- 用户问与 DeepKing 本体的关系: 纯皮肤套件, 与 DeepKing 本体相互独立, 可单独安装。
