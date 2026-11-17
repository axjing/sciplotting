"""
draw_diagram.py - 纯 Python 顶刊矢量示意图生成器 (Pure Python Vector Diagram Engine)

零 LaTeX 依赖，纯 Python 原生渲染出版级矢量示意图 (PDF, SVG, EPS, PNG)。
内置三种核心科研范式模板:
1. workflow: 线性与多阶段科研技术路线图 (Experimental Workflow)
2. pathway: 细胞信号传导与分子机制图 (Cellular Signaling Pathway)
3. apparatus: 微流控与实验装置构造原理图 (Microfluidic & Apparatus Schematic)
"""

import argparse
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

# 导入全局样式引擎
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from global_style import (
    apply_journal_style,
    get_figsize,
    get_palette,
    save_figure,
)


def draw_rounded_box(ax, x, y, w, h, text, facecolor, edgecolor="#262626", text_color="#262626", fontsize=7.0, boxstyle="round,pad=0.2,rounding_size=0.08"):
    """绘制高雅圆角矩形模块"""
    p = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=boxstyle,
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=0.8,
        zorder=3,
    )
    ax.add_patch(p)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=text_color,
        fontweight="normal",
        zorder=4,
    )
    return p


def draw_activation_arrow(ax, start, end, color="#262626", lw=1.0, rad=0.0):
    """绘制直接激活实心三角箭头"""
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>,head_length=4.5,head_width=2.8",
        connectionstyle=f"arc3,rad={rad}",
        color=color,
        linewidth=lw,
        zorder=3,
    )
    ax.add_patch(arrow)
    return arrow


def draw_inhibition_bar(ax, start, end, color="#D9534F", lw=1.0):
    """绘制直接抑制平头 T 字杠"""
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-[",
        color=color,
        linewidth=lw,
        zorder=3,
    )
    ax.add_patch(arrow)
    return arrow


def draw_workflow_diagram(ax):
    """绘制标准化科研路线流程图 (Workflow)"""
    steps = [
        {"title": "Step 1\nPatient Cohort", "sub": "Clinical samples (n=120)", "color": "#F8F9FA"},
        {"title": "Step 2\nSingle-Cell RNA-seq", "sub": "10x Genomics profiling", "color": "#F8F9FA"},
        {"title": "Step 3\nTarget Discovery", "sub": "Differentially expressed genes", "color": "#E9ECEF"},
        {"title": "Step 4\nMechanistic Assay", "sub": "CRISPR/Cas9 knockout", "color": "#E9ECEF"},
        {"title": "Step 5\nTherapeutic Target", "sub": "Lead small molecule validation", "color": "#FDE8E8", "edge": "#E15759", "accent": True},
    ]

    n = len(steps)
    box_w = 1.35
    box_h = 0.75
    gap = 0.45
    total_w = n * box_w + (n - 1) * gap
    start_x = (10.0 - total_w) / 2
    y_pos = 2.0

    # 阶段分界色带 (上方)
    phase1_w = 2 * box_w + gap
    phase2_w = 2 * box_w + gap
    phase3_w = box_w

    ax.add_patch(Rectangle((start_x, 3.1), phase1_w, 0.22, facecolor="#4E79A7", alpha=0.15, edgecolor="none"))
    ax.text(start_x + phase1_w / 2, 3.21, "Phase I: Cohort Screening", ha="center", va="center", fontsize=6.5, color="#4E79A7", fontweight="bold")

    p2_x = start_x + phase1_w + gap
    ax.add_patch(Rectangle((p2_x, 3.1), phase2_w, 0.22, facecolor="#59A14F", alpha=0.15, edgecolor="none"))
    ax.text(p2_x + phase2_w / 2, 3.21, "Phase II: Validation", ha="center", va="center", fontsize=6.5, color="#59A14F", fontweight="bold")

    p3_x = p2_x + phase2_w + gap
    ax.add_patch(Rectangle((p3_x, 3.1), phase3_w, 0.22, facecolor="#E15759", alpha=0.15, edgecolor="none"))
    ax.text(p3_x + phase3_w / 2, 3.21, "Phase III: Efficacy", ha="center", va="center", fontsize=6.5, color="#E15759", fontweight="bold")

    # 绘制各节点
    for i, s in enumerate(steps):
        x = start_x + i * (box_w + gap)
        ec = s.get("edge", "#8C8C8C")
        tc = "#262626"
        p = draw_rounded_box(ax, x, y_pos, box_w, box_h, s["title"], s["color"], edgecolor=ec, text_color=tc, fontsize=6.5)

        # 辅助次要文字
        ax.text(x + box_w / 2, y_pos - 0.25, s["sub"], ha="center", va="top", fontsize=5.5, color="#6C757D")

        # 箭头
        if i < n - 1:
            arrow_color = "#E15759" if i == n - 2 else "#262626"
            draw_activation_arrow(
                ax,
                (x + box_w, y_pos + box_h / 2),
                (x + box_w + gap, y_pos + box_h / 2),
                color=arrow_color,
                lw=1.0,
            )

    ax.set_xlim(0, 10)
    ax.set_ylim(0.5, 3.8)


