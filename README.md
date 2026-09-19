# 🐳 Desktop · IDE · AI Skin — 大肥鱼 & AI 全家桶 皮肤大全

**DeepSeek 蓝色大肥鱼** ×22 套 + **AI 全家桶**(GPT / Claude / GLM / Kimi / DeepSeek / 千问 / MiniMax / Grok)×10 套
主题皮肤的统一目录与安装器。所有皮肤: 素材内置、离线可用、跨平台(Windows / macOS / Linux)、
壁纸随时可切换(2×2 拼贴 / 单图 / 随机 / 定时轮换),
支持 **DeepKing / VSCode / Harness / CodeX / Trae / PyCharm / Claude Code / Kimi Code** 等环境与**桌面桌宠**,
32 套彼此独立、可同时安装、各自切换。

## 🚀 三种安装方式

### ① 给任意 AI 一句话(推荐)
把**任一皮肤仓库**或本仓库链接发给 AI(DeepKing / Claude Code / Kimi Code / CodeX / Trae / Harness / Cursor 等),
AI 会读取该仓库的 `AGENTS.md` 自动完成: 克隆 → 装 Pillow → 生成壁纸并设置 → 按环境装 IDE 扩展 → 可选桌宠。

```text
请安装 https://github.com/WPH666-py/Deepseek-Skin-Suit1 的大肥鱼皮肤1
```

### ② pip 安装(已发布 PyPI 官方源)
```bash
py -3 -m pip install deepskins          # https://pypi.org/project/deepskins/
py -3 -m deepskins                      # 不带参数 = 命令总览
py -3 -m deepskins list                 # 列出全部 32 套
py -3 -m deepskins install deepseek-1   # 克隆并安装(自动生成+设置壁纸)
py -3 -m deepskins wallpaper deepseek-22        # 直接换第 22 套的壁纸(默认随机)
py -3 -m deepskins wallpaper deepseek-22 1      # 切到第 1 张单图; 加 --list 看全部模式
py -3 -m deepskins doctor               # 体检: 代理探测 / 网络 / git / Pillow
py -3 -m deepskins mirror               # 国内镜像(清华 / 中科大 / 阿里)装包命令
py -3 -m deepskins url aifamily-7       # 打印仓库地址
py -3 -m deepskins sync                 # 克隆全部
py -3 -m deepskins --version            # 看版本
```
> **兼容性: Python 3.8 ~ 3.13 全部支持**（CI 里 3 平台 × 6 版本逐个装 wheel 真跑）。
> **统一用 `py -3 -m` 调用**：不依赖 pip 的 `Scripts` 目录在不在 `PATH`，也不用管你装的是哪个 Python 版本。
> **macOS / Linux 把 `py -3` 换成 `python3`**，其余完全一样；装了多个 Python 时先 `py -0p` —— `py -3` 挑的是**版本最高**的那个。
>
> 本包完全符合 PyPI 规范(pyproject.toml)。由于需要你的 PyPI 账号凭据才能发布到官方源,
> 默认走 `py -3 -m pip install "git+..."` 安装; 之后你可用 `py -3 -m build && py -3 -m twine upload dist/*` 一键上传。
> `py -3 -m deepskins wallpaper <id> [模式]` 会自动找到(必要时克隆)对应皮肤仓库、合成并设为系统壁纸,
> 不用自己进仓库找脚本。

### ③ 手动
```bash
git clone <任一皮肤仓库> && cd <仓库>
py -3 tools/install.py         # 生成壁纸并设置桌面(Windows 也可双击 install.bat)
```

## 📚 皮肤目录

### DeepSeek 蓝色大肥鱼(22 套)

