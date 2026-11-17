# demo_plot.R - R / ggplot2 顶刊科研图生成演示
# 展示柱状散点叠加图与箱线图的标准绘制

source(file.path(dirname(sys.frame(1)$ofile), "global_style.R"))

suppressPackageStartupMessages({
  library(ggplot2)
})

# 1. 构造具有真实生物学特征的合成数据
set.seed(42)
groups <- c("Vehicle", "Drug-A", "Drug-B", "Combination")
n_rep <- 10

df_demo <- data.frame(
  Group = factor(rep(groups, each = n_rep), levels = groups),
  Response = c(
    rnorm(n_rep, mean = 25.0, sd = 3.5),
    rnorm(n_rep, mean = 42.0, sd = 4.2),
    rnorm(n_rep, mean = 38.5, sd = 3.8),
    rnorm(n_rep, mean = 65.0, sd = 5.0)
  )
)

# 2. 绘制符合顶刊规范的柱状图 + 误差棒 + 散点抖动
p_bar <- ggplot(df_demo, aes(x = Group, y = Response, fill = Group)) +
  # 均值柱 (带半透明与细黑边)
  stat_summary(fun = mean, geom = "bar", width = 0.55, alpha = 0.75, color = "#262626", linewidth = 0.35) +
  # SEM 误差棒
  stat_summary(fun.data = mean_se, geom = "errorbar", width = 0.2, color = "#262626", linewidth = 0.35) +
  # 叠加真实样本散点 (Jittered Scatter)
  geom_jitter(shape = 21, size = 1.8, stroke = 0.3, alpha = 0.85, width = 0.12) +
  # 顶刊配色与主题注入
  scale_fill_nature("nature_main_5") +
  theme_nature(base_size = 7) +
  theme(legend.position = "none") +
  labs(
    x = "Experimental Conditions",
    y = "Relative Normalized Signal (a.u.)",
    title = "Target Inhibition in Patient-Derived Xenograft"
  )

# 3. 导出为 Nature 单栏高精度矢量 PDF
# save_journal_figure(p_bar, "Fig_R_bar.pdf", journal = "nature-single", aspect_ratio = 0.8)
message("[INFO] Demo ggplot2 code ready. Run in your R environment.")
