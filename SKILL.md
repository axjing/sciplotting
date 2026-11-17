---
name: sciplotting
title: 顶刊科研绘图全场景助手
description: 覆盖定量统计、组学分析、实验成像、机制模式、技术流程、结构装置六类科研配图，提供符合Nature/Science/Cell顶刊标准的配色推荐、排版规范、多子图拼版编排、代码生成(Python/R/TikZ)与多模态合规自愈校验，全程满足色盲友好与印刷适配要求。
tags: ["科研绘图", "顶刊配色", "学术可视化", "Nature规范", "投稿配图", "科研示意图", "多子图拼版", "生存分析", "森林图", "ggplot2"]
triggers:
  - "科研绘图配色"
  - "顶刊配图规范"
  - "柱状图/箱线图配色"
  - "热图/火山图配色"
  - "免疫荧光配色"
  - "机制图/通路图设计"
  - "技术路线图/流程图"
  - "Graphical Abstract"
  - "投稿图片格式要求"
  - "科研图合规检查"
  - "TikZ 科研图"
  - "Python 科研绘图"
  - "多子图拼版"
  - "生存分析曲线"
  - "Kaplan-Meier"
  - "森林图"
  - "Forest Plot"
  - "Scaling Law 绘图"
  - "R 语言科研绘图"
  - "ggplot2 顶刊主题"
---

## 1. 技能目标
为 Coding Agent 注入全场景顶刊科研配图的流程化知识体系与可执行工具链，确保输出的图表代码与示意图严格匹配 Nature, Science, Cell, PNAS, Lancet, NEJM 等国际顶刊作者指南（Author Guidelines）。
全面规避配色违规、分辨率不达标、字号过小、截断坐标轴、标签裁剪碰撞、色彩空间错位及色盲无障碍缺陷等常见技术拒稿风险，实现「需求识别 → 类型匹配 → 拼版编排 → 方案输出 → 视觉自检自愈」的自动化闭环。

---

## 2. 核心能力范围
1. **全场景配色推荐**：覆盖 6 大类科研配图的专属色板（基于 `assets/palettes.json`），提供十六进制色值、适用场景与顶级期刊文献依据。
2. **分类型排版规范**：针对单栏（85-89 mm）、1.5 栏（120-136 mm）、双栏（174-180 mm）提供精确的画布尺寸、字体层级、线条粗细与边框设定。
3. **多子图联合拼版编排 (`compose_figure.py`)**：一键生成由多个独立子图（Figure 1a-f）构成的复合主图，统一字体缩放比例，像素级对齐坐标轴脊线，注入期刊标号。
4. **多语言与工具代码生成**：
   - **Python**：基于纯原生渲染，输出带误差棒与抖动点的统计图、聚类热图、火山图、PCA、KM 生存曲线、Meta 森林图、标度律曲线与纯矢量示意图；
   - **R / ggplot2**：提供原生 `theme_nature()` 与色彩标度 `scale_color_nature()`，无缝衔接生物信息学分析管线；
   - **TikZ / LaTeX**：输出印刷级、可无限缩放的矢量路线图、信号通路图与微流控芯片构造图；
   - **Mermaid**：输出适用于 GitHub/草稿/Supplementary 的轻量级流程图与 CONSORT 入组图。
5. **多模态视觉自愈与全维度合规校验**：
   - 计算机视觉边缘裁剪扫描 (`verify_render.py`)：检测轴标签溢出、画布空白与对比度缺陷；
   - 色彩无障碍仿真 (`check_palette.py`)：仿真红色盲、绿色盲、蓝黄色盲，计算 CIE 相对明度与色差矩阵。
6. **跨图一致性管控**：保障同一篇学术论文中所有主图与补充图的分组颜色、标识符号与线型体系高度绑定、完全一致。

---

## 3. 标准执行工作流
Agent 加载本技能后，必须严格遵循以下五步标准作业程序响应用户：

```
用户提出绘图/配色需求
         │
         ▼
[步骤 1: 配图类型识别] ── 匹配到 6 大核心品类之一
         │
         ▼
[步骤 2: 工具与资源匹配] ─ 读取 assets/ 与 references/，选择最优脚本 (Python/R/TikZ)
         │
         ▼
[步骤 3: 拼版与排版设计] ─ 确定单/双栏尺寸，规划单图或多子图大图板 (compose_figure)
         │
         ▼
[步骤 4: 标准化方案输出] ─ 输出色板、排版尺寸、可运行代码、说明
         │
         ▼
[步骤 5: 视觉质检与自愈] ─ 执行 verify_render.py 与 check_palette.py 自愈修复
```

### 步骤 1：配图类型识别
将用户的科研数据与绘图意图准确归类至 6 大核心品类：
| 配图大类 | 核心数据特征 | 典型子类型 | 对应参考文档 / 脚本 |
| :--- | :--- | :--- | :--- |
| **1. 定量数据统计图** | 离散分组定量对比、统计显著性 | 柱状图+散点、箱线图、小提琴图、折线动力学、散点回归、生存曲线 | `plot_stats.py`, `plot_survival.py`, `plot_forest.py` |
| **2. 高通量组学分析图** | 高维连续矩阵、差异表达、降维聚类 | 表达热图、火山图、PCA/t-SNE/UMAP、GO/KEGG 富集气泡图 | `plot_omics.py` |
| **3. 实验成像与表征图** | 仪器显微成像、条带谱图、多通道 Merge | 免疫荧光共聚焦、电镜 SEM/TEM、Western Blot 凝胶、XRD/NMR 谱图 | `references/figure_types.md` 第 3 节 |
| **4. 机制原理与模式图** | 生物逻辑阐释、靶点作用、结论凝练 | 信号通路图、分子作用机制、概念模型图、Graphical Abstract | `draw_diagram.py`, `scripts/tikz/` |
| **5. 技术流程与方案图** | 步骤串联、分析流程、队列筛选 | 实验路线图、生信分析管线、CONSORT 临床筛选流、算法流程图 | `scripts/tikz/`, `scripts/mermaid/` |
| **6. 结构与装置示意图** | 空间构型、工程器械、微流控构造 | 分子空间构型、材料层叠图、流动反应器、微流控芯片、活体注射定位 | `apparatus_schematic.tex`, `draw_diagram.py` |
| **★ 多子图主图拼版** | 跨图型整版联合编排 | 组合大图 (Figure 1a-f: 机制 + 统计 + 组学 + 标尺) | `compose_figure.py` |

