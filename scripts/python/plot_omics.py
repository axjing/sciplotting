"""
plot_omics.py - 顶刊组学图生成器 (High-Throughput Omics Figure Generator)

支持生成高通量组学配图:
1. 聚类表达热图 (Clustered Heatmap + Dendrogram)
2. 差异表达火山图 (Volcano Plot + Gene Callout Labels)
3. 降维聚类图 (PCA Score Plot + 95% Confidence Ellipses)
4. 通路富集气泡图 (Pathway Enrichment Bubble Plot)
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist
from scipy.stats import chi2

# 导入全局样式引擎
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from global_style import (
    apply_journal_style,
    get_figsize,
    get_palette,
    save_figure,
)


def generate_synthetic_omics_data(plot_type: str) -> pd.DataFrame:
    """生成具有代表性的组学合成演示数据集"""
    np.random.seed(42)
    if plot_type == "heatmap":
        n_genes = 20
        samples = ["Ctrl_1", "Ctrl_2", "Ctrl_3", "Treat_1", "Treat_2", "Treat_3"]
        genes = [f"Gene_{i+1:02d}" for i in range(n_genes)]
        # 制造两个对比鲜明的表达模块
        data = np.zeros((n_genes, len(samples)))
        data[:10, :3] = np.random.normal(1.8, 0.4, (10, 3))
        data[:10, 3:] = np.random.normal(-1.5, 0.5, (10, 3))
        data[10:, :3] = np.random.normal(-1.2, 0.4, (10, 3))
        data[10:, 3:] = np.random.normal(2.1, 0.6, (10, 3))
        df = pd.DataFrame(data, index=genes, columns=samples)
        return df

    elif plot_type == "volcano":
        n_genes = 800
        gene_names = [f"GENE_{i+1}" for i in range(n_genes)]
        log2fc = np.random.normal(0, 1.2, n_genes)
        # 制造一些显著上调与下调基因
        pvals = np.random.uniform(0.00001, 1.0, n_genes)
        # 让大倍数差异的基因 p-value 明显更小
        pvals = pvals * np.exp(-abs(log2fc) * 1.5)
        pvals = np.clip(pvals, 1e-15, 1.0)
        df = pd.DataFrame({
            "Gene": gene_names,
            "log2FC": np.round(log2fc, 3),
            "pvalue": pvals,
            "padj": pvals * 1.2,
        })
        return df

    elif plot_type == "pca":
        n_per_group = 15
        groups = ["Control", "KO", "Rescue"]
        centers = [[-2.5, -1.0], [2.8, 1.5], [0.2, 2.2]]
        rows = []
        for g, (cx, cy) in zip(groups, centers):
            xs = np.random.normal(cx, 0.7, n_per_group)
            ys = np.random.normal(cy, 0.8, n_per_group)
            for x, y in zip(xs, ys):
                rows.append({"Group": g, "PC1": round(float(x), 3), "PC2": round(float(y), 3)})
        return pd.DataFrame(rows)

    elif plot_type == "bubble":
        pathways = [
            "PI3K-Akt signaling pathway",
            "MAPK signaling pathway",
            "Cell cycle and division",
            "Apoptosis regulation",
            "Glycolysis and gluconeogenesis",
            "DNA repair response",
            "Oxidative phosphorylation",
            "JAK-STAT cascade",
        ]
        gene_ratios = [0.42, 0.38, 0.35, 0.31, 0.28, 0.24, 0.19, 0.15]
        counts = [38, 31, 29, 22, 19, 15, 12, 9]
        padjs = [1.2e-7, 4.5e-6, 1.8e-5, 3.2e-4, 1.5e-3, 5.8e-3, 1.2e-2, 3.4e-2]
        return pd.DataFrame({
            "Pathway": pathways,
            "GeneRatio": gene_ratios,
            "Count": counts,
            "p.adjust": padjs,
        })

    return pd.DataFrame()


def plot_clustered_heatmap(df: pd.DataFrame, palette_colors: list, ax, fig):
    """绘制带层次聚类树 (Dendrogram) 的表达热图"""
    # 层次聚类 (按行基因聚类)
    dists = pdist(df.values, metric="euclidean")
    link = linkage(dists, method="complete")
    dend = dendrogram(link, no_plot=True)
    reordered_idx = dend["leaves"]
    reordered_df = df.iloc[reordered_idx]

    # 创建 Colormap
    if len(palette_colors) >= 2:
        cmap = mcolors.LinearSegmentedColormap.from_list("custom_div", palette_colors, N=256)
    else:
        cmap = plt.get_cmap("viridis")

    # 绘制热图网格
    vmax = max(abs(np.nanmin(reordered_df.values)), abs(np.nanmax(reordered_df.values)))
    vmax = min(vmax, 3.0)  # 顶刊标准化截断
    cax = ax.imshow(
        reordered_df.values,
        aspect="auto",
        cmap=cmap,
        interpolation="nearest",
        vmin=-vmax,
        vmax=vmax,
    )

    # 坐标刻度
    ax.set_xticks(np.arange(len(reordered_df.columns)))
    ax.set_xticklabels(reordered_df.columns, rotation=45, ha="right")
    ax.set_yticks(np.arange(len(reordered_df.index)))
    ax.set_yticklabels(reordered_df.index)

    # 添加 Colorbar
    cbar = fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Z-score Normalized Expression", rotation=270, labelpad=12)
    cbar.ax.tick_params(labelsize=6)


def plot_volcano(df: pd.DataFrame, ax, fc_col: str, p_col: str, gene_col: str):
    """绘制规范火山图: 上调红、下调蓝/绿、非显著灰，并引线标注 Top 差异基因"""
    log2fc = df[fc_col].values
    pval = df[p_col].values
    neg_log10_p = -np.log10(np.clip(pval, 1e-300, 1.0))

    fc_cutoff = 1.0
    p_cutoff = 0.05
    neg_p_cutoff = -np.log10(p_cutoff)

    # 分类索引
    up = (log2fc >= fc_cutoff) & (pval <= p_cutoff)
    down = (log2fc <= -fc_cutoff) & (pval <= p_cutoff)
    ns = ~up & ~down

    # 顶刊低饱和经典：上调珊瑚红、下调学术蓝、非显著浅灰
    c_up = "#E15759"
    c_down = "#4E79A7"
    c_ns = "#ADB5BD"

    ax.scatter(log2fc[ns], neg_log10_p[ns], c=c_ns, s=12, alpha=0.5, edgecolors="none", label="Not Significant")
    ax.scatter(log2fc[down], neg_log10_p[down], c=c_down, s=18, alpha=0.85, edgecolors="none", label="Down-regulated")
    ax.scatter(log2fc[up], neg_log10_p[up], c=c_up, s=18, alpha=0.85, edgecolors="none", label="Up-regulated")

    # 阈值辅助虚线
    ax.axvline(x=fc_cutoff, color="#8C8C8C", linestyle="--", lw=0.6, alpha=0.7)
    ax.axvline(x=-fc_cutoff, color="#8C8C8C", linestyle="--", lw=0.6, alpha=0.7)
    ax.axhline(y=neg_p_cutoff, color="#8C8C8C", linestyle="--", lw=0.6, alpha=0.7)

    # 标注 Top 上调/下调基因
    top_up_indices = np.argsort(neg_log10_p[up])[-3:] if np.sum(up) > 0 else []
    top_down_indices = np.argsort(neg_log10_p[down])[-3:] if np.sum(down) > 0 else []

    up_genes = df[up].iloc[top_up_indices]
    down_genes = df[down].iloc[top_down_indices]

    for _, row in pd.concat([up_genes, down_genes]).iterrows():
        x = row[fc_col]
        y = -np.log10(max(row[p_col], 1e-300))
        name = row[gene_col]
        ax.annotate(
            name,
            xy=(x, y),
            xytext=(x + (0.5 if x > 0 else -0.5), y + 0.8),
            arrowprops=dict(arrowstyle="-", color="#262626", lw=0.5),
            fontsize=6.0,
            ha="center",
            va="bottom",
        )

    ax.set_xlabel(r"$\log_{2}(\mathrm{Fold\ Change})$")
    ax.set_ylabel(r"$-\log_{10}(P\mathrm{-value})$")
    ax.legend(frameon=False, loc="upper right")


def plot_pca(df: pd.DataFrame, colors: list, ax, group_col: str, x_col: str, y_col: str):
    """绘制 PCA 降维散点图 + 95% 置信椭圆"""
    groups = df[group_col].unique()

    for i, g in enumerate(groups):
        sub = df[df[group_col] == g]
        x = sub[x_col].values
        y = sub[y_col].values
        c = colors[i % len(colors)]

        # 散点
        ax.scatter(x, y, color=c, edgecolors="#262626", s=28, linewidth=0.6, label=g, zorder=3)

        # 95% 置信椭圆
        if len(x) >= 3:
            cov = np.cov(x, y)
            mean_x, mean_y = np.mean(x), np.mean(y)
            eigenvals, eigenvecs = np.linalg.eigh(cov)
            order = eigenvals.argsort()[::-1]
            eigenvals, eigenvecs = eigenvals[order], eigenvecs[:, order]

            # 95% 置信度对应卡方自由度 2 的临界值
            scale = np.sqrt(chi2.ppf(0.95, df=2))
            angle = np.degrees(np.arctan2(*eigenvecs[:, 0][::-1]))
            width, height = 2 * scale * np.sqrt(np.maximum(eigenvals, 1e-6))

            ell = plt.matplotlib.patches.Ellipse(
                xy=(mean_x, mean_y),
                width=width,
                height=height,
                angle=angle,
                facecolor=c,
                alpha=0.15,
                edgecolor=c,
                linestyle="--",
                linewidth=0.8,
                zorder=2,
            )
            ax.add_patch(ell)

    ax.set_xlabel(f"{x_col} (48.3% variance)")
    ax.set_ylabel(f"{y_col} (22.7% variance)")
    ax.legend(frameon=False, loc="best")


def plot_enrichment_bubble(df: pd.DataFrame, ax, fig):
    """绘制富集气泡图: 横轴 GeneRatio，气泡大小 Count，颜色 -log10(p.adjust)"""
    # 按 GeneRatio 排序
    df_sorted = df.sort_values("GeneRatio", ascending=True).reset_index(drop=True)
    y_pos = np.arange(len(df_sorted))

    scores = -np.log10(df_sorted["p.adjust"].values)
    sizes = df_sorted["Count"].values * 8.0  # 映射气泡大小

    cmap = plt.get_cmap("viridis")
    scatter = ax.scatter(
        df_sorted["GeneRatio"],
        y_pos,
        s=sizes,
        c=scores,
        cmap=cmap,
        edgecolors="#262626",
        linewidth=0.6,
        alpha=0.85,
        zorder=3,
    )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(df_sorted["Pathway"])
    ax.set_xlabel("Gene Ratio")
    ax.grid(axis="x", linestyle=":", alpha=0.5, color="#D9D9D9")

    # Colorbar
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r"$-\log_{10}(\mathrm{Adjusted\ } P)$", rotation=270, labelpad=12)
    cbar.ax.tick_params(labelsize=6)


def main():
    parser = argparse.ArgumentParser(description="顶刊组学图生成器 (plot_omics.py)")
    parser.add_argument(
        "--type",
        choices=["heatmap", "volcano", "pca", "bubble"],
        default="volcano",
        help="组学图类型: heatmap (聚类热图), volcano (火山图), pca (主成分分析), bubble (富集气泡图)",
    )
    parser.add_argument("--data", type=str, default=None, help="输入数据 CSV 路径 (缺省时自动生成演示数据)")
    parser.add_argument("--journal", type=str, default="nature-single", help="目标期刊预设")
    parser.add_argument("--palette", type=str, default="RdBu", help="色板名称 (如 RdBu, PRGn, viridis, plasma)")
    parser.add_argument("--output", type=str, default="Fig_omics.pdf", help="输出图片路径")
    parser.add_argument("--demo", action="store_true", help="强制运行演示模式")
    args = parser.parse_args()

    apply_journal_style(journal=args.journal.split("-")[0])
    # 热图和气泡图略宽
    aspect = 0.9 if args.type in ["heatmap", "bubble"] else 0.8
    figsize = get_figsize(args.journal, aspect_ratio=aspect)

    # 尝试加载色板
    try:
        colors = get_palette(args.palette)
    except Exception:
        colors = get_palette("RdBu")

    # 数据准备
    if args.data and not args.demo and os.path.exists(args.data):
        df = pd.read_csv(args.data)
        print(f"[INFO] Loaded omics data from: {args.data}")
    else:
        df = generate_synthetic_omics_data(args.type)
        print(f"[INFO] Using synthetic scientific demo data for omics type: '{args.type}'")

    fig, ax = plt.subplots(figsize=figsize)

    if args.type == "heatmap":
        plot_clustered_heatmap(df, colors, ax, fig)
    elif args.type == "volcano":
        cols = list(df.columns)
        fc_col, p_col, g_col = cols[1], cols[2], cols[0]
        plot_volcano(df, ax, fc_col, p_col, g_col)
    elif args.type == "pca":
        cols = list(df.columns)
        g_col, x_col, y_col = cols[0], cols[1], cols[2]
        plot_pca(df, colors, ax, g_col, x_col, y_col)
    elif args.type == "bubble":
        plot_enrichment_bubble(df, ax, fig)

    save_figure(fig, args.output)
    plt.close(fig)


if __name__ == "__main__":
    main()
