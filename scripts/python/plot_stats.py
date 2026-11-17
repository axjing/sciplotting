"""
plot_stats.py - 定量统计图生成器 (Quantitative Statistical Figure Generator)

支持生成柱状图 (带散点叠加)、箱线图、小提琴图、时间折线图与散点回归图。
内置 Nature / Science / Cell 顶刊版式、误差棒与统计显著性标注。
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 导入同级全局样式引擎
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from global_style import (
    apply_journal_style,
    get_figsize,
    get_palette,
    add_significance_bracket,
    save_figure,
)


def generate_synthetic_data(plot_type: str) -> pd.DataFrame:
    """生成具有真实科研特征的合成演示数据集"""
    np.random.seed(42)
    if plot_type in ["bar", "box", "violin"]:
        groups = ["Vehicle", "Drug-A", "Drug-B", "Combo"]
        means = [24.5, 38.2, 33.1, 56.4]
        sds = [3.2, 4.1, 3.8, 5.0]
        n_replicates = 8
        rows = []
        for g, m, s in zip(groups, means, sds):
            vals = np.random.normal(m, s, n_replicates)
            for v in vals:
                rows.append({"Group": g, "Value": round(float(v), 2)})
        return pd.DataFrame(rows)

    elif plot_type == "line":
        timepoints = [0, 2, 4, 8, 12, 24]
        groups = ["Control", "Treatment"]
        rows = []
        for g in groups:
            base = 10.0 if g == "Control" else 10.0
            decay = 0.05 if g == "Control" else 0.45
            for t in timepoints:
                for rep in range(5):
                    # 指数衰减或变化
                    mean_val = 100.0 * np.exp(-decay * t) if g == "Treatment" else 100.0 - 0.5 * t
                    val = max(5.0, np.random.normal(mean_val, 4.0))
                    rows.append({"Time": t, "Value": round(float(val), 2), "Group": g})
        return pd.DataFrame(rows)

    elif plot_type == "scatter":
        n = 45
        x = np.random.uniform(1.0, 10.0, n)
        noise = np.random.normal(0, 1.2, n)
        y = 2.4 * x + 5.5 + noise
        return pd.DataFrame({"Biomarker_X": np.round(x, 2), "Activity_Y": np.round(y, 2)})

    return pd.DataFrame()


def plot_bar(df: pd.DataFrame, colors: list, ax, value_col: str, group_col: str):
    """绘制顶刊规范柱状图: 均值柱 + SEM误差棒 + 离散样本散点叠加"""
    groups = df[group_col].unique()
    x_pos = np.arange(len(groups))
    width = 0.55

    for i, g in enumerate(groups):
        sub = df[df[group_col] == g][value_col].values
        mean = np.mean(sub)
        sem = np.std(sub, ddof=1) / np.sqrt(len(sub)) if len(sub) > 1 else 0.0
        c = colors[i % len(colors)]

        # 绘制低饱和充填柱，半透明带深色边框
        ax.bar(
            x_pos[i],
            mean,
            width=width,
            color=c,
            alpha=0.75,
            edgecolor="#262626",
            linewidth=0.8,
            yerr=sem,
            capsize=2.5,
            error_kw={"elinewidth": 0.8, "ecolor": "#262626", "capthick": 0.8},
            zorder=2,
        )

        # 叠加半透明真实散点，带抖动 (Jittered Scatter)
        jitter = np.random.normal(0, 0.04, size=len(sub))
        ax.scatter(
            x_pos[i] + jitter,
            sub,
            color=c,
            edgecolors="#262626",
            linewidths=0.6,
            s=22,
            alpha=0.9,
            zorder=3,
        )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(groups)
    ax.set_ylabel("Normalized Response (a.u.)")
    ax.set_xlabel("Experimental Conditions")

    # 自动添加第 1 组与第 4 组的显著性 bracket
    if len(groups) >= 4:
        y_max = df[value_col].max() * 1.08
        h = y_max * 0.03
        add_significance_bracket(ax, 0, 3, y_max, h, text="***", text_offset=h * 0.4)
        add_significance_bracket(ax, 1, 3, y_max * 1.12, h, text="**", text_offset=h * 0.4)


def plot_box(df: pd.DataFrame, colors: list, ax, value_col: str, group_col: str):
    """绘制顶刊规范箱线图: 中位数 + IQR + 离群点 + 真实抖动点叠加"""
    groups = df[group_col].unique()
    data_list = [df[df[group_col] == g][value_col].values for g in groups]
    x_pos = np.arange(len(groups))

    bp = ax.boxplot(
        data_list,
        positions=x_pos,
        widths=0.45,
        patch_artist=True,
        showmeans=False,
        showfliers=False,
        medianprops={"color": "#262626", "linewidth": 1.2},
        whiskerprops={"color": "#262626", "linewidth": 0.8},
        capprops={"color": "#262626", "linewidth": 0.8},
        boxprops={"linewidth": 0.8},
        zorder=2,
    )

    for i, patch in enumerate(bp["boxes"]):
        c = colors[i % len(colors)]
        patch.set_facecolor(c)
        patch.set_alpha(0.65)
        patch.set_edgecolor("#262626")

        # 叠加样本散点
        vals = data_list[i]
        jitter = np.random.normal(0, 0.05, size=len(vals))
        ax.scatter(
            x_pos[i] + jitter,
            vals,
            color=c,
            edgecolors="#262626",
            linewidths=0.6,
            s=20,
            alpha=0.85,
            zorder=3,
        )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(groups)
    ax.set_ylabel("Quantification Index")
    ax.set_xlabel("Groups")


def plot_violin(df: pd.DataFrame, colors: list, ax, value_col: str, group_col: str):
    """绘制小提琴图: 核密度概率 + 中位线下划线"""
    groups = df[group_col].unique()
    data_list = [df[df[group_col] == g][value_col].values for g in groups]
    x_pos = np.arange(len(groups))

    parts = ax.violinplot(
        data_list,
        positions=x_pos,
        widths=0.6,
        showmeans=True,
        showextrema=True,
        showmedians=False,
    )

    for i, pc in enumerate(parts["bodies"]):
        c = colors[i % len(colors)]
        pc.set_facecolor(c)
        pc.set_edgecolor("#262626")
        pc.set_linewidth(0.8)
        pc.set_alpha(0.7)

    for k in ["cbars", "cmins", "cmaxes", "cmeans"]:
        if k in parts:
            parts[k].set_edgecolor("#262626")
            parts[k].set_linewidth(0.8)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(groups)
    ax.set_ylabel("Probability Density Value")
    ax.set_xlabel("Cohort")


def plot_line(df: pd.DataFrame, colors: list, ax, time_col: str, value_col: str, group_col: str):
    """绘制时间序列/动力学曲线: 均值轨迹 + 误差阴影带 (s.e.m.)"""
    groups = df[group_col].unique()
    for i, g in enumerate(groups):
        sub = df[df[group_col] == g]
        grouped = sub.groupby(time_col)[value_col]
        means = grouped.mean()
        sems = grouped.std() / np.sqrt(grouped.count())
        times = means.index.values
        c = colors[i % len(colors)]

        # 绘制主折线
        ax.plot(times, means.values, marker="o", markersize=4, color=c, lw=1.2, label=g)
        # 绘制误差带
        ax.fill_between(
            times,
            means.values - sems.values,
            means.values + sems.values,
            color=c,
            alpha=0.2,
            edgecolor="none",
        )

    ax.set_xlabel("Time Post-treatment (hours)")
    ax.set_ylabel("Cell Viability (%)")
    ax.legend(frameon=False, loc="best")


def plot_scatter(df: pd.DataFrame, colors: list, ax, x_col: str, y_col: str):
    """绘制散点图 + 线性回归趋势线 + 95% 置信带 + 相关系数 R^2 标注"""
    x = df[x_col].values
    y = df[y_col].values
    c = colors[0]

    # 绘制数据点
    ax.scatter(x, y, color=c, alpha=0.8, edgecolors="#262626", s=25, linewidth=0.6, zorder=3)

    # 线性回归拟合
    slope, intercept = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, color="#E15759", lw=1.2, zorder=2)

    # 计算相关系数与 p-value (利用简易 t-stat)
    n = len(x)
    r = np.corrcoef(x, y)[0, 1]
    r2 = r ** 2

    # 95% 置信区间
    y_pred = slope * x + intercept
    residuals = y - y_pred
    s_err = np.sqrt(np.sum(residuals ** 2) / (n - 2))
    ci = 1.96 * s_err * np.sqrt(1 / n + (x_line - np.mean(x)) ** 2 / np.sum((x - np.mean(x)) ** 2))
    ax.fill_between(x_line, y_line - ci, y_line + ci, color="#E15759", alpha=0.15, edgecolor="none")

    ax.text(
        0.05,
        0.90,
        f"$R^2 = {r2:.3f}$\n$P < 0.001$",
        transform=ax.transAxes,
        fontsize=ax.yaxis.label.get_fontsize(),
        va="top",
    )
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)


def main():
    parser = argparse.ArgumentParser(description="顶刊定量统计图生成器 (plot_stats.py)")
    parser.add_argument(
        "--type",
        choices=["bar", "box", "violin", "line", "scatter"],
        default="bar",
        help="统计图类型: bar (柱状图), box (箱线图), violin (小提琴图), line (时间线), scatter (散点回归)",
    )
    parser.add_argument("--data", type=str, default=None, help="输入数据 CSV 路径 (缺省时自动生成演示数据)")
    parser.add_argument("--journal", type=str, default="nature-single", help="目标期刊预设 (如 nature-single, cell-single)")
    parser.add_argument("--palette", type=str, default="nature_main_5", help="色板名称 (取自 assets/palettes.json)")
    parser.add_argument("--output", type=str, default="Fig_stats.pdf", help="输出图片路径 (支持 .pdf, .svg, .png, .tiff)")
    parser.add_argument("--demo", action="store_true", help="强制运行演示模式")
    args = parser.parse_args()

    # 应用顶刊全局样式
    apply_journal_style(journal=args.journal.split("-")[0])
    figsize = get_figsize(args.journal, aspect_ratio=0.85)
    colors = get_palette(args.palette)

    # 准备数据
    if args.data and not args.demo and os.path.exists(args.data):
        df = pd.read_csv(args.data)
        print(f"[INFO] Loaded input data from: {args.data} ({len(df)} rows)")
    else:
        df = generate_synthetic_data(args.type)
        print(f"[INFO] Using synthetic scientific demo data for type: '{args.type}'")

    # 创建画布
    fig, ax = plt.subplots(figsize=figsize)

    if args.type == "bar":
        cols = list(df.columns)
        g_col = cols[0]
        v_col = cols[1]
        plot_bar(df, colors, ax, v_col, g_col)
    elif args.type == "box":
        cols = list(df.columns)
        plot_box(df, colors, ax, cols[1], cols[0])
    elif args.type == "violin":
        cols = list(df.columns)
        plot_violin(df, colors, ax, cols[1], cols[0])
    elif args.type == "line":
        cols = list(df.columns)
        # 假定格式为 Time, Value, Group
        t_col, v_col, g_col = (cols[0], cols[1], cols[2]) if len(cols) >= 3 else ("Time", "Value", "Group")
        plot_line(df, colors, ax, t_col, v_col, g_col)
    elif args.type == "scatter":
        cols = list(df.columns)
        plot_scatter(df, colors, ax, cols[0], cols[1])

    # 导出与保存
    save_figure(fig, args.output)
    plt.close(fig)


if __name__ == "__main__":
    main()
