---
name: sciplotting
title: 顶刊科研绘图全场景助手
description: 覆盖定量统计、组学分析、实验成像、机制模式、技术流程、结构装置六类科研配图，提供符合Nature/Science/Cell顶刊标准的配色推荐、排版规范、代码生成与合规校验，全程满足色盲友好与印刷适配要求。
tags: ["科研绘图", "顶刊配色", "学术可视化", "Nature规范", "投稿配图", "科研示意图"]
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
---

## 1. 技能目标
为 Coding Agent 注入全场景顶刊科研配图的流程化知识体系与可执行工具链，确保输出的图表代码与示意图严格匹配 Nature, Science, Cell, PNAS, Lancet, NEJM 等国际顶刊作者指南（Author Guidelines）。
全面规避配色违规、分辨率不达标、字号过小、截断坐标轴、色彩空间错位及色盲无障碍缺陷等常见技术拒稿风险，实现「需求识别 → 类型匹配 → 方案输出 → 合规自检」的自动化闭环。

---

## 2. 核心能力范围
1. **全场景配色推荐**：覆盖 6 大类科研配图的专属色板（基于 `assets/palettes.json`），提供十六进制色值、适用场景与顶级期刊文献依据。
2. **分类型排版规范**：针对单栏（85-89 mm）、1.5 栏（120-136 mm）、双栏（174-180 mm）提供精确的画布尺寸、字体层级、线条粗细与边框设定。
3. **多工具代码生成**：
   - **Python**：基于 `matplotlib` 纯原生渲染，输出带误差棒与显著性星号的统计图表、高通量聚类热图、火山图、PCA 降维图与矢量示意图；
   - **TikZ / LaTeX**：输出印刷级、可无限缩放的矢量路线图、信号转导通路图与微流控装置原理图；
   - **Mermaid**：输出适用于 GitHub/草稿/Supplementary 的轻量级流程图与 CONSORT 入组图。
4. **全维度合规校验**：自动化仿真红色盲 (Protanopia)、绿色盲 (Deuteranopia)、蓝黄色盲 (Tritanopia)，审计 CIE 相对明度与灰度打印兼容性，扫描红绿对立与 Jet 彩虹色板陷阱。
5. **跨图一致性管控**：保障同一篇学术论文中所有主图与补充图的分组颜色、标识符号与线型体系高度绑定、完全一致。

---

## 3. 标准执行工作流
Agent 加载本技能后，必须严格遵循以下四步标准作业程序响应用户：

```
用户提出绘图/配色需求
         │
         ▼
[步骤 1: 配图类型识别] ── 匹配到 6 大核心品类之一
         │
         ▼
[步骤 2: 工具与资源匹配] ─ 读取 assets/ 与 references/，调用 scripts/
         │
         ▼
[步骤 3: 标准化方案输出] ─ 输出色板、排版尺寸、可运行代码、说明
         │
         ▼
[步骤 4: 强制合规自检] ── 运行 check_palette.py 验证色盲友好与灰度
```

### 步骤 1：配图类型识别
将用户的科研数据与绘图意图准确归类至 6 大核心品类：
| 配图大类 | 核心数据特征 | 典型子类型 | 对应参考文档 |
| :--- | :--- | :--- | :--- |
| **1. 定量数据统计图** | 离散分组定量对比、统计显著性 | 柱状图+散点、箱线图、小提琴图、折线动力学、散点回归、生存曲线 | `references/figure_types.md` 第 1 节 |
| **2. 高通量组学分析图** | 高维连续矩阵、差异表达、降维聚类 | 表达热图、火山图、PCA/t-SNE/UMAP、GO/KEGG 富集气泡图 | `references/figure_types.md` 第 2 节 |
| **3. 实验成像与表征图** | 仪器显微成像、条带谱图、多通道 Merge | 免疫荧光共聚焦、电镜 SEM/TEM、Western Blot 凝胶、XRD/NMR 谱图 | `references/figure_types.md` 第 3 节 |
| **4. 机制原理与模式图** | 生物逻辑阐释、靶点作用、结论凝练 | 信号通路图、分子作用机制、概念模型图、Graphical Abstract | `references/figure_types.md` 第 4 节 & `diagram_specs.md` |
| **5. 技术流程与方案图** | 步骤串联、分析流程、队列筛选 | 实验路线图、生信分析管线、CONSORT 临床筛选流、算法流程图 | `references/figure_types.md` 第 5 节 |
| **6. 结构与装置示意图** | 空间构型、工程器械、微流控构造 | 分子空间构型、材料层叠图、流动反应器、微流控芯片、活体注射定位 | `references/figure_types.md` 第 6 节 |

