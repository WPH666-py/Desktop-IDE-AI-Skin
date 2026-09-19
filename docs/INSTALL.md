# 安装说明(INSTALL)

## 方式〇: pip 安装(已发布到 PyPI 官方源, 最推荐)

```bash
pip install deepskins          # 已发布: https://pypi.org/project/deepskins/
deepskins list                 # 32 套一览
deepskins doctor               # 体检: 代理探测 / 网络 / git / Pillow
deepskins url deepseek-12      # 打印仓库地址
deepskins install aifamily-7   # 克隆到 ~/.deepskin-suits 并设置壁纸
deepskins wallpaper deepseek-22 1   # 直接切换第 22 套的第 1 张壁纸
deepskins sync                 # 克隆全部 32 套
```
备用: `pip install "git+https://github.com/WPH666-py/Desktop-IDE-AI-Skin"`

### 装完敲 `deepskins` 说「找不到命令」?（任何 Python 版本都适用）

`pip` 装完通常会打印一句警告: `...\Scripts' which is not on PATH`。此时直接敲
`deepskins` 会报 `无法将"deepskins"项识别为 cmdlet…`(Windows)或 `command not found`
(macOS / Linux)。**这不是安装失败** —— 先确认包在不在:

```bash
pip show deepskins        # 能显示版本就说明装好了
```

然后三选一。注意下面**没有写死任何 Python 版本号** —— 网上抄来的那种
`...\Programs\Python\Python3<版本号>\Scripts` 路径, 只有当你恰好也装的正是那个版本时才成立:

```bash
# ① 最稳: 用模块方式调用。用「你装包的那个 python」跑, 3.8~3.13 都对
python -m deepskins list
py -3 -m deepskins list          # Windows 装了 py 启动器时
python3 -m deepskins list        # macOS / Linux
```

```bash
# ② 打印你这个 python 的 Scripts 目录(exe 就在里面), 再拿完整路径直接调
python -c "import sys,os;print(os.path.dirname(sys.executable))"
```

```powershell
# ③ 把它永久加进用户 PATH(之后重开终端, deepskins 就能直接敲)
$s = python -c "import sys,os;print(os.path.dirname(sys.executable))"
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$s", "User")
```

> ⚠️ **装了多个 Python 时最容易踩的坑**: `py -3` 永远挑**版本最高**的那个, 而你未必是
> 往那个里面装的包 —— 于是报 `No module named deepskins`。
> 先 `py -0p` 列出本机全部 Python 及其路径, 再用 `python -m pip show deepskins` 确认
> 「当前这个 python 里到底有没有」。**记住一条: 用哪个 python 装的, 就用哪个 python 跑。**

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

deepskins list                  # 32 套一览
deepskins url deepseek-12       # 打印仓库地址
deepskins install aifamily-7    # 克隆到 ~/.deepskin-suits 并设置壁纸
deepskins wallpaper deepseek-22 # 直接切换第 22 套的壁纸(不带模式=随机)
deepskins wallpaper deepseek-15 3   # 切到第 3 张单图(简写 1/2/3/4)
deepskins wallpaper deepseek-15 --list   # 看这套有哪些模式
deepskins sync                  # 克隆全部 32 套
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

- **Python 3.8 ~ 3.13 全部支持**（CI 里 3 个平台 × 6 个版本逐个装 wheel 再真跑一次）。
  无 Python 时: Windows `winget install Python.Python.3.12`（任意 ≥3.8 的版本都行）、
  macOS `brew install python`、Ubuntu `sudo apt install python3 python3-pil`。
- 不确定自己是哪个版本: `python -V`; Windows 装了多个时 `py -0p` 列出全部。
- Pillow 缺失时 `install` / `wallpaper` 会自动 pip 安装。
- 运行目录隔离: DeepSeek 系列 `~/.deepskin*`, AI 全家桶 `~/.aifamily*`;32 套可同时安装互不覆盖。
- 桌宠透明: Windows 原生支持; macOS/Linux 部分桌面不支持透明色会退化为白底卡片, 功能不受影响。

## 常见问题

- **壁纸尺寸**: 脚本默认取屏幕分辨率, 可 `--size 2560x1440` 自定义; 多显示器建议系统设为「跨屏/平铺」。
- **无网安装**: 素材内置在仓库内, 装过 Pillow 后离线可用。
- **素材更新**: 重新拉取仓库后运行任意 `--set` 命令即热更新(自动按素材/脚本修改时间重新合成)。

