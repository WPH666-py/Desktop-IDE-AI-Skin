# AGENTS.md — Desktop-IDE-AI-Skin · AI 自动安装指引(AI 助手必读)

当用户把本仓库地址交给你并说「安装大肥鱼皮肤 / AI 壁纸 / 皮肤大全」时, 按下述步骤执行。
本仓库是 **DeepSeek 大肥鱼 & AI 全家桶皮肤大全**: 32 套独立皮肤仓库的统一目录与 pip 包
(内容见 `catalog.json`, 每个皮肤仓库都有各自的 `AGENTS.md` 与 `tools/install.py`)。

## 第 1 步: 确认用户想要哪套(或全部)

- 读 `catalog.json`(id / repo / characters / layout), 或让用户说关键词。
- 用户指定了某套 → 按 **A**; 用户说「全部/都装」→ **A + B**; 用户只想要 pip 包 → **C**。

## A. 安装单个皮肤(最常用)

> **调用格式统一**：Windows 用 `py -3`，macOS / Linux 用 `python3`。
> 这些是仓库里的**脚本文件**，所以用 `py -3 <脚本>`（不是 `-m`）。

```bash
git clone https://github.com/WPH666-py/<RepoName>.git "$HOME/<RepoName>"
cd "$HOME/<RepoName>"
py -3 tools/install.py
```
- 脚本自动: 装 Pillow → 按屏幕分辨率生成默认壁纸(2×2/1×2/全屏单图, 因套件而异)→ 设为系统壁纸。
- 没有 Python 时: Windows `winget install Python.Python.3.12`（3.8~3.13 任一版本都行）;
  macOS `brew install python`; Ubuntu `sudo apt install python3 python3-pil`。
- 另附玩法: `py -3 tools/wallpaper.py random --set` 随机、`cycle 30` 每 30 分钟随机、
  `switcher.py` 图形切换器、`pet.py` 桌面桌宠(右键换表情)。
- 用户说"壁纸被任务栏/桌面图标挡住"时: 各套件已默认 `--anchor top`(底部留白); 可再调
  `py -3 tools/wallpaper.py grid --anchor top --pad-bottom 15`(百分数), 或 `--anchor center` 回旧行为。



## B. 全部克隆(可选)

```bash
py -3 scripts/sync_all.py      # 全部克隆到 ~/.deepskin-suits
```


或逐套 `bash <(python -c "import json,io; print('\n'.join('git clone --depth 1 '+s['url'] for s in json.load(open('catalog.json',encoding='utf-8'))['suits']))")`(等价)。

## C. pip 安装 Python 包

**统一调用格式：Windows 一律 `py -3 -m`，macOS / Linux 一律 `python3 -m`。**

```powershell
py -3 -m pip install deepskins                                               # 已发布 PyPI(推荐)
py -3 -m pip install "git+https://github.com/WPH666-py/Desktop-IDE-AI-Skin"  # 备用
py -3 -m deepskins list                       # 列出全部 32 套
py -3 -m deepskins install deepseek-1         # 克隆+设置壁纸
py -3 -m deepskins wallpaper deepseek-1 1     # 切换某套壁纸(简写 1/2/3..; 加 --list 看模式)
py -3 -m deepskins doctor                     # 体检: 代理 / 网络 / git / Pillow
py -3 -m deepskins mirror                     # 国内镜像装包命令
```

**为什么非要这个形式**：它不依赖 pip 的 `Scripts` 目录在不在 `PATH` 里。
用户报「无法将 deepskins 项识别为 cmdlet / 不是内部或外部命令」时，让他改用上面的写法即可 ——
**不要**再教他配 PATH，**绝不要**照着 `...\Programs\Python\Python3<版本>\Scripts`
这类**写死版本**的路径去配：那只在用户恰好也是那个版本时才成立。

`py -3` 挑的是本机**版本最高**的 Python，未必是装了包的那个（症状：`No module named deepskins`）。
先 `py -0p` 列出全部版本，再用 `py -3 -m pip show deepskins` 确认当前这个里有没有；
必要时指定版本，例如 `py -3.12 -m deepskins list`。

支持 Python **3.8 ~ 3.13**（CI 三平台 × 六版本逐个装 wheel 再真跑一次）。



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
