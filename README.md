# 🐳 Desktop · IDE · AI Skin — 大肥鱼 & AI 全家桶 皮肤大全

**DeepSeek 蓝色大肥鱼** ×14 套 + **AI 全家桶**(GPT / Claude / GLM / Kimi / DeepSeek / 千问 / MiniMax / Grok)×10 套
主题皮肤的统一目录与安装器。所有皮肤: 素材内置、离线可用、跨平台(Windows / macOS / Linux)、
支持 **DeepKing / VSCode / Harness / CodeX / Trae / PyCharm / Claude Code / Kimi Code** 等环境与**桌面桌宠**,
24 套彼此独立、可同时安装、各自切换。

## 🚀 三种安装方式

### ① 给任意 AI 一句话(推荐)
把**任一皮肤仓库**或本仓库链接发给 AI(DeepKing / Claude Code / Kimi Code / CodeX / Trae / Harness / Cursor 等),
AI 会读取该仓库的 `AGENTS.md` 自动完成: 克隆 → 装 Pillow → 生成壁纸并设置 → 按环境装 IDE 扩展 → 可选桌宠。

```text
请安装 https://github.com/WPH666-py/Deepseek-Skin-Suit1 的大肥鱼皮肤1
```

### ② pip 安装 Python 包 `deepskins`
```bash
pip install "git+https://github.com/WPH666-py/Desktop-IDE-AI-Skin"
deepskins list                 # 列出全部 24 套
deepskins install deepseek-1   # 克隆并安装(自动生成+设置壁纸)
deepskins url aifamily-7       # 打印仓库地址
deepskins sync                 # 克隆全部
```
> 本包完全符合 PyPI 规范(pyproject.toml)。由于需要你的 PyPI 账号凭据才能发布到官方源,
> 默认走 `git+` 安装; 之后你可用 `python -m build && python -m twine upload dist/*` 一键上传。

### ③ 手动
```bash
git clone <任一皮肤仓库> && cd <仓库>
python tools/install.py        # 生成壁纸并设置桌面(Windows 也可双击 install.bat)
```

## 📚 皮肤目录

### DeepSeek 蓝色大肥鱼(14 套)

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
catalog.json      30 套皮肤机器可读目录
deepskins/        Python 包(deepskins CLI): list / install / url / sync
scripts/          sync_all.py: 克隆全部皮肤
docs/INSTALL.md   完整安装说明(含 VS Code 扩展、JetBrains、常见问题)
AGENTS.md         AI 自动安装指引(AI 助手必读)
```

## 🙏 素材

各家 AI 拟人插画, 作者标识见各素材水印 (BEAR-177 等)。仅用于个人桌面美化, 请勿二次商用。
