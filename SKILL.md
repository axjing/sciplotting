---
name: sciplotting
version: "2.0.0"
title: 顶刊科研绘图全场景助手
description: Use this skill when you need to create publication-ready figures, palettes, multi-panel layouts, or verify compliance for Nature, Science, and Cell submissions.
author: "axjing <axjing@users.noreply.github.com>"
metadata:
  author: "axjing <axjing@users.noreply.github.com>"
  version: "2.0.0"
  tags: ["scientific-plotting", "nature", "science", "cell", "data-visualization"]
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

# sciplotting: 顶刊科研绘图全场景助手

## Purpose
Use this skill when you need to create publication-ready scientific figures, generate journal-compliant palettes, compose multi-panel layouts, or audit visual and colorblind compliance for Nature, Science, Cell, PNAS, Lancet, and NEJM submissions.

---

## Prerequisites
- **Python Environment**: Python >= 3.9
- **Core Dependencies**:
  ```bash
  pip install matplotlib numpy scipy pandas pillow
  ```
- **Optional R Environment**: R >= 4.0, `ggplot2` (for `scripts/r/`)
- **Optional LaTeX Environment**: TeXLive / MiKTeX (`pdflatex`) for compiling `scripts/tikz/`.

---

## Resources
This resource-based skill provides standardized assets, templates, and reference guides:
- **Color Palettes Asset**: `assets/palettes.json` - Complete structured database of categorical, sequential, diverging, and fluorescence color hex codes.
- **Journal Specifications Guide**: `references/journal_specs.md` - Dimensions (mm/in), DPI, font size hierarchies, and line weights for 10+ journals.
- **Figure Types Best Practices**: `references/figure_types.md` - Design rules and red flags for 8 scientific figure categories.
- **Diagram Layout Specifications**: `references/diagram_specs.md` - 3-layer visual hierarchy, arrow grammar, and standardized biological component glyphs.
- **Submission Compliance Checklist**: `references/compliance_checklist.md` - 9-dimension pre-submission verification checklist.
- **Palette Decision Tree & Guide**: `references/palette_guide.md` - Colorblind simulation mathematics and grayscale luminance formulas.
- **Vector TikZ Templates**: `scripts/tikz/` - Standalone templates for linear workflows, parallel arms, signaling pathways, and apparatus schematics.
- **Mermaid Markdown Templates**: `scripts/mermaid/diagram_templates.md` - Lightweight workflow and protocol diagrams.

---

## Instructions
Execute the following step-by-step workflow when responding to user requests:

1. **Identify Figure Category**: Match the request against the 8 core scientific categories (Statistical, Omics, Imaging, Mechanism, Workflow, Structural, Clinical, or Multi-panel composite).
2. **Select Tool & Template**:
   - For composite master figures: Execute `scripts/python/compose_figure.py`.
   - For statistical comparisons: Execute `scripts/python/plot_stats.py`.
   - For clinical survival: Execute `scripts/python/plot_survival.py`.
   - For meta-analysis: Execute `scripts/python/plot_forest.py`.
   - For high-throughput omics: Execute `scripts/python/plot_omics.py`.
   - For AI benchmarks & scaling laws: Execute `scripts/python/plot_benchmark.py`.
   - For R / ggplot2 workflows: Load `scripts/r/global_style.R`.
   - For vector schematics: Use `scripts/tikz/` or execute `scripts/python/draw_diagram.py`.
3. **Format Layout & Sizing**: Set exact journal column widths (Single: 85-89 mm, Double: 174-180 mm) and apply TrueType font embedding (`pdf.fonttype = 42`).
4. **Audit Color Accessibility**: Run `scripts/python/check_palette.py` to ensure zero red-green juxtaposition and Delta E >= 10 across CVD simulations.
5. **Verify Visual Geometry**: Run `scripts/python/verify_render.py` on the output image to detect edge clipping, text cutoff, or low contrast, and apply self-healing adjustments if needed.

---

## Examples

### Example 1: Multi-panel Composite Figure (Figure 1a-d)
```bash
python scripts/python/compose_figure.py --journal nature-double --output Fig1_composite.pdf
```

### Example 2: Kaplan-Meier Survival Analysis Curve
```bash
python scripts/python/plot_survival.py --journal nature-single --output Fig_survival.pdf
```

### Example 3: Meta-Analysis Forest Plot
```bash
python scripts/python/plot_forest.py --journal nature-single --output Fig_forest.pdf
```

### Example 4: Visual QC Edge Clipping Verification
```bash
python scripts/python/verify_render.py Fig1_composite.png --journal nature-double
```

### Example 5: Palette Colorblind Compliance Audit
```bash
python scripts/python/check_palette.py --palette nature_main_5 --format markdown
```

---

## Error Handling & Validation
- **Colorblind Violations**: When `check_palette.py` reports fatal collisions (BLOCK), replace with colorblind-safe palettes such as `okabe_ito_8` or `PRGn`.
- **Label Edge Clipping**: When `verify_render.py` reports border overflow, add `bbox_inches='tight', pad_inches=0.08` and increase `subplots_adjust` bottom margin.
- **Missing Data Fallback**: When input CSV is omitted, scripts automatically generate synthetic publication-grade data for immediate visual verification.

---

## Limitations
- **3D Surface Rendering**: This skill specializes in 2D statistical, omics, and vector mechanism diagrams; it does not cover 3D protein cryo-EM density maps or molecular orbital ray-tracing.
- **CMYK Print Conversion**: Vector PDFs are exported in high-fidelity sRGB by default; final CMYK rasterization for physical print proofing should use Ghostscript or Photoshop.

---

## Troubleshooting

| Error / Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| Exported PDF text displays as blocks in Illustrator | Fonts not embedded (Type 3 rasterization) | Ensure `apply_journal_style()` is called to enforce `pdf.fonttype = 42` |
| Long X-axis tick labels truncated at bottom edge | Insufficient margin padding | Set `bbox_inches='tight'` and rotate tick labels with `rotation=30` |
| Bar chart flagged by reviewer as misleading | Small sample points hidden | Never use standalone bars; always overlay jittered data points with `ax.scatter()` |
| Heatmap turns into muddy solid color in grayscale print | Non-uniform or rainbow colormap used | Replace colormap with `viridis`, `plasma`, or colorblind-optimized `cividis` |
| LaTeX compilation error in TikZ scripts | Missing TeXLive packages | Fall back to the pure Python vector generator `scripts/python/draw_diagram.py` |
