"""
compose_figure.py - 顶刊多子图拼版编排器 (Multi-Panel Figure Composer)

专为 Nature / Science / Cell 多子图大版面 (Figure 1a-f) 设计。
解决多子图字体失调、坐标轴粗细不一、标签位置对不齐等顶刊排版通病。
支持:
1. 声明式网格布局 (GridSpec) 与跨行跨列 (Row/Col Span)
2. 顶刊标准化子图标号注入 (Nature 风格 'a'-'z', Science/Cell 风格 'A'-'Z')
3. 动态代码绘制与外部矢量/光栅图 (PDF, PNG, SVG) 混合编排
4. 像素级基线与边距对齐，导出 100% 比例保真的印刷通栏大图
"""

import argparse
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from typing import Callable, Dict, List, Optional, Tuple, Union

# 导入全局样式引擎
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from global_style import (
    apply_journal_style,
    get_figsize,
    save_figure,
)


class FigureComposer:
    """
    顶刊多子图拼版编排核心类
    """

    def __init__(
        self,
        journal: str = "nature-double",
        nrows: int = 2,
        ncols: int = 2,
        aspect_ratio: float = 0.85,
        wspace: float = 0.35,
        hspace: float = 0.38,
        width_ratios: Optional[List[float]] = None,
        height_ratios: Optional[List[float]] = None,
    ):
        """
        初始化拼版画布
        journal: 期刊预设 (nature-single, nature-double, science-double, cell-double 等)
        nrows, ncols: 网格行列数
        aspect_ratio: 整体画布高宽比
        wspace, hspace: 子图水平与垂直间距
        """
        self.journal = journal.lower()
        self.publisher = self.journal.split("-")[0]
        apply_journal_style(journal=self.publisher)

        self.figsize = get_figsize(self.journal, aspect_ratio=aspect_ratio)
        self.fig = plt.figure(figsize=self.figsize)
        self.gs = gridspec.GridSpec(
            nrows,
            ncols,
            figure=self.fig,
            wspace=wspace,
            hspace=hspace,
            width_ratios=width_ratios,
            height_ratios=height_ratios,
        )
        self.panels = []

    def get_panel_label(self, index: int) -> str:
        """根据目标期刊风格生成标准化子图序号"""
        if self.publisher in ["nature", "lancet"]:
            # Nature / Lancet: 小写加粗 a, b, c, d
            return chr(ord("a") + index)
        else:
            # Science / Cell / PNAS / NEJM: 大写加粗 A, B, C, D
            return chr(ord("A") + index)

    def add_subplot(
        self,
        row_slice: Union[int, slice, Tuple[int, int]],
        col_slice: Union[int, slice, Tuple[int, int]],
        plot_func: Optional[Callable] = None,
        label: Optional[str] = None,
        label_offset: Tuple[float, float] = (-0.14, 1.06),
        label_fontsize: float = 8.5,
        **kwargs,
    ):
        """
        添加一个基于代码动态绘制的子图
        row_slice, col_slice: 切片语法，支持网格合并 (例如 0, slice(0, 2))
        plot_func: 回调函数，签名必须接收 (ax, **kwargs)
        label: 自定义序号 (缺省时按添加顺序自动生成 a, b, c / A, B, C)
        """
        # 处理切片转换
        r = slice(row_slice, row_slice + 1) if isinstance(row_slice, int) else (
            slice(row_slice[0], row_slice[1]) if isinstance(row_slice, tuple) else row_slice
        )
        c = slice(col_slice, col_slice + 1) if isinstance(col_slice, int) else (
            slice(col_slice[0], col_slice[1]) if isinstance(col_slice, tuple) else col_slice
        )

        ax = self.fig.add_subplot(self.gs[r, c])

        # 确定序号文字
        if label is None:
            label = self.get_panel_label(len(self.panels))

        # 注入标准子图序号 (顶级无衬线粗体)
        ax.text(
            label_offset[0],
            label_offset[1],
            label,
            transform=ax.transAxes,
            fontsize=label_fontsize,
            fontweight="bold",
            va="top",
            ha="left",
            clip_on=False,
            color="#000000",
        )

        if plot_func:
            plot_func(ax, **kwargs)

        self.panels.append({"ax": ax, "label": label})
        return ax

    def add_image_panel(
        self,
        row_slice: Union[int, slice, Tuple[int, int]],
        col_slice: Union[int, slice, Tuple[int, int]],
        image_path: str,
        label: Optional[str] = None,
        label_offset: Tuple[float, float] = (-0.08, 1.05),
        label_fontsize: float = 8.5,
    ):
        """
        嵌入外部显微照片、电镜图或已有分析图
        """
        ax = self.add_subplot(
            row_slice,
            col_slice,
            label=label,
            label_offset=label_offset,
            label_fontsize=label_fontsize,
        )
        ax.axis("off")

        if os.path.exists(image_path):
            img = mpimg.imread(image_path)
            ax.imshow(img)
        else:
            # 文件不存在时绘制提示占位块
            ax.text(0.5, 0.5, f"[Image Placeholder:\n{os.path.basename(image_path)}]", ha="center", va="center", color="#8C8C8C", fontsize=7.0)
            ax.set_facecolor("#F8F9FA")

        return ax

    def save(self, filepath: str, dpi: int = 600):
        """导出出版级多子图拼版文件"""
        save_figure(self.fig, filepath, dpi=dpi)
        plt.close(self.fig)


