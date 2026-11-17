# sciplotting: Publication-Ready Scientific Plotting Agent Skill

[English](README.md) | [中文说明](README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent_Skills-Open_Standard-8A2BE2)](https://agentskills.io/home)
[![SkillEvaluator](https://img.shields.io/badge/SkillEvaluator-100%2F100_Grade_A-brightgreen)](https://docs.nvidia.com/skills/skillevaluator/)
[![Python](https://img.shields.io/badge/Python-3.9+-informational)](https://www.python.org/)
[![R-ggplot2](https://img.shields.io/badge/R-ggplot2-276DC3)](https://ggplot2.tidyverse.org/)

A full-spectrum scientific plotting toolkit strictly adhering to the [Agent Skills Open Standard](https://agentskills.io/home). Engineered from the ground up for top-tier academic journals (Nature, Science, Cell, PNAS, The Lancet, NEJM), providing standardized palettes, layout specifications, multi-panel figure composition, multi-ecosystem code generation (Python / R / TikZ), and multimodal visual self-healing quality control. Compatible with Claude Code, Anthropic Codex, Cursor, Goose, VS Code, and 70+ AI coding assistants.

---

## ✨ Key Features

- 🎨 **Top-Tier Journal Palettes**: Curated color databases including official Nature low-saturation sets, Okabe-Ito colorblind-safe scales, Science/Cell/NEJM palettes, and Viridis/Plasma perceptual colormaps.
- 📐 **Rigorous Journal Dimensions**: Millimeter-accurate layouts for single-column (85–89 mm), 1.5-column (120–136 mm), and double-column (174–180 mm) across 10+ major publishers.
- 🧩 **Multi-Panel Master Figure Composer (`compose_figure.py`)**: Declarative grid layout (`GridSpec`) solving the common pain point of misaligned spines and inconsistent font scaling across subpanels (Figure 1a–f).
- 🩺 **Specialized Clinical & AI Figures**: Native support for Kaplan-Meier survival curves with time-synchronized **Number at Risk** tables, Meta-analysis forest plots with summary diamonds, and AI compute scaling laws with Pareto frontiers.
- 📊 **Unified Cross-Tool Ecosystem**:
  - **Python**: Zero-extra-dependency Matplotlib engine with TrueType font embedding (`pdf.fonttype = 42`).
  - **R / ggplot2**: Native `theme_nature()`, `scale_color_nature()`, and `save_journal_figure()` for bioinformatics pipelines.
  - **LaTeX / TikZ**: Verified standalone vector templates for linear pipelines, signaling pathways, and microfluidic apparatus.
  - **Mermaid**: Fast, lightweight workflow and CONSORT screening diagrams.
- 👁️ **Multimodal Visual Self-Healing QC (`verify_render.py`)**: Pixel-level boundary scanning to detect label clipping, edge truncation, blank canvas degradation, and contrast issues.
- ✅ **Colorblind & Grayscale Auditing (`check_palette.py`)**: Brettel-Vienot LMS cone-space simulations (Deuteranopia, Protanopia, Tritanopia) and CIE relative luminance calculation with $\Delta E$ conflict detection.
- 📦 **Zero-Configuration One-Click Install**: Installs via the `skills` CLI across all compliant Coding Agents in a single command.

---

## 📦 One-Click Installation

### Prerequisites
- **Node.js ≥ 22.20** (for running the `skills` CLI)
- **Python ≥ 3.9** (optional for running scripts locally; agent-level specification guidance requires no Python installation)
- Optional Python dependencies: `pip install matplotlib numpy pandas scipy pillow`

### 1. Direct Remote Installation from GitHub (Recommended)
Install globally to all detected AI Coding Agents without manual cloning:
```bash
npx skills add axjing/sciplotting -g --all
```

Options:
- `axjing/sciplotting`: GitHub repository shorthand (full URL `https://github.com/axjing/sciplotting` is also supported)
- `-g`: Global install across all agent conversations and projects
- `--all`: Automatically configures all supported Coding Agents

### 2. Install to Specific Agents
To install only to selected programming tools:
```bash
# Example: Claude Code + Codex + Cursor
npx skills add axjing/sciplotting -g -a claude-code codex cursor
```

Supported Coding Agents:
Claude Code, Anthropic Codex, Cursor, Goose, VS Code, OpenCode, Letta, Gemini CLI, GitHub Copilot, and 70+ compatible tools.

### 3. Windows Compatibility
On Windows, if symlink creation is restricted, use the `--copy` flag:
```bash
npx skills add axjing/sciplotting -g --all --copy
```

### 4. Local Installation from Source
```bash
git clone https://github.com/axjing/sciplotting.git
cd sciplotting
npx skills add . -g --all
```

### 5. Verification & Management
```bash
# List all globally installed skills
npx skills list -g

# Update to latest release
npx skills update sciplotting -g

# Uninstall
npx skills remove sciplotting -g
```

---

## 🚀 Quickstart & Examples

### 1. Multi-Panel Master Figure Composition (Figure 1a–d)
Eliminate inconsistent font sizes and mismatched spines when assembling complex multi-panel publication figures:
```bash
python scripts/python/compose_figure.py \
  --journal nature-double \
  --output Fig1_master_composite.pdf
```

### 2. Kaplan-Meier Survival Analysis with Number at Risk Table
Generate clinical oncology survival curves with synchronized risk tables and Log-rank test $P$-values:
```bash
python scripts/python/plot_survival.py \
  --journal nature-single \
  --output Fig2_survival.pdf
```

### 3. Clinical Meta-Analysis Forest Plot
Display study point estimates, inverse-variance sample weights, and pooled summary diamonds:
```bash
python scripts/python/plot_forest.py \
  --journal nature-single \
  --output Fig3_forest.pdf
```

### 4. AI Benchmarks & Compute Scaling Laws
Double-logarithmic power-law regression with theoretical extrapolation bands and Pareto frontier curves:
```bash
python scripts/python/plot_benchmark.py \
  --type scaling \
  --output Fig4_scaling.pdf
```

### 5. Quantitative Statistical Plots (Bar + SEM + Jittered Replicate Points)
Avoid dynamite plunger plots by overlaying individual biological replicates as required by Nature guidelines:
```bash
python scripts/python/plot_stats.py \
  --type bar \
  --journal nature-single \
  --palette nature_main_5 \
  --output Fig5_bar.pdf
```

### 6. High-Throughput Omics Volcano Plot with Gene Callouts
Differential expression with dual-cutoff threshold lines and collision-free top gene callouts:
```bash
python scripts/python/plot_omics.py \
  --type volcano \
  --journal nature-single \
  --output Fig6_volcano.pdf
```

### 7. Pure Python Vector Mechanism Diagram (Zero LaTeX Dependency)
Render publication-grade cellular signaling pathways and microfluidic devices directly with Matplotlib vector primitives:
```bash
python scripts/python/draw_diagram.py \
  --template pathway \
  --journal nature-double \
  --output Fig7_pathway.pdf
```

### 8. R / ggplot2 Publication Theme (Bioinformatics & Single-Cell)
```r
source("scripts/r/global_style.R")

# Automatically injects Nature Arial 7pt typography and palettes
p <- ggplot(df, aes(x = Group, y = Value, fill = Group)) +
  geom_bar(stat = "identity", width = 0.55) +
  scale_fill_nature("nature_main_5") +
  theme_nature(base_size = 7)

# Millimeter-accurate vector PDF export (89 mm single-column width)
save_journal_figure(p, "Fig8_R_nature.pdf", journal = "nature-single")
```

### 9. Visual QC & Colorblind Accessibility Auditing
```bash
# Pixel-level edge clipping, truncation, and dynamic contrast verification
python scripts/python/verify_render.py Fig1_master_composite.png --journal nature-double

# CVD simulation and Delta E color difference matrix audit
python scripts/python/check_palette.py --palette nature_main_5 --format markdown
```

---

## 📁 Repository Structure

```
sciplotting/
├── SKILL.md                    # [Main Entry] Agent instructions, 5-step workflow, metadata
├── README.md                   # [English] User documentation, installation, quickstart
├── README_zh.md                # [Chinese] Comprehensive user documentation
├── assets/
│   └── palettes.json           # Structured color library: categorical/sequential/diverging
├── references/
│   ├── journal_specs.md        # Publisher guidelines: dimensions (mm/in), DPI, font hierarchies
│   ├── figure_types.md         # Eight figure categories: design best practices & red flags
│   ├── diagram_specs.md        # 3-layer visual hierarchy, arrow grammar & biological glyphs
│   ├── compliance_checklist.md # 9-dimension pre-submission verification checklist
│   └── palette_guide.md        # Palette decision tree, LMS simulation & luminance formulas
├── scripts/
│   ├── python/
│   │   ├── global_style.py     # Global styling engine (Arial font, TrueType 42, despine)
│   │   ├── compose_figure.py   # Multi-panel master figure composer (GridSpec, a-d labels)
│   │   ├── plot_stats.py       # Statistical generator (bar/box/violin/line/scatter)
│   │   ├── plot_survival.py    # Kaplan-Meier survival curves + Number at Risk table
│   │   ├── plot_forest.py      # Meta-analysis & Hazard Ratio (HR/RR) forest plots
│   │   ├── plot_benchmark.py   # Pareto frontiers, compute scaling laws & radar charts
│   │   ├── plot_omics.py       # Omics generator (heatmap/volcano/PCA/bubble)
│   │   ├── draw_diagram.py     # Pure Python vector schematics (pathways/microfluidics)
│   │   ├── check_palette.py    # Accessibility auditor (CVD simulation & Delta E matrix)
│   │   └── verify_render.py    # Visual QC auditor (pixel-level edge clipping & self-healing)
│   ├── r/
│   │   ├── global_style.R      # R / ggplot2 theme_nature & palette injection engine
│   │   └── demo_plot.R         # R script example for publication-grade bar & box plots
│   ├── tikz/
│   │   ├── linear_workflow.tex     # Linear workflow template (pdflatex verified)
│   │   ├── parallel_workflow.tex   # Multi-arm parallel workflow template (pdflatex verified)
│   │   ├── signaling_pathway.tex   # Molecular signaling pathway template (pdflatex verified)
│   │   └── apparatus_schematic.tex # Microfluidic apparatus template (pdflatex verified)
│   └── mermaid/
│       └── diagram_templates.md    # Lightweight workflow templates (CONSORT/Bioinformatics)
├── tests/
│   └── test_sciplotting.py     # Automated regression test suite (12 unit tests passing)
└── .github/
    └── workflows/
        └── ci.yml              # GitHub Actions CI matrix (Ubuntu / Windows, Python 3.10-3.12)
```

---

## 🛠️ Quick Parameter Cheatsheet

### Journal Dimension Presets (`--journal`)
| Preset | Applicable Journals | Single Column | Double Column |
| :--- | :--- | :--- | :--- |
| `nature-single` / `nature-double` | Nature, Nature Communications, Nature Methods | 89 mm (3.50 in) | 180 mm (7.08 in) |
| `science-single` / `science-double` | Science, Science Advances, Science Immunology | 55 mm (2.17 in) | 178 mm (7.00 in) |
| `cell-single` / `cell-double` | Cell, Cancer Cell, Immunity, Molecular Cell | 85 mm (3.35 in) | 174 mm (6.85 in) |
| `pnas-single` / `pnas-double` | PNAS (Proc. Natl. Acad. Sci. U.S.A.) | 86 mm (3.38 in) | 178 mm (7.00 in) |
| `lancet-single` / `lancet-double` | The Lancet series journals | 85 mm (3.35 in) | 175 mm (6.89 in) |
| `nejm-single` / `nejm-double` | New England Journal of Medicine | 86 mm (3.38 in) | 178 mm (7.00 in) |

### Built-in Color Palettes (`--palette`)
- **Discrete Categorical**: `nature_main_5` (Nature 5-color set), `okabe_ito_8` (CVD colorblind-safe 8-color set), `science_classic_6`, `cell_press_6`, `nejm_classic_5`
- **Continuous Sequential**: `viridis` (perceptually uniform), `plasma` (high-contrast warm), `cividis` (optimized for deuteranopia & tritanopia)
- **Bipolar Diverging**: `RdBu` (classic two-tailed red-blue), `PRGn` (colorblind-safe purple-green)
- **Fluorescence Multi-Channel**: `dual_channel` (Green + Magenta, avoids red-green ambiguity), `triple_channel` (Cyan + Magenta + Yellow)

---

## 🧪 Quality Assurance & Benchmarks

`sciplotting` is continuously tested for compliance and reliability:
- **NVIDIA SkillEvaluator Score**: **100.0 / 100 (Grade: A)** (Correctness 100%, Discoverability 100%, Reliability 100%, Efficiency 100%).
- **PII & Secrets Scan**: Zero sensitive keys, private paths, or personal identifiers detected.
- **Unit Test Coverage**: 12 automated unit tests covering global styling, colorimetry, survival mathematics, and figure composition (`python -m unittest tests/test_sciplotting.py`).
- **LaTeX Compilation**: All TikZ `.tex` templates compiled and verified with `pdflatex`.

---

## ❓ Frequently Asked Questions (FAQ)

**Q: My AI Agent cannot discover the skill after installation?**  
A: Ensure the directory name matches the `name` field in `SKILL.md` (`sciplotting`). Restart your coding agent session to refresh skill cache.

**Q: Can I generate diagrams without installing TeXLive or LaTeX?**  
A: Absolutely. Run `scripts/python/draw_diagram.py` for pure Python vector diagram generation with zero external dependencies.

**Q: Will exported PDF fonts display correctly across different operating systems?**  
A: Yes. `global_style.py` enforces `pdf.fonttype = 42` (TrueType font embedding), preventing Type 3 rasterization and ensuring font fidelity on macOS, Windows, Linux, and publisher typesetting software.

**Q: Can I use my own CSV datasets with the CLI scripts?**  
A: Yes. Pass `--data path/to/your_data.csv`. If omitted, scripts automatically generate synthetic datasets with standard academic statistical distributions for testing.

**Q: Is commercial or patent use permitted?**  
A: Yes. All code, styles, and palettes adhere to standard open academic guidelines and the MIT License.

---

## 📄 License
Released under the [MIT License](LICENSE) and compliant with the [Agent Skills Open Standard](https://agentskills.io/home).