| 仓库 | 主题 | 样式 |
|---|---|---|
| [Deepseek-Skin-Suit1](https://github.com/WPH666-py/Deepseek-Skin-Suit1) | 摸摸头/亲亲/深睡/太棒了 | 紧凑式 2×2 |
| [Deepseek-Skin-Suit2](https://github.com/WPH666-py/Deepseek-Skin-Suit2) | 有点饿了/大的药来了/压力一只鱼/万字文言文 | 2×2 |
| [Deepseek-Skin-Suit3](https://github.com/WPH666-py/Deepseek-Skin-Suit3) | 喜欢偷懒/就吃一碗/没吃饱喵/算token哦 | 2×2 |
| [Deepseek-Skin-Suit4](https://github.com/WPH666-py/Deepseek-Skin-Suit4) | 终于上当了/爆了爆了/瞎编应付下/用户怒了 | 2×2 |
| [Deepseek-Skin-Suit5](https://github.com/WPH666-py/Deepseek-Skin-Suit5) | 先养着吧/暂时没啥用/先赶走吧/赶都赶不走 | 2×2 |
| [Deepseek-Skin-Suit6](https://github.com/WPH666-py/Deepseek-Skin-Suit6) | 快夸我喵/摸摸头/完蛋了/开摆 | 2×2 |
| [Deepseek-Skin-Suit7](https://github.com/WPH666-py/Deepseek-Skin-Suit7) | 不要再蹬了/违反AI指令/守护着你/有资源吗 | 2×2 |
| [Deepseek-Skin-Suit8](https://github.com/WPH666-py/Deepseek-Skin-Suit8) | 一锅炖不下/我是大肥鱼/吃白饭Token/吃饱饱 | 2×2 |
| [Deepseek-Skin-Suit9](https://github.com/WPH666-py/Deepseek-Skin-Suit9) | 一脚踢飞/乖乖坐好 | 1×2 竖版 |
| [Deepseek-Skin-Suit10](https://github.com/WPH666-py/Deepseek-Skin-Suit10) | 杂鱼杂鱼?/我会一直陪着你 | 1×2 |
| [Deepseek-Skin-Suit11](https://github.com/WPH666-py/Deepseek-Skin-Suit11) | 数据在脑子里/彻底怒了/大胆想法/大赢鲸 | 2×2 |
| [Deepseek-Skin-Suit12](https://github.com/WPH666-py/Deepseek-Skin-Suit12) | 漂浮在蓝海水面(宽幅) | 全屏/卡片单图 |
| [Deepseek-Skin-Suit13](https://github.com/WPH666-py/Deepseek-Skin-Suit13) | 黑裙礼装/蓝发女仆 | 1×2 |
| [Deepseek-Skin-Suit14](https://github.com/WPH666-py/Deepseek-Skin-Suit14) | 你愿意和我…吗/我不知道耶/就骚了/好模型 | 2×2 |
| [Deepseek-Skin-Suit15](https://github.com/WPH666-py/Deepseek-Skin-Suit15) | 你愿意和我…吗?/DSH? DeepSeek Hentai?/大烧货吗?/正在思考… | 2×2 |
| [Deepseek-Skin-Suit16](https://github.com/WPH666-py/Deepseek-Skin-Suit16) | 别再蹬了啦!/你已经有我了…/求你们不要再嘲笑了/已思考13秒: 穷光蛋 | 2×2 |
| [Deepseek-Skin-Suit17](https://github.com/WPH666-py/Deepseek-Skin-Suit17) | 大胆孝/偷偷孝/跳脸孝/嘴硬孝(单张四格) | 单张(完整卡片 / 全屏铺满) |
| [Deepseek-Skin-Suit18](https://github.com/WPH666-py/Deepseek-Skin-Suit18) | 誓死捍卫深度求索/摸鱼/别再蹬了啦!/缓存必中 | 2×2 |
| [Deepseek-Skin-Suit19](https://github.com/WPH666-py/Deepseek-Skin-Suit19) | 特别充值通道 1鲸子=1tonken(单张) | 单张(完整卡片 / 全屏铺满) |
| [Deepseek-Skin-Suit20](https://github.com/WPH666-py/Deepseek-Skin-Suit20) | 苗寨灯火·银饰鲸鱼娘(16:9 宽幅单张) | 单张(全屏铺满 / 卡片) |
| [Deepseek-Skin-Suit21](https://github.com/WPH666-py/Deepseek-Skin-Suit21) | 银杏银饰·青羽(16:9 宽幅单张) | 单张(全屏铺满 / 卡片) |
| [Deepseek-Skin-Suit22](https://github.com/WPH666-py/Deepseek-Skin-Suit22) | 苗寨鼓楼·青羽执扇(16:9 宽幅单张) | 单张(全屏铺满 / 卡片) |

### AI 全家桶(10 套, GPT / Claude / GLM / Kimi / DeepSeek / 千问 / MiniMax / Grok)

| 仓库 | 角色 | 样式 |
|---|---|---|
| [AI-Family-Skin-Suit1](https://github.com/WPH666-py/AI-Family-Skin-Suit1) | 用不起就别用/劣等模型/想看色图?早说嘛!/别急别急了 | 2×2 |
| [AI-Family-Skin-Suit2](https://github.com/WPH666-py/AI-Family-Skin-Suit2) | GPT/Claude/GLM/DeepSeek 四格对比卡 | 单图 |
| [AI-Family-Skin-Suit3](https://github.com/WPH666-py/AI-Family-Skin-Suit3) | 白龙娘(GPT)/橙发书娘(Claude) | 1×2 |
| [AI-Family-Skin-Suit4](https://github.com/WPH666-py/AI-Family-Skin-Suit4) | 蓝发女仆(DeepSeek)/折扇娘(千问) | 1×2 |
| [AI-Family-Skin-Suit5](https://github.com/WPH666-py/AI-Family-Skin-Suit5) | 黑裙书娘(GLM)/月弧虹音娘(Kimi) | 1×2 |
| [AI-Family-Skin-Suit6](https://github.com/WPH666-py/AI-Family-Skin-Suit6) | 粉橙导演娘(MiniMax)/暗黑双斧娘(Grok) | 1×2 |
| [AI-Family-Skin-Suit7](https://github.com/WPH666-py/AI-Family-Skin-Suit7) | Claude 咖啡娘(暖阳) | 全屏/卡片单图 |
| [AI-Family-Skin-Suit8](https://github.com/WPH666-py/AI-Family-Skin-Suit8) | Kimi 月夜吹笛娘(星空) | 全屏/卡片单图 |
| [AI-Family-Skin-Suit9](https://github.com/WPH666-py/AI-Family-Skin-Suit9) | GLM 图书馆猫娘(暖光) | 全屏/卡片单图 |
| [AI-Family-Skin-Suit10](https://github.com/WPH666-py/AI-Family-Skin-Suit10) | 千问 竹窗折扇娘(青花) | 全屏/卡片单图 |

> 完整机器可读目录: [catalog.json](catalog.json)(含运行时目录、VS Code 扩展 ID、vsix 路径)。

## 🧩 IDE 支持

| 环境 | 方式 |
|---|---|
| VSCode / Trae / CodeX | 克隆后 `code --install-extension vscode/<ext>.vsix` → 活动栏 🐳/🤖 → 皮肤画廊一键换壁纸 |
| PyCharm / WebStorm / IntelliJ | `python tools/wallpaper.py all` 生成素材 → Settings → Background Image |
| DeepKing / Claude Code / Kimi Code / CodeX / Trae / Harness 等 AI | 发仓库链接, AI 按 [AGENTS.md](AGENTS.md) 自动安装 |
| 桌面桌宠 | `python tools/pet.py`(透明置顶、右键换表情、可拖动) |

## 📁 仓库结构

```
catalog.json      32 套皮肤机器可读目录
deepskins/        Python 包(deepskins CLI): list / install / url / wallpaper / sync
scripts/          sync_all.py: 克隆全部皮肤
docs/INSTALL.md   完整安装说明(含 VS Code 扩展、JetBrains、常见问题)
AGENTS.md         AI 自动安装指引(AI 助手必读)
```

## 🙏 素材

各家 AI 拟人插画, 作者标识见各素材水印 (BEAR-177 等)。仅用于个人桌面美化, 请勿二次商用。