# =========================================================================
# 内置 Demo 绘制函数 (展示统计图、组学图与时间序列曲线的协同拼版)
# =========================================================================

def _demo_bar_panel(ax):
    import numpy as np
    groups = ["Vehicle", "Drug-A", "Drug-B", "Synergy"]
    means = [24.5, 41.2, 36.8, 62.4]
    sems = [2.1, 3.4, 2.9, 4.2]
    colors = ["#4E79A7", "#76B7B2", "#F28E2B", "#E15759"]
    x = np.arange(len(groups))

    ax.bar(x, means, yerr=sems, capsize=2.5, color=colors, alpha=0.8, edgecolor="#262626", linewidth=0.8, error_kw={"elinewidth": 0.8, "ecolor": "#262626"})
    np.random.seed(42)
    for i, m in enumerate(means):
        pts = np.random.normal(m, 3.5, 6)
        ax.scatter(np.repeat(x[i], 6) + np.random.normal(0, 0.04, 6), pts, color=colors[i], edgecolors="#262626", s=18, linewidth=0.6, alpha=0.9, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(groups, rotation=20, ha="right")
    ax.set_ylabel("Tumor Burden (% of control)")
    # 显著性标注
    from global_style import add_significance_bracket
    add_significance_bracket(ax, 0, 3, 70.0, 2.5, text="***", text_offset=1.5)


def _demo_line_panel(ax):
    import numpy as np
    times = [0, 4, 8, 12, 24, 48]
    ctrl = [100.0, 98.2, 95.1, 93.4, 91.0, 89.2]
    treat = [100.0, 84.5, 62.1, 41.3, 22.8, 11.4]
    ax.plot(times, ctrl, marker="o", markersize=3.5, color="#4E79A7", lw=1.2, label="Vehicle")
    ax.plot(times, treat, marker="s", markersize=3.5, color="#E15759", lw=1.2, label="Drug-Combination")
    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Cell Viability (%)")
    ax.legend(frameon=False, loc="lower left", fontsize=6.0)


def _demo_volcano_panel(ax):
    import numpy as np
    np.random.seed(42)
    n = 350
    fc = np.random.normal(0, 1.3, n)
    pval = np.random.uniform(0.0001, 1.0, n) * np.exp(-abs(fc) * 1.2)
    pval = np.clip(pval, 1e-12, 1.0)
    neg_p = -np.log10(pval)

    up = (fc >= 1.0) & (pval <= 0.05)
    down = (fc <= -1.0) & (pval <= 0.05)
    ns = ~up & ~down

    ax.scatter(fc[ns], neg_p[ns], c="#ADB5BD", s=10, alpha=0.5, edgecolors="none")
    ax.scatter(fc[down], neg_p[down], c="#4E79A7", s=14, alpha=0.85, edgecolors="none")
    ax.scatter(fc[up], neg_p[up], c="#E15759", s=14, alpha=0.85, edgecolors="none")
    ax.axvline(1.0, color="#8C8C8C", linestyle="--", lw=0.6)
    ax.axvline(-1.0, color="#8C8C8C", linestyle="--", lw=0.6)
    ax.axhline(-np.log10(0.05), color="#8C8C8C", linestyle="--", lw=0.6)
    ax.set_xlabel(r"$\log_{2}(\mathrm{Fold\ Change})$")
    ax.set_ylabel(r"$-\log_{10}(P\mathrm{-value})$")


def _demo_schematic_panel(ax):
    """绘制流程与机制小插图"""
    import matplotlib.patches as patches
    ax.axis("off")
    # 绘制微流控与靶点概念图
    b1 = patches.FancyBboxPatch((0.05, 0.45), 0.38, 0.40, boxstyle="round,pad=0.05", facecolor="#F8F9FA", edgecolor="#4E79A7", lw=0.8)
    b2 = patches.FancyBboxPatch((0.57, 0.45), 0.38, 0.40, boxstyle="round,pad=0.05", facecolor="#FEE2E2", edgecolor="#E15759", lw=0.8)
    ax.add_patch(b1)
    ax.add_patch(b2)
    ax.text(0.24, 0.65, "Target\nIdentification", ha="center", va="center", fontsize=6.0, color="#262626")
    ax.text(0.76, 0.65, "PROTAC\nDegradation", ha="center", va="center", fontsize=6.0, color="#B91C1C", fontweight="bold")
    arrow = patches.FancyArrowPatch((0.44, 0.65), (0.56, 0.65), arrowstyle="-|>,head_length=4,head_width=2.5", color="#262626", lw=1.0)
    ax.add_patch(arrow)
    ax.text(0.50, 0.22, "Targeted Ubiquitination Cascade", ha="center", fontsize=5.8, color="#64748B", style="italic")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)


