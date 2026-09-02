# 安装说明(INSTALL)

## 方式〇: pip 安装(已发布到 PyPI 官方源, 最推荐)

```bash
pip install deepskins          # 已发布: https://pypi.org/project/deepskins/
deepskins list                 # 24 套一览
deepskins url deepseek-12      # 打印仓库地址
deepskins install aifamily-7   # 克隆到 ~/.deepskin-suits 并设置壁纸
deepskins sync                 # 克隆全部 24 套
```
备用: `pip install "git+https://github.com/WPH666-py/Desktop-IDE-AI-Skin"`

## 方式一: 给 AI 一句话(DeepKing / Claude Code / Kimi Code / CodeX / Trae / Harness / Cursor …)

把任一皮肤仓库链接发给 AI 并说「安装」, AI 读该仓库 `AGENTS.md` 自动完成全部步骤
(克隆 → Pillow → 生成壁纸并设置 → 按环境装 VS Code 扩展或引导 JetBrains → 可选桌宠)。

```text
请安装 https://github.com/WPH666-py/Deepseek-Skin-Suit12 的大肥鱼皮肤12
请安装 https://github.com/WPH666-py/AI-Family-Skin-Suit7 的 AI 全家桶皮肤7
```

## 方式二: pip 安装 `deepskins`(git 备用)

```bash
pip install "git+https://github.com/WPH666-py/Desktop-IDE-AI-Skin"

deepskins list                  # 24 套一览
deepskins url deepseek-12       # 打印仓库地址
deepskins install aifamily-7    # 克隆到 ~/.deepskin-suits 并设置壁纸
deepskins sync                  # 克隆全部 24 套
```

> PyPI 说明: `pyproject.toml` 已按发布规范写好。官方源(pypi.org)上传需要你自己的 PyPI 账号令牌,
> 后续只需: `python -m pip install build twine && python -m build && python -m twine upload dist/*`。

## 方式三: 手动(git)

```bash
git clone https://github.com/WPH666-py/<任意皮肤仓库>.git
cd <仓库>
python tools/install.py          # Windows 亦可直接双击 install.bat
```

## 每套皮肤通用玩法

```bash
python tools/wallpaper.py grid --set      # 默认壁纸(2x2 / 1x2 / 全屏单图 依套件)
python tools/wallpaper.py random --set    # 随机一张
python tools/wallpaper.py cycle 30        # 每 30 分钟自动随机(Ctrl+C 停止)
python tools/switcher.py                  # 可视化切换器
python tools/pet.py                       # 桌面桌宠(右键换表情, Esc 退出)
```

## VS Code / Trae / CodeX 扩展

```bash
code --install-extension vscode/deepskin-suit12-0.1.0.vsix      # DeepSeek 系列
code --install-extension vscode/ai-family-skin-suit7-0.1.0.vsix # AI 全家桶系列
```
装完: 活动栏出现 🐳(DeepSeek 系列)或 🤖(AI 全家桶系列)图标 → 皮肤画廊 → 点「设为壁纸」;
命令面板搜索 `大肥鱼N` / `AI全家桶N` 亦可。设置项 `deepskinN.repoPath` / `aifamilyN.repoPath`
指向仓库位置(默认 `%USERPROFILE%\DeepSkin-SuitN` / `AI-Family-Skin-SuitN`)。

## JetBrains(PyCharm / WebStorm / IntelliJ)

```bash
python tools/wallpaper.py all --out "$HOME/Skins"
```
Settings / Preferences → Appearance & Behavior → **Background Image** → `+` 选择生成的图片
(建议编辑器区用单图、欢迎页用 2×2/1×2 拼贴)。

## 依赖与兼容

- Python 3.9+(Pillow 缺失自动安装); 无 Python 时: Windows `winget install Python.Python.3.11`。
- 运行目录隔离: DeepSeek 系列 `~/.deepskin*`, AI 全家桶 `~/.aifamily*`;24 套可同时安装互不覆盖。
- 桌宠透明: Windows 原生支持; macOS/Linux 部分桌面不支持透明色会退化为白底卡片, 功能不受影响。

## 常见问题

- **壁纸尺寸**: 脚本默认取屏幕分辨率, 可 `--size 2560x1440` 自定义; 多显示器建议系统设为「跨屏/平铺」。
- **无网安装**: 素材内置在仓库内, 装过 Pillow 后离线可用。
- **素材更新**: 重新拉取仓库后运行任意 `--set` 命令即热更新(自动按素材/脚本修改时间重新合成)。