### 步骤 2：工具与资源自动匹配
根据用户需求场景自动选择资源与可执行脚本：
- **查阅期刊尺寸与格式**：读取 `references/journal_specs.md`
- **获取标准色值**：读取 `assets/palettes.json` 中的对应色板
- **生成统计配图**：调用 `scripts/python/plot_stats.py`
- **生成组学配图**：调用 `scripts/python/plot_omics.py`
- **生成无 LaTeX 依赖的矢量示意图**：调用 `scripts/python/draw_diagram.py`
- **生成印刷级 TikZ 矢量示意图**：调用 `scripts/tikz/` 模板
- **生成轻量级流程图**：调用 `scripts/mermaid/diagram_templates.md`
- **进行配色合规审计**：调用 `scripts/python/check_palette.py`

### 步骤 3：标准化输出
输出内容必须结构完整，包含：
1. **对应场景的顶刊配色方案**：注明 Hex 色值、色相名称与期刊依据；
2. **目标期刊排版参数**：注明单栏/双栏宽度（mm / in）、字号阶梯（pt）与误差棒定义；
3. **完整且可独立运行的代码**：包含数据准备、样式加载、矢量导出与图形关闭；
4. **色盲友好与灰度适配等级说明**。

### 步骤 4：强制合规自检
输出代码或方案前，必须对照 `references/compliance_checklist.md` 进行检查：
- 严禁出现纯红-纯绿直接对比；
- 连续渐变严禁使用 `jet` 或 `rainbow`；
- 分类颜色数量控制在合理范围（主图推荐 $\le 5$ 组，最大 $\le 8$ 组）；
- 小样本（$n < 20$）柱状图必须叠加离散生物学重复散点；
- 全图文字在印刷缩放后不得小于 5 pt。

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

## 5. 分品类绘图规范速查
### 5.1 定量数据统计图
- **首选色板**：3-5 组首选 `nature_main_5`；6-8 组首选 `okabe_ito_8`。
- **排版规范**：去除 Top/Right 边框，Spine 线宽 0.8 pt，Tick 向外，字体 Arial/Helvetica。
- **核心要求**：对照组固定中性冷灰/冷蓝；处理组暖色；误差棒完整并写明含义；禁止截断纵坐标夸大差异。

### 5.2 高通量组学分析图
- **连续数值**：首选 `viridis`，高对比选用 `plasma`，极端无障碍选用 `cividis`。
- **正负差异**：首选 `RdBu`（红上调/蓝下调）或色盲友好 `PRGn`（紫上调/绿下调）。
- **核心要求**：Colorbar 明确标示 Z-score 截断范围与物理单位；PCA 坐标轴标注方差贡献率。

### 5.3 实验成像与表征图
- **荧光成像**：双通道绿 + 品红，三通道青 + 品红 + 黄；必须配套单通道灰度图。
- **WB/凝胶**：保留真实背景（上下 3-5 倍胶高）；拼接胶必须画虚线分隔；标明 kDa 分子量。
- **核心要求**：右下角必附实体 Scale bar，并在图注中指明标尺物理长度。

### 5.4 机制原理与模式图
- **配色原则**：1 种核心强调色（#E15759）+ 1 种辅助色（#4E79A7）+ 多级灰阶背景。
- **符号语义**：实心三角箭头表示直接激活；平头 T 字杠表示抑制；虚线表示间接作用；弯箭表示跨膜转位。
- **核心要求**：层级清晰（背景边界 → 常规元件 → 高亮靶点），文字简明，无多余装饰。

### 5.5 技术流程与方案图
- **流向标准**：一律由左向右或自上而下；禁止交叉连线。
- **模块化对齐**：统一圆角矩形节点，内部文本居中；阶段上方附带时间轴或 Phase 色带。

### 5.6 结构与装置示意图
- **几何精度**：严格按工程比例或注明“Not to scale”；流体管路内部标出微小单向流向箭头。
- **材质区分**：液体用半透明（alpha=0.6），基底用哑光冷灰，金属件用低反光深灰。

---

## 6. 核心工具与脚本调用参考
- **全局绘图样式注入**：
  ```python
  from scripts.python.global_style import apply_journal_style, get_figsize, get_palette, save_figure
  apply_journal_style(journal="nature")
  ```
- **生成定量统计图**：
  ```bash
  python scripts/python/plot_stats.py --type bar --journal nature-single --palette nature_main_5 --output Fig1.pdf
  ```
- **生成组学配图**：
  ```bash
  python scripts/python/plot_omics.py --type volcano --journal nature-single --output Fig2_volcano.pdf
  ```
- **生成纯 Python 矢量示意图**：
  ```bash
  python scripts/python/draw_diagram.py --template pathway --output Fig3_mechanism.pdf
  ```
- **执行配色合规性审计**：
  ```bash
  python scripts/python/check_palette.py --palette nature_main_5 --format markdown
  ```