def build_demo_figure(journal: str = "nature-double", output_path: str = "Fig1_composite.pdf"):
    """构建四子图标准化主图 (Figure 1a-d) 示例"""
    composer = FigureComposer(journal=journal, nrows=2, ncols=2, aspect_ratio=0.72, wspace=0.32, hspace=0.35)

    # Panel a: 概念路线图
    composer.add_subplot(0, 0, plot_func=_demo_schematic_panel)

    # Panel b: 动力学折线图
    composer.add_subplot(0, 1, plot_func=_demo_line_panel)

    # Panel c: 定量统计柱状图 (带散点叠加)
    composer.add_subplot(1, 0, plot_func=_demo_bar_panel)

    # Panel d: 差异火山图
    composer.add_subplot(1, 1, plot_func=_demo_volcano_panel)

    composer.save(output_path)
    print(f"[OK] Master composite figure successfully built: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="顶刊多子图拼版编排器 (compose_figure.py)")
    parser.add_argument("--journal", type=str, default="nature-double", help="目标期刊预设 (如 nature-double, science-double, cell-double)")
    parser.add_argument("--output", type=str, default="Fig1_composite.pdf", help="导出文件路径 (支持 .pdf, .svg, .png, .tiff)")
    parser.add_argument("--demo", action="store_true", default=True, help="运行完整四子图拼版演示")
    args = parser.parse_args()

    build_demo_figure(journal=args.journal, output_path=args.output)


if __name__ == "__main__":
    main()
