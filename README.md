# sciplotting · 顶刊科研绘图 Agent Skill
全场景科研绘图技能包，符合 [Agent Skills 开放标准](https://agentskills.io/home)，支持 Nature / Science / Cell / PNAS / Lancet / NEJM 等顶刊投稿规范，完整覆盖 6 大类科研配图，原生兼容 Claude Code、Codex、Cursor、Goose、VS Code 等所有主流 AI 编程工具与 Coding Agent。

---

## ✨ 核心特性
- 🎨 **顶刊标准色板库**：结构化内置 Nature 官方推荐色板、Okabe-Ito 色板、Science/Cell/NEJM 经典色板，全程色盲友好、灰度可打印。
- 📐 **自动适配期刊版面**：一键精准匹配 10+ 顶级期刊的单栏（85-89 mm）、1.5 栏（120-136 mm）、双栏（174-180 mm）尺寸与分辨率要求。
- 🧩 **六大类配图全覆盖**：定量统计、高通量组学、实验成像表征、机制原理模型、技术流程方案、结构装置图全场景支持。
- ✅ **自动化合规校验引擎**：一键仿真红色盲、绿色盲、蓝黄色盲，自动化审计 CIE 相对明度、色差矩阵与禁用色板。
- 🔄 **跨工具风格统一**：Python / TikZ / Mermaid 深度联动，共用同一套色值体系与视觉设计语言。
- 📦 **开箱即用零配置**：单行命令安装到所有兼容 Agent，无需任何繁琐的初始化配置。

---

## 📦 一键安装

### 前置依赖
- **Node.js ≥ 22.20**（用于运行 `skills` CLI 安装工具）
- **Python ≥ 3.9**（运行绘图脚本可选；Agent 调用规范无需 Python 环境）
- 可选依赖库：`pip install matplotlib numpy pandas scipy pillow`

### 1. 从 GitHub 远程直接安装（推荐）
无需先手动克隆代码仓库，直接在终端中执行即可全局安装到所有已识别的兼容 Agent：
```bash
npx skills add axjing/sciplotting -g --all
```

参数说明：
- `axjing/sciplotting`：GitHub 仓库地址（支持完整 URL `https://github.com/axjing/sciplotting`）
- `-g`：全局安装，所有项目与对话会话均可调用
- `--all`：自动识别并安装到所有兼容的 Agent 工具

### 2. 安装到指定的 Agent
仅将技能安装到你当前日常使用的指定编程工具：
```bash
# 示例：仅安装到 Claude Code + Codex + Cursor
npx skills add axjing/sciplotting -g -a claude-code codex cursor
```

支持的主流 Agent 清单：
Claude Code、Anthropic Codex、Cursor、Goose、VS Code、OpenCode、Letta、Gemini CLI、GitHub Copilot 等 70+ 工具。

### 3. Windows 兼容说明
Windows 系统下若因权限限制无法创建符号链接（symlink），可添加 `--copy` 参数切换为文件复制模式：
```bash
npx skills add axjing/sciplotting -g --all --copy
```

### 4. 本地源码安装（适用于二次开发/离线使用）
```bash
git clone https://github.com/axjing/sciplotting.git
cd sciplotting
npx skills add . -g --all
```

### 5. 验证安装与卸载
```bash
# 查看全局已安装技能
npx skills list -g

# 更新技能到最新版本
npx skills update sciplotting -g

# 卸载技能
npx skills remove sciplotting -g
```

---

## 🚀 核心功能快速上手

### 1. 多子图主图联合拼版 (Figure 1 复合大图)
解决 Nature / Science 投稿时各小图字体失调与轴对不齐的顽疾：
```bash
python scripts/python/compose_figure.py \
  --journal nature-double \
  --output Fig1_master_composite.pdf
```

### 2. 临床生存分析曲线 (Kaplan-Meier + 风险人群表)
带有时间对齐的 Number at Risk 表、95% 置信区间与 Log-rank 检验：
```bash
python scripts/python/plot_survival.py \
  --journal nature-single \
  --output Fig2_survival.pdf
```

### 3. Meta 分析与风险比森林图 (Forest Plot)
严谨呈现 RCT 效应量、逆方差样本权重与底部合并效应棱形 (Diamond)：
```bash
python scripts/python/plot_forest.py \
  --journal nature-single \
  --output Fig3_forest.pdf
```

### 4. AI 标杆与计算标度律 (Scaling Laws / Pareto Frontier)
绘制计算量 vs 测试损失的双对数标度律与帕累托前沿图：
```bash
python scripts/python/plot_benchmark.py \
  --type scaling \
  --output Fig4_scaling.pdf
```

### 5. 定量统计图 (均值柱 + SEM + 离散样本散点叠加)
```bash
python scripts/python/plot_stats.py \
  --type bar \
  --journal nature-single \
  --palette nature_main_5 \
  --output Fig5_bar.pdf
```

### 6. 高通量组学差异火山图 (带防重叠引线标注)
```bash
python scripts/python/plot_omics.py \
  --type volcano \
  --journal nature-single \
  --output Fig6_volcano.pdf
```

### 7. 纯 Python 矢量机制图 (零 LaTeX 依赖)
```bash
python scripts/python/draw_diagram.py \
  --template pathway \
  --journal nature-double \
  --output Fig7_pathway.pdf
```

### 8. R / ggplot2 顶刊主题使用 (生信与单细胞推荐)
```r
source("scripts/r/global_style.R")

# 自动注入 Arial 7pt 无衬线轴线与 Nature 5 色板
p <- ggplot(df, aes(x = Group, y = Value, fill = Group)) +
  geom_bar(stat = "identity", width = 0.55) +
  scale_fill_nature("nature_main_5") +
  theme_nature(base_size = 7)

# 自动匹配 Nature 单栏 89 mm 宽度高保真导出
save_journal_figure(p, "Fig8_R_nature.pdf", journal = "nature-single")
```

### 9. 视觉自愈质检与色盲无障碍审计
```bash
# 像素级边缘裁剪、截断与动态对比度核查
python scripts/python/verify_render.py Fig1_master_composite.png --journal nature-double

# 色盲仿真与 Delta E 色差矩阵审计
python scripts/python/check_palette.py --palette nature_main_5 --format markdown
```

---

## 📁 技能包目录结构

```
sciplotting/
├── SKILL.md                    # 【主控】Agent 执行入口：元数据、5步工作流、多模态自愈闭环
├── README.md                   # 【人类使用说明】安装、上手、参数速查、FAQ
├── assets/
│   └── palettes.json           # 结构化色值库：分类/连续/分歧/荧光/强调色全场景
├── references/
│   ├── journal_specs.md        # 顶刊投稿硬规范：尺寸/分辨率/字体/文件格式
│   ├── figure_types.md         # 八类配图定义、适用场景与最佳实践
│   ├── diagram_specs.md        # 流程/机制/装置图的排版符号与布局规范
│   ├── compliance_checklist.md # 投稿前 7 维度合规校验清单
│   └── palette_guide.md        # 色板选型决策树 + 色盲友好灰度适配说明
├── scripts/
│   ├── python/
│   │   ├── global_style.py     # 顶刊风格全局配置（统一字体/线宽/色板/毫米转换）
│   │   ├── compose_figure.py   # 【多子图拼版】主图联合编排器 (GridSpec, a-d 标号)
│   │   ├── plot_stats.py       # 定量统计图生成器（柱/箱/线/散点+误差棒+显著性）
│   │   ├── plot_survival.py    # 【临床图】Kaplan-Meier 生存分析曲线与风险人群表
│   │   ├── plot_forest.py      # 【临床图】Meta 分析与风险比 (HR/RR) 森林图
│   │   ├── plot_benchmark.py   # 【AI/前沿】帕累托最优、标度律与多维雷达图
│   │   ├── plot_omics.py       # 组学图生成器（热图/火山图/PCA/富集气泡图）
│   │   ├── draw_diagram.py     # 矢量示意图生成器（流程/通路/微流控芯片）
│   │   ├── check_palette.py    # 配色合规校验（色盲模拟/灰度对比度/感知均匀性）
│   │   └── verify_render.py    # 【视觉质检】像素级边缘截断与自愈反馈诊断器
│   ├── r/
│   │   ├── global_style.R      # R / ggplot2 顶刊主题与色板注入引擎
│   │   └── demo_plot.R         # R 语言标准绘图与导出脚本示例
│   ├── tikz/
│   │   ├── linear_workflow.tex     # 线性技术路线图模板 (已过 pdflatex 编译)
│   │   ├── parallel_workflow.tex   # 并行多模块实验流程图模板 (已过 pdflatex 编译)
│   │   ├── signaling_pathway.tex   # 信号通路/分子机制图模板 (已过 pdflatex 编译)
│   │   └── apparatus_schematic.tex # 实验装置/结构示意图模板 (已过 pdflatex 编译)
│   └── mermaid/
│       └── diagram_templates.md    # 轻量级流程图模板（生信/CONSORT/机制回路）
├── tests/
│   └── test_sciplotting.py     # 全场景自动化回归测试套件 (12 组用例全部通过)
└── .github/
    └── workflows/
        └── ci.yml              # GitHub Actions 跨平台 (Ubuntu/Windows) CI 流水线
```

---

## 🛠️ 常用参数速查

### 期刊版面预设 (`--journal`)
| 选项 | 适用出版物 | 单栏宽度 | 双栏宽度 |
| :--- | :--- | :--- | :--- |
| `nature-single` / `nature-double` | Nature, Nature Communications, Nature Methods | 89 mm | 180 mm |
| `science-single` / `science-double` | Science, Science Advances, Science Immunology | 55 mm | 178 mm |
| `cell-single` / `cell-double` | Cell, Cancer Cell, Immunity, Molecular Cell | 85 mm | 174 mm |
| `pnas-single` / `pnas-double` | PNAS (Proc. Natl. Acad. Sci. U.S.A.) | 86 mm | 178 mm |
| `lancet-single` / `lancet-double` | The Lancet 系列期刊 | 85 mm | 175 mm |
| `nejm-single` / `nejm-double` | New England Journal of Medicine | 86 mm | 178 mm |

### 内置色板预设 (`--palette`)
- **离散分类色**：`nature_main_5`（Nature 低饱和 5 色）、`okabe_ito_8`（色盲绝对友好 8 色）、`science_classic_6`、`cell_press_6`、`nejm_classic_5`
- **连续数值色**：`viridis`（感知均匀）、`plasma`（高对比）、`cividis`（全色盲无障碍优化）
- **双极分歧色**：`RdBu`（经典差异上调红/下调蓝）、`PRGn`（色盲友好紫/绿差异）
- **显微多通道**：`dual_channel`（绿 + 品红）、`triple_channel`（青 + 品红 + 黄）

---

## ❓ 常见问题 (FAQ)

**Q：安装后 Agent 提示找不到技能？**  
A：请确认技能文件夹名与 `SKILL.md` 中 `name` 字段完全一致（均为 `sciplotting`）；并尝试重启 Coding Agent 重新加载技能缓存。

**Q：没有安装 LaTeX/TeXLive 环境，能使用示意图与流程图功能吗？**  
A：完全可以！运行纯 Python 脚本 `scripts/python/draw_diagram.py` 即可直接生成同等专业度的矢量 PDF/SVG 示意图，零额外环境依赖。

**Q：导出的 PDF 字体在不同操作系统中打开会发生跑版或缺失吗？**  
A：不会。`global_style.py` 严格配置了 `pdf.fonttype = 42`（TrueType 字体完全嵌入），保证跨 Mac、Windows、Linux 与出版商排版系统打开时 100% 字体保真。

**Q：可以直接输入我自己的 CSV 数据文件进行绘图吗？**  
A：可以。通过 `--data your_data.csv` 参数传入即可；缺省该参数时脚本会自动生成具有标准学术特征的模拟数据方便调试。

**Q：可以用于商业项目或专利申请配图吗？**  
A：完全可以。本技能代码与色板规范遵循开放学术协议，所用色板均为国际学术界公开标准，可自由用于学术论文、学术专著、基金申报书及专利撰写。

---

## 📄 许可证
遵循 MIT 许可证及 [Agent Skills 开放标准](https://agentskills.io/home)，允许自由使用、分发与二次定制。
