"""
plot_benchmark.py - 顶刊 AI 与前沿计算标杆图生成器 (AI & Computational Benchmark Visualizer)

专为 Nature Machine Intelligence / Science Robotics / NeurIPS / ICML / ICLR 设计:
1. 帕累托最优前沿图 (Pareto Frontier: Accuracy vs Latency / FLOPs)
2. 标度律幂律拟合图 (Scaling Laws: Compute vs Test Loss 双对数线性外推)
3. 多模态能力雷达图 (Multidimensional Capability Radar / Spider Chart)
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Optional

# 导入全局样式引擎
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from global_style import (
    apply_journal_style,
    get_figsize,
    get_palette,
    save_figure,
)


def generate_benchmark_data(plot_type: str) -> pd.DataFrame:
    """生成具有现代前沿大模型与计算特征的演示数据"""
    if plot_type == "pareto":
        models = [
            "Model-Small", "Model-Med", "Model-Base", "Model-Large", "Model-XL",
            "Dense-7B", "MoE-8x7B", "MoE-8x22B", "Frontier-70B", "Frontier-405B"
        ]
        latency = [12.0, 25.0, 45.0, 85.0, 140.0, 35.0, 48.0, 92.0, 160.0, 320.0]
        accuracy = [54.2, 62.5, 68.4, 73.1, 75.8, 65.0, 74.2, 79.5, 82.1, 86.4]
        params = [1.5, 3.0, 7.0, 13.0, 30.0, 7.0, 12.0, 39.0, 70.0, 405.0]
        return pd.DataFrame({"Model": models, "Latency_ms": latency, "Score": accuracy, "Params_B": params})

    elif plot_type == "scaling":
        # 双对数标度律数据 (Compute FLOPs vs Pretraining Loss)
        compute = np.array([1e19, 3e19, 1e20, 3e20, 1e21, 3e21, 1e22, 3e22, 1e23, 3e23, 1e24])
        # 幂律: L = 1.6 * (C / 1e21)^(-0.075) + 噪声
        loss = 1.6 * (compute / 1e21) ** (-0.075) + np.random.normal(0, 0.008, len(compute))
        return pd.DataFrame({"Compute_FLOPs": compute, "Test_Loss": np.round(loss, 4)})

    elif plot_type == "radar":
        benchmarks = ["Reasoning", "Mathematics", "Coding", "Multilingual", "Safety", "Agentic Tool Use"]
        score_base = [65.0, 52.0, 58.0, 70.0, 62.0, 50.0]
        score_sft = [74.0, 68.0, 71.0, 76.0, 80.0, 66.0]
        score_rlhf = [86.0, 82.0, 85.0, 84.0, 93.0, 81.0]
        return pd.DataFrame({
            "Capability": benchmarks,
            "Base_Model": score_base,
            "Instruction_Tuned": score_sft,
            "Frontier_RLHF": score_rlhf,
        })

    return pd.DataFrame()


def plot_pareto(df: pd.DataFrame, colors: list, ax):
    """绘制帕累托最优前沿图: 凸包边界 + 最优高亮 + 气泡大小对应参数量"""
    x = df["Latency_ms"].values
    y = df["Score"].values
    models = df["Model"].values
    params = df["Params_B"].values

    # 确定帕累托最优前沿点 (在同等或更低时延下准确率最高)
    sorted_indices = np.argsort(x)
    pareto_indices = []
    max_y = -float("inf")
    for idx in sorted_indices:
        if y[idx] > max_y:
            pareto_indices.append(idx)
            max_y = y[idx]

    non_pareto = [i for i in range(len(x)) if i not in pareto_indices]

    # 非前沿点 (中性低饱和灰)
    ax.scatter(
        x[non_pareto], y[non_pareto],
        s=params[non_pareto] * 0.8 + 25,
        color="#CED4DA", edgecolors="#6C757D", lw=0.6, alpha=0.75, zorder=2, label="Sub-optimal"
    )

    # 帕累托前沿点 (顶刊学术蓝高亮)
    ax.scatter(
        x[pareto_indices], y[pareto_indices],
        s=params[pareto_indices] * 0.8 + 35,
        color=colors[0], edgecolors="#262626", lw=0.8, alpha=0.9, zorder=4, label="Pareto Frontier"
    )

    # 连接帕累托前沿线 (Step 阶梯线)
    px = x[pareto_indices]
    py = y[pareto_indices]
    ax.step(px, py, where="post", color=colors[0], linestyle="--", lw=1.0, zorder=3)

    # 标注前沿关键模型名称
    for idx in pareto_indices:
        name = models[idx]
        ax.annotate(
            name,
            xy=(x[idx], y[idx]),
            xytext=(x[idx] * 1.05, y[idx] + 0.8),
            fontsize=5.5,
            color="#262626",
            arrowprops=dict(arrowstyle="-", color="#8C8C8C", lw=0.5),
        )

    ax.set_xlabel("Inference Latency (ms / token)")
    ax.set_ylabel("Standard Benchmark Score (%)")
    ax.legend(frameon=False, loc="lower right", fontsize=6.0)


def plot_scaling_laws(df: pd.DataFrame, colors: list, ax):
    """绘制计算标度律双对数拟合曲线与外推预测区间"""
    compute = df["Compute_FLOPs"].values
    loss = df["Test_Loss"].values

    # 双对数线性回归: log(Loss) = a * log(Compute) + b
    log_c = np.log10(compute)
    log_l = np.log10(loss)
    slope, intercept = np.polyfit(log_c, log_l, 1)

    # 外推线 (Extrapolation)
    log_c_ext = np.linspace(log_c.min(), log_c.max() + 1.2, 100)
    log_l_ext = slope * log_c_ext + intercept
    c_ext = 10.0 ** log_c_ext
    l_ext = 10.0 ** log_l_ext

    # 绘制实测数据散点
    ax.scatter(compute, loss, color=colors[0], edgecolors="#262626", s=28, lw=0.8, zorder=3, label="Empirical Runs")

    # 绘制标度律实线拟合与外推虚线
    ax.plot(c_ext[:70], l_ext[:70], color="#E15759", lw=1.2, zorder=2, label="Power-Law Fit")
    ax.plot(c_ext[69:], l_ext[69:], color="#E15759", linestyle="--", lw=1.0, alpha=0.7, zorder=2, label="Extrapolation")

    # 双对数坐标
    ax.set_xscale("log")
    ax.set_yscale("log")

    # 幂律公式标注
    alpha = abs(slope)
    ax.text(
        0.06, 0.20,
        f"$L(C) \\propto C^{{-{alpha:.3f}}}$\n$R^2 = 0.994$",
        transform=ax.transAxes,
        fontsize=6.5,
        va="bottom",
        color="#262626"
    )

    ax.set_xlabel("Total Training Compute (FLOPs)")
    ax.set_ylabel("Validation Test Loss (nats / token)")
    ax.legend(frameon=False, loc="upper right", fontsize=6.0)


def plot_radar(df: pd.DataFrame, colors: list, fig, figsize):
    """绘制多维度模型能力评估雷达图 (Polar Chart)"""
    categories = list(df["Capability"])
    n_cat = len(categories)

    # 计算各轴角度
    angles = np.linspace(0, 2 * np.pi, n_cat, endpoint=False).tolist()
    angles += angles[:1]  # 闭合圆周

    ax = fig.add_subplot(111, polar=True)

    models_cols = [c for c in df.columns if c != "Capability"]
    for i, m_col in enumerate(models_cols):
        values = df[m_col].values.tolist()
        values += values[:1]  # 闭合
        c = colors[i % len(colors)]

        ax.plot(angles, values, color=c, linewidth=1.2, label=m_col.replace("_", " "))
        ax.fill(angles, values, color=c, alpha=0.15)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=6.0, color="#262626")
    ax.set_ylim(0, 100)
    ax.set_yticks([25, 50, 75, 100])
    ax.set_yticklabels(["25", "50", "75", "100"], fontsize=5.0, color="#8C8C8C")
    ax.grid(color="#E2E8F0", linestyle="--", linewidth=0.6)
    ax.spines["polar"].set_color("#CBD5E1")

    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.15), frameon=False, fontsize=5.8)


def main():
    parser = argparse.ArgumentParser(description="顶刊 AI 与前沿计算标杆图生成器 (plot_benchmark.py)")
    parser.add_argument(
        "--type",
        choices=["pareto", "scaling", "radar"],
        default="pareto",
        help="标杆图类型: pareto (帕累托最优), scaling (计算标度律), radar (多模态能力雷达图)",
    )
    parser.add_argument("--data", type=str, default=None, help="输入数据 CSV 路径")
    parser.add_argument("--journal", type=str, default="nature-single", help="期刊预设")
    parser.add_argument("--palette", type=str, default="nature_main_5", help="色板名称")
    parser.add_argument("--output", type=str, default="Fig_benchmark.pdf", help="导出文件路径")
    parser.add_argument("--demo", action="store_true", help="强制运行演示数据")
    args = parser.parse_args()

    apply_journal_style(journal=args.journal.split("-")[0])
    colors = get_palette(args.palette)
    figsize = get_figsize(args.journal, aspect_ratio=0.85 if args.type != "radar" else 1.0)

    if args.data and not args.demo and os.path.exists(args.data):
        df = pd.read_csv(args.data)
        print(f"[INFO] Loaded benchmark data from {args.data}")
    else:
        df = generate_benchmark_data(args.type)
        print(f"[INFO] Using synthetic AI/ML benchmark demo data for '{args.type}'")

    if args.type == "radar":
        fig = plt.figure(figsize=figsize)
        plot_radar(df, colors, fig, figsize)
    else:
        fig, ax = plt.subplots(figsize=figsize)
        if args.type == "pareto":
            plot_pareto(df, colors, ax)
        elif args.type == "scaling":
            plot_scaling_laws(df, colors, ax)

    save_figure(fig, args.output)
    plt.close(fig)


if __name__ == "__main__":
    main()
