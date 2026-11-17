"""
plot_forest.py - 顶刊 Meta 分析与风险比森林图生成器 (Meta-Analysis & Forest Plot Generator)

严格遵循 The Lancet / NEJM / JAMA / Cochrane 临床医学与流行病学规范:
1. 研究/亚组分行排布，点估计方块大小正比于样本权重 (Inverse-Variance Weights)
2. 95% 置信区间 (CI) 横向误差须线
3. 无效线 (Null Effect Line, HR/RR=1.0) 与效应倾向箭头 ("Favours Experimental" vs "Favours Control")
4. 右侧精确标注点估计与区间数值 (如 "0.68 [0.52, 0.89]")
5. 底部自动绘制合并效应量汇总棱形 (Summary Pooled Diamond)
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Dict, List, Optional

# 导入全局样式引擎
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from global_style import (
    apply_journal_style,
    get_figsize,
    get_palette,
    save_figure,
)


def generate_synthetic_meta_data() -> pd.DataFrame:
    """生成具有代表性的随机对照试验 (RCT) Meta 分析演示数据集"""
    studies = [
        "Smith et al. (2020)",
        "Chen et al. (2021)",
        "Rodriguez et al. (2022)",
        "Yamamoto et al. (2023)",
        "Müller et al. (2024)",
        "O'Connor et al. (2025)",
    ]
    hrs = [0.72, 0.58, 0.85, 0.62, 0.49, 0.77]
    ci_lowers = [0.51, 0.41, 0.68, 0.46, 0.33, 0.59]
    ci_uppers = [0.98, 0.82, 1.06, 0.84, 0.72, 1.01]
    weights = [18.5, 22.4, 25.1, 14.8, 8.2, 11.0]

    return pd.DataFrame({
        "Study": studies,
        "HR": hrs,
        "CI_Lower": ci_lowers,
        "CI_Upper": ci_uppers,
        "Weight": weights,
    })


def plot_forest(df: pd.DataFrame, study_col: str, hr_col: str, lower_col: str, upper_col: str, weight_col: str, output_path: str, journal: str = "nature-single", palette: str = "nature_main_5"):
    """绘制顶刊标准森林图"""
    figsize = get_figsize(journal, aspect_ratio=0.85)
    fig, ax = plt.subplots(figsize=figsize)

    colors = get_palette(palette)
    point_color = colors[0]  # 主点学术蓝
    summary_color = "#E15759"  # 汇总棱形珊瑚红

    n_studies = len(df)
    y_positions = np.arange(n_studies)[::-1]  # 自顶向下排列

    # 计算合并随机/固定效应量 (Weighted Average)
    weights = df[weight_col].values / 100.0
    pooled_hr = np.exp(np.sum(weights * np.log(df[hr_col].values)) / np.sum(weights))
    pooled_se = np.sqrt(1.0 / np.sum(1.0 / ((np.log(df[upper_col].values) - np.log(df[lower_col].values)) / 3.92) ** 2))
    pooled_lower = np.exp(np.log(pooled_hr) - 1.96 * pooled_se)
    pooled_upper = np.exp(np.log(pooled_hr) + 1.96 * pooled_se)

    # 1. 坐标轴尺度设定 (必须最先设置对数尺度与范围)
    ax.set_xscale("log")
    ax.set_xlim(0.25, 2.8)
    ax.set_xticks([0.3, 0.5, 0.7, 1.0, 1.5, 2.0])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    # 绘制无效假说垂直参考线 (Null Effect HR = 1.0)
    ax.axvline(1.0, color="#8C8C8C", linestyle="--", lw=0.8, zorder=1)

    # 2. 绘制各独立研究点与 95% 置信区间
    max_weight = df[weight_col].max()
    for y, (_, row) in zip(y_positions, df.iterrows()):
        hr = row[hr_col]
        low = row[lower_col]
        high = row[upper_col]
        w = row[weight_col]

        # 95% CI 须线
        ax.plot([low, high], [y, y], color="#262626", lw=1.0, zorder=2)

        # 方块大小正比于样本权重 (4~11 磅)
        box_size = 4.0 + (w / max_weight) * 6.5
        ax.plot(hr, y, marker="s", markersize=box_size, markerfacecolor=point_color, markeredgecolor="#262626", markeredgewidth=0.6, zorder=3)

        # 右侧数值标注
        stat_text = f"{hr:.2f} [{low:.2f}, {high:.2f}]"
        ax.text(1.70, y, stat_text, va="center", ha="left", fontsize=6.0, color="#262626")
        ax.text(2.65, y, f"{w:.1f}%", va="center", ha="right", fontsize=6.0, color="#6C757D")

    # 3. 底部绘制合并效应量棱形 (Summary Diamond)
    diamond_y = -1.2
    dh = 0.35
    diamond_pts = np.array([
        [pooled_lower, diamond_y],
        [pooled_hr, diamond_y + dh],
        [pooled_upper, diamond_y],
        [pooled_hr, diamond_y - dh],
    ])
    diamond = patches.Polygon(diamond_pts, closed=True, facecolor=summary_color, edgecolor="#262626", lw=0.8, zorder=4)
    ax.add_patch(diamond)

    # 汇总数值标注
    pooled_text = f"{pooled_hr:.2f} [{pooled_lower:.2f}, {pooled_upper:.2f}]"
    ax.text(1.70, diamond_y, pooled_text, va="center", ha="left", fontsize=6.0, fontweight="bold", color=summary_color)
    ax.text(2.65, diamond_y, "100.0%", va="center", ha="right", fontsize=6.0, fontweight="bold", color="#262626")

    # 4. Y 轴刻度与研究标签
    all_y = list(y_positions) + [diamond_y]
    all_labels = list(df[study_col].values) + ["Overall Effect (Pooled)"]
    ax.set_yticks(all_y)
    ax.set_yticklabels(all_labels)

    # 5. 表头文字 (右侧列)
    ax.text(1.70, n_studies + 0.3, "HR [95% CI]", fontsize=6.5, fontweight="bold", ha="left")
    ax.text(2.65, n_studies + 0.3, "Weight", fontsize=6.5, fontweight="bold", ha="right")

    # 6. X 轴与治疗偏向指示
    ax.set_xlabel("Hazard Ratio (log scale)")
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    # 底部偏向指示箭头
    ax.text(0.65, diamond_y - 1.2, r"$\longleftarrow$ Favours Treatment", fontsize=5.8, color="#59A14F", ha="center")
    ax.text(1.45, diamond_y - 1.2, r"Favours Control $\longrightarrow$", fontsize=5.8, color="#E15759", ha="center")

    ax.set_ylim(diamond_y - 1.8, n_studies + 0.8)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)

    save_figure(fig, output_path)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="顶刊 Meta 分析与风险比森林图生成器 (plot_forest.py)")
    parser.add_argument("--data", type=str, default=None, help="输入数据 CSV 路径")
    parser.add_argument("--study-col", type=str, default="Study", help="研究/试验名称列")
    parser.add_argument("--hr-col", type=str, default="HR", help="点估计效应量列名 (HR / RR / OR)")
    parser.add_argument("--lower-col", type=str, default="CI_Lower", help="置信区间下限列名")
    parser.add_argument("--upper-col", type=str, default="CI_Upper", help="置信区间上限列名")
    parser.add_argument("--weight-col", type=str, default="Weight", help="样本权重百分比列名")
    parser.add_argument("--journal", type=str, default="nature-single", help="期刊预设")
    parser.add_argument("--palette", type=str, default="nature_main_5", help="色板名称")
    parser.add_argument("--output", type=str, default="Fig_forest.pdf", help="导出文件路径")
    parser.add_argument("--demo", action="store_true", help="强制运行演示数据")
    args = parser.parse_args()

    apply_journal_style(journal=args.journal.split("-")[0])

    if args.data and not args.demo and os.path.exists(args.data):
        df = pd.read_csv(args.data)
        print(f"[INFO] Loaded meta-analysis data from {args.data} ({len(df)} trials)")
    else:
        df = generate_synthetic_meta_data()
        print("[INFO] Using synthetic clinical RCT meta-analysis demo data")

    plot_forest(df, args.study_col, args.hr_col, args.lower_col, args.upper_col, args.weight_col, args.output, journal=args.journal, palette=args.palette)


if __name__ == "__main__":
    main()