## 装不上 / SSL 报错怎么办

典型症状: `pip install deepskins` 报 `SSL: UNEXPECTED_EOF_WHILE_READING` 或
`Read timed out (pypi.org:443)`。

**还有一种更迷惑人的**: 报
`ProxyError('Cannot connect to proxy.', FileNotFoundError(2, 'No such file or directory'))`，
重试 5 次后以 `Could not find a version that satisfies the requirement deepskins
(from versions: none)` 收尾 —— 看起来像"包不存在"，其实是**代理**问题:

- Windows 的 `ProxyServer` 如果只有 `host:port`（没有 `http=...;https=...` 协议列表），
  urllib 会把 https 代理拼成 `https://host:port`，pip 于是连不上；
- 但浏览器/`Invoke-WebRequest` 用的是另一套逻辑，所以"网页能开、pip 装不上"。
- 解法: 显式给 pip 一个 `http://` 代理
  ```powershell
  $env:HTTP_PROXY='http://localhost:7897'; $env:HTTPS_PROXY='http://localhost:7897'
  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple deepskins
  ```
  （端口以你的代理软件为准；`deepskins doctor` 会探测注册表里的系统代理。）

原因通常是**桌面代理软件只设了 Windows 系统代理**:

| 通道 | 读代理的方式 | 结果 |
|---|---|---|
| git | 读 Windows 系统代理(注册表) | 能用 → 克隆皮肤仓库正常 |
| pip / requests | **只读 `HTTP_PROXY` / `HTTPS_PROXY` 环境变量** | 读不到 → 直连 pypi.org, 在受限网络下就断 |

诊断与三条出路:

```bash
deepskins doctor        # 已装好时: 直接看代理探测结果与各站点 HTTPS 实测
```

1. **用国内镜像装**(最省事, 三个源任选; 都是 PyPI 只读镜像, 自动同步):
   ```bash
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple deepskins   # 清华 TUNA
   pip install -i https://mirrors.ustc.edu.cn/pypi/simple deepskins    # 中科大 USTC
   pip install -i https://mirrors.aliyun.com/pypi/simple deepskins     # 阿里云
   ```
   不想记这些地址: `deepskins mirror` 会把三条命令和「怎么确认镜像同步了」一起打出来;
   `deepskins doctor` 会**实测**哪个源连得通, 直接给可用的那条。
2. **给 pip 设一次环境变量**(之后 pip 自己就走代理了):
   ```powershell
   setx HTTPS_PROXY http://127.0.0.1:7897
   setx HTTP_PROXY  http://127.0.0.1:7897
   ```
   (端口以你的代理软件为准; 重新开一个终端生效)
3. **临时单次使用**:
   ```bash
   pip install --proxy http://127.0.0.1:7897 deepskins
   ```

> 包内已内置代理自动探测: `deepskins install/wallpaper` 在调用 **git 克隆** 和
> **pip 装 Pillow** 时会自动带上探测到的代理(顺序: 环境变量 → Windows 注册表 →
> 本机常见端口)。用户 git 已自配代理时不覆盖。
> 关闭: `DEEPSKINS_NO_PROXY=1`; 手动指定: `DEEPSKINS_PROXY=http://host:port`。

## 壁纸被任务栏/桌面图标挡住怎么办

2×2 拼贴和"完整卡片"单图默认**垂直居中**: 2×2 整块约占屏高 91%, 卡片底边离屏底约 43px,
所以在任务栏较厚或图标排到下方的桌面上, 底部内容会被压住(壁纸本身没有缩放裁切,
纯粹是位置偏下)。

各套件已内置**垂直锚点**, 默认 `top`(把内容放进安全区, 底部留白):

```bash
python tools/wallpaper.py grid --anchor top      # 默认: 底部留白(2×2 约 120px)
python tools/wallpaper.py grid --anchor center   # 回到旧的居中(会压到任务栏)
python tools/wallpaper.py grid --pad-bottom 20   # 自定义底部预留(百分数或 0~1 小数)
```

也可用环境变量: `DEEPSKIN_GRID_ANCHOR=top|center|bottom`、`DEEPSKIN_GRID_PAD_BOTTOM=11`(百分数)。

> 1536×960 实测: 2×2 修前 y=14..946(压住任务栏) → 修后 y=14..840(留 120px);
> 完整卡片修前 y=43..917(留 43px) → 修后 y=43..812(留 148px)。
> 屏幕很矮时会自动回退居中, 避免格子被压得过小。