def draw_pathway_diagram(ax):
    """绘制细胞分子机制信号通路图 (Cellular Signaling Pathway)"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)

    # 1. 胞外与细胞膜区域
    # 细胞膜
    membrane = Rectangle((0.5, 4.8), 9.0, 0.35, facecolor="#E2E8F0", edgecolor="#94A3B8", lw=0.8, zorder=2)
    ax.add_patch(membrane)
    ax.text(0.7, 5.35, "Extracellular Space", fontsize=6.5, color="#64748B", fontweight="bold")
    ax.text(0.7, 4.45, "Cytoplasm", fontsize=6.5, color="#64748B", fontweight="bold")
    ax.text(9.3, 4.97, "Plasma Membrane", ha="right", va="center", fontsize=5.5, color="#475569")

    # 2. 细胞核区域
    nucleus = patches.FancyBboxPatch(
        (3.0, 0.4),
        4.0,
        1.8,
        boxstyle="round,pad=0.2,rounding_size=0.4",
        facecolor="#F1F5F9",
        edgecolor="#CBD5E1",
        lw=0.8,
        linestyle="--",
        zorder=1,
    )
    ax.add_patch(nucleus)
    ax.text(3.3, 1.95, "Nucleus", fontsize=6.5, color="#64748B", fontweight="bold")

    # 3. 胞外配体与受体 (Ligand & Receptor)
    # 配体 (Ligand)
    ligand = Circle((3.5, 5.8), 0.22, facecolor="#F28E2B", edgecolor="#262626", lw=0.8, zorder=4)
    ax.add_patch(ligand)
    ax.text(3.5, 6.2, "Ligand", ha="center", fontsize=6.0, fontweight="bold")

    # 膜受体 (Receptor RTK)
    draw_rounded_box(ax, 3.0, 4.6, 1.0, 0.75, "RTK", facecolor="#76B7B2", fontsize=6.5)
    draw_activation_arrow(ax, (3.5, 5.58), (3.5, 5.35), color="#262626")

    # 4. 胞内激酶级联传导
    draw_rounded_box(ax, 3.0, 3.4, 1.0, 0.55, "MAPK", facecolor="#E9ECEF", fontsize=6.5)
    draw_activation_arrow(ax, (3.5, 4.6), (3.5, 3.95), color="#262626")

    # 抑制剂靶向阻断 (Inhibitor)
    draw_rounded_box(ax, 1.2, 3.4, 0.9, 0.55, "Inhibitor X", facecolor="#FEE2E2", edgecolor="#E15759", text_color="#B91C1C", fontsize=6.0)
    draw_inhibition_bar(ax, (2.1, 3.67), (3.0, 3.67), color="#E15759", lw=1.2)

    # 核心效应因子 (突破靶标高亮高饱和)
    draw_rounded_box(ax, 3.0, 2.3, 1.0, 0.55, "STAT3*", facecolor="#E15759", text_color="#FFFFFF", fontsize=6.5)
    draw_activation_arrow(ax, (3.5, 3.4), (3.5, 2.85), color="#262626")

    # 5. 易位入核与转录启动
    # 转录因子在核内
    draw_rounded_box(ax, 4.2, 0.8, 1.1, 0.5, "STAT3-Dimer", facecolor="#E15759", text_color="#FFFFFF", fontsize=6.0)
    draw_activation_arrow(ax, (3.8, 2.3), (4.5, 1.3), color="#E15759", lw=1.0, rad=-0.2)

    # DNA 示意与转录箭头
    ax.plot([3.8, 6.5], [0.65, 0.65], lw=1.5, color="#334155", zorder=3)
    ax.text(3.9, 0.5, "Promoter", fontsize=5.5, color="#64748B")
    draw_activation_arrow(ax, (5.3, 0.65), (5.3, 1.1), color="#262626", lw=0.8)
    draw_activation_arrow(ax, (5.3, 1.1), (6.2, 1.1), color="#262626", lw=0.8)
    ax.text(6.4, 1.1, "Target Gene Expression\n(Survival & Proliferation)", va="center", fontsize=6.0, color="#0F172A", fontweight="bold")


def draw_apparatus_diagram(ax):
    """绘制微流控液滴反应芯片装置示意图 (Microfluidic Apparatus)"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)

    # 芯片基底轮廓
    chip = FancyBboxPatch((1.0, 0.8), 8.0, 3.4, boxstyle="round,pad=0.2,rounding_size=0.2", facecolor="#F8FAFC", edgecolor="#CBD5E1", lw=1.0)
    ax.add_patch(chip)
    ax.text(1.3, 3.9, "Microfluidic Droplet Generator Chip", fontsize=7.0, color="#475569", fontweight="bold")

    # 进样口 1 (水相/细胞悬液)
    draw_rounded_box(ax, 1.5, 2.8, 1.2, 0.5, "Aqueous\n(Cells/Reagents)", facecolor="#E0F2FE", edgecolor="#0284C7", fontsize=5.5)
    # 进样口 2 (油相)
    draw_rounded_box(ax, 1.5, 1.4, 1.2, 0.5, "Oil Phase\n(Surfactant)", facecolor="#FEF3C7", edgecolor="#D97706", fontsize=5.5)

    # 微流控通道 (流动交叉十字点)
    # 水相通道
    ax.plot([2.7, 4.2], [3.05, 2.3], color="#0284C7", lw=1.5)
    # 油相上下夹击通道
    ax.plot([2.7, 4.2], [1.65, 2.3], color="#D97706", lw=1.5)

    # 交汇十字液滴形成点
    junction = Circle((4.2, 2.3), 0.15, facecolor="#38BDF8", edgecolor="#0284C7", lw=0.8)
    ax.add_patch(junction)
    ax.text(4.2, 2.65, "Junction", ha="center", fontsize=5.5, color="#0369A1", fontweight="bold")

    # 反应与混合蛇形通道
    snake_x = [4.2, 5.0, 5.0, 5.8, 5.8, 6.6]
    snake_y = [2.3, 2.3, 2.8, 2.8, 1.8, 1.8]
    ax.plot(snake_x, snake_y, color="#38BDF8", lw=1.2, linestyle="-")

    # 形成的水包油微液滴
    for dx in [4.6, 5.4, 6.2]:
        d = Circle((dx, 2.3 if dx == 4.6 else (2.8 if dx == 5.4 else 1.8)), 0.08, facecolor="#E0F2FE", edgecolor="#0284C7", lw=0.6)
        ax.add_patch(d)

    # 激光检测窗口 (Laser interrogation)
    ax.plot([7.2, 7.2], [1.2, 2.4], color="#EF4444", lw=1.0, linestyle="--")
    ax.text(7.2, 1.0, "Laser 488 nm", ha="center", fontsize=5.5, color="#DC2626")

    # 出样收集池
    draw_rounded_box(ax, 7.5, 1.5, 1.2, 0.6, "Collection\nReservoir", facecolor="#F1F5F9", edgecolor="#64748B", fontsize=5.5)
    draw_activation_arrow(ax, (6.6, 1.8), (7.5, 1.8), color="#262626", lw=1.0)