### 步骤 2：工具与资源自动匹配
- **查阅期刊尺寸与格式**：读取 `references/journal_specs.md`
- **获取标准色值**：读取 `assets/palettes.json` 中的对应色板
- **生成常规统计配图**：调用 `scripts/python/plot_stats.py`
- **生成临床生存分析 (KM)**：调用 `scripts/python/plot_survival.py`
- **生成 Meta 分析森林图**：调用 `scripts/python/plot_forest.py`
- **生成 AI/计算标杆与标度律**：调用 `scripts/python/plot_benchmark.py`
- **生成组学配图**：调用 `scripts/python/plot_omics.py`
- **生成多子图复合大版面**：调用 `scripts/python/compose_figure.py`
- **R / ggplot2 绘图**：调用 `scripts/r/global_style.R`
- **生成纯 Python 矢量示意图**：调用 `scripts/python/draw_diagram.py`
- **生成印刷级 TikZ 矢量示意图**：调用 `scripts/tikz/` 模板
- **生成轻量级流程图**：调用 `scripts/mermaid/diagram_templates.md`
- **执行视觉质检自愈**：调用 `scripts/python/verify_render.py`
- **执行配色合规审计**：调用 `scripts/python/check_palette.py`

### 步骤 3：标准化输出要求
输出内容必须结构完整，包含：
1. **对应场景的顶刊配色方案**：注明 Hex 色值、色相名称与期刊依据；
2. **目标期刊排版参数**：注明单栏/双栏宽度（mm / in）、字号阶梯（pt）与误差棒定义；
3. **完整且可独立运行的代码**：包含数据准备、样式加载、矢量导出与图形关闭；
4. **色盲友好与灰度适配等级说明**。

### 步骤 4：强制合规自检与视觉自愈
输出代码或方案前，必须对照 `references/compliance_checklist.md` 进行检查，并运行视觉质检工具：
- 严禁出现纯红-纯绿直接对比；
- 连续渐变严禁使用 `jet` 或 `rainbow`；
- 分类颜色数量控制在合理范围（主图推荐 $\le 5$ 组，最大 $\le 8$ 组）；
- 小样本（$n < 20$）柱状图必须叠加离散生物学重复散点；
- 全图文字在印刷缩放后不得小于 5 pt；
- 若 `verify_render.py` 报告边缘裁剪风险，主动在代码中增加 `pad_inches` 或调整刻度角度。

---

## 4. 基础合规红线（强制执行）
1. **色盲友好红线**：禁止红-绿直接对比，所有分类色板必须兼容红绿色盲（Deuteranopia/Protanopia 仿真 $\Delta E \ge 10$）。
2. **色彩空间保真**：审稿初投强制 sRGB；终稿提交印刷前需确保无超出 CMYK 域的超饱和荧光色。
3. **数量控制**：单图分类色彩 $\le 8$ 种，主图建议 $\le 5$ 种；超出数量必须结合点形状、线型或分面（Facet）辅助区分。
4. **禁用清单**：
   - ❌ 禁用 `jet` / `rainbow` 色板；
   - ❌ 禁用 Excel / Office 默认高饱和配色；
   - ❌ 禁用 3D 浮雕柱体、渐变反光装饰球体；
   - ❌ 禁用无生物学意义的纯装饰底纹。
5. **灰度可区分**：所有组别转为黑白灰度后，相邻类别相对亮度差值 $\Delta Y \ge 0.10$。
6. **跨图一致性**：同一论文内，相同实验处理、基因型在所有主图与补充图中颜色严格一致。

---

## 5. 核心工具与脚本调用参考
- **主图联合拼版**：
  ```bash
  python scripts/python/compose_figure.py --journal nature-double --output Fig1_composite.pdf
  ```
- **生成临床生存分析曲线 (带 Number at Risk 表)**：
  ```bash
  python scripts/python/plot_survival.py --journal nature-single --output Fig_survival.pdf
  ```
- **生成临床 Meta 分析森林图**：
  ```bash
  python scripts/python/plot_forest.py --journal nature-single --output Fig_forest.pdf
  ```
- **生成计算标度律与 AI 标杆图**：
  ```bash
  python scripts/python/plot_benchmark.py --type pareto --output Fig_pareto.pdf
  ```
- **R / ggplot2 主题使用**：
  ```r
  source("scripts/r/global_style.R")
  p <- ggplot(df, aes(x, y, fill=group)) + geom_bar(...) + theme_nature() + scale_fill_nature()
  save_journal_figure(p, "Fig_R.pdf", journal="nature-single")
  ```
- **执行视觉质检与自愈诊断**：
  ```bash
  python scripts/python/verify_render.py Fig1_composite.png --journal nature-double
  ```
- **执行配色合规性审计**：
  ```bash
  python scripts/python/check_palette.py --palette nature_main_5 --format markdown
  ```