def main():
    parser = argparse.ArgumentParser(description="纯 Python 顶刊矢量示意图生成器 (draw_diagram.py)")
    parser.add_argument(
        "--template",
        choices=["workflow", "pathway", "apparatus"],
        default="workflow",
        help="示意图模板: workflow (技术路线), pathway (分子机制信号通路), apparatus (实验装置结构)",
    )
    parser.add_argument("--journal", type=str, default="nature-double", help="目标期刊预设 (示意图通常建议 nature-double 或 cell-double)")
    parser.add_argument("--palette", type=str, default="nature_main_5", help="色板名称")
    parser.add_argument("--output", type=str, default="Fig_diagram.pdf", help="输出图片路径 (PDF/SVG/PNG)")
    args = parser.parse_args()

    apply_journal_style(journal=args.journal.split("-")[0])
    # 示意图适合 16:9 或 2:1 比例
    aspect = 0.55 if args.template == "workflow" else (0.7 if args.template == "pathway" else 0.5)
    figsize = get_figsize(args.journal, aspect_ratio=aspect)

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")  # 示意图关闭坐标轴

    if args.template == "workflow":
        draw_workflow_diagram(ax)
    elif args.template == "pathway":
        draw_pathway_diagram(ax)
    elif args.template == "apparatus":
        draw_apparatus_diagram(ax)

    save_figure(fig, args.output)
    plt.close(fig)


if __name__ == "__main__":
    main()
