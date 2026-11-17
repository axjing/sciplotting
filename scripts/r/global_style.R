# global_style.R - 顶刊 ggplot2 全局样式与色板引擎 (R Publication Style Engine)
# 原生适配 Nature / Science / Cell 标准，兼容 ggplot2 生态

suppressPackageStartupMessages({
  if (!requireNamespace("ggplot2", quietly = TRUE)) {
    warning("Package 'ggplot2' is required to use theme_nature().")
  }
})

# 内置核心色板默认定义 (当 jsonlite 未安装时无缝降级)
NATURE_PALETTES <- list(
  nature_main_5 = c("#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F"),
  okabe_ito_8   = c("#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000"),
  science_6     = c("#2B5C8F", "#D95F02", "#7570B3", "#E7298A", "#66A61E", "#E6AB02"),
  cell_6        = c("#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD", "#8C564B"),
  nejm_5        = c("#BC3C29", "#0072B5", "#E18727", "#20854E", "#6F99AD"),
  RdBu          = c("#67001F", "#B2182B", "#D6604D", "#F4A582", "#FDDBC7", "#FFFFFF", "#D1E5F0", "#92C5DE", "#4393C3", "#2166AC", "#053061"),
  PRGn          = c("#40004B", "#762A83", "#9970AB", "#C2A5CF", "#E7D4E8", "#FFFFFF", "#D9F0D3", "#A6DBA0", "#5AAE61", "#1B7837", "#00441B")
)

# 动态尝试读取 assets/palettes.json
load_palettes_json <- function() {
  json_path <- file.path(dirname(dirname(getwd())), "assets", "palettes.json")
  if (!file.exists(json_path)) {
    json_path <- file.path("assets", "palettes.json")
  }
  if (file.exists(json_path) && requireNamespace("jsonlite", quietly = TRUE)) {
    tryCatch({
      raw <- jsonlite::fromJSON(json_path)
      return(raw)
    }, error = function(e) NATURE_PALETTES)
  }
  return(NATURE_PALETTES)
}

#' 获取指定名称的学术色板
get_nature_palette <- function(palette_name = "nature_main_5") {
  if (palette_name %in% names(NATURE_PALETTES)) {
    return(NATURE_PALETTES[[palette_name]])
  }
  return(NATURE_PALETTES$nature_main_5)
}

#' Nature 顶刊经典无衬线风格主题
#' 
#' @param base_size 基础字号 (默认 7 pt, 符合 6-8 pt 顶刊标准)
#' @param base_family 字体族 (Arial / Helvetica)
theme_nature <- function(base_size = 7, base_family = "sans") {
  library(ggplot2)
  theme_classic(base_size = base_size, base_family = base_family) +
    theme(
      # 坐标轴与线宽控制 (0.35 mm 对应约 0.8 pt)
      axis.line = element_line(linewidth = 0.35, color = "#262626"),
      axis.ticks = element_line(linewidth = 0.35, color = "#262626"),
      axis.ticks.length = unit(3.0, "pt"),
      
      # 文字阶梯
      axis.text = element_text(color = "#262626", size = base_size - 0.5),
      axis.title = element_text(color = "#262626", size = base_size),
      
      # 图例规范
      legend.background = element_blank(),
      legend.key = element_blank(),
      legend.text = element_text(size = base_size - 0.5, color = "#262626"),
      legend.title = element_text(size = base_size, color = "#262626", face = "bold"),
      legend.margin = margin(0, 0, 0, 0),
      
      # 去除背景与多余网格
      panel.background = element_rect(fill = "#FFFFFF", color = NA),
      plot.background = element_rect(fill = "#FFFFFF", color = NA),
      panel.border = element_blank(),
      strip.background = element_blank(),
      strip.text = element_text(size = base_size, face = "bold", color = "#262626"),
      
      # 标题与边距
      plot.title = element_text(size = base_size + 1.0, face = "bold", color = "#262626", hjust = 0),
      plot.margin = margin(4, 4, 4, 4, "pt")
    )
}

#' Cell 风格活跃主题
theme_cell <- function(base_size = 7, base_family = "sans") {
  theme_nature(base_size = base_size, base_family = base_family)
}

#' Science 风格严谨主题
theme_science <- function(base_size = 7, base_family = "sans") {
  theme_nature(base_size = base_size, base_family = base_family)
}

#' ggplot2 离散色彩标度 (Color)
scale_color_nature <- function(palette = "nature_main_5", ...) {
  library(ggplot2)
  colors <- get_nature_palette(palette)
  discrete_scale("colour", "nature", manual_pal(values = colors), ...)
}

#' ggplot2 离散填充标度 (Fill)
scale_fill_nature <- function(palette = "nature_main_5", ...) {
  library(ggplot2)
  colors <- get_nature_palette(palette)
  discrete_scale("fill", "nature", manual_pal(values = colors), ...)
}

#' 顶刊尺寸标准导出助手
#' 
#' @param plot ggplot2 图形对象
#' @param filename 导出文件名 (支持 .pdf, .svg, .png, .tiff)
#' @param journal 期刊尺寸预设 ("nature-single", "nature-double", "science-single", etc.)
#' @param aspect_ratio 高宽比 (默认 0.75)
#' @param dpi 分辨率 (默认 600)
save_journal_figure <- function(plot, filename, journal = "nature-single", aspect_ratio = 0.75, dpi = 600) {
  library(ggplot2)
  
  # 毫米宽度映射表
  widths_mm <- list(
    "nature-single"  = 89.0,
    "nature-double"  = 180.0,
    "science-single" = 55.0,
    "science-double" = 178.0,
    "cell-single"    = 85.0,
    "cell-double"    = 174.0,
    "pnas-single"    = 86.0,
    "pnas-double"    = 178.0
  )
  
  w_mm <- if (journal %in% names(widths_mm)) widths_mm[[journal]] else 89.0
  h_mm <- w_mm * aspect_ratio
  
  ggsave(
    filename = filename,
    plot = plot,
    width = w_mm,
    height = h_mm,
    units = "mm",
    dpi = dpi,
    device = if (grepl("\\.pdf$", filename)) cairo_pdf else NULL
  )
  message(sprintf("[OK] R ggplot2 figure saved: %s (%s, %.1f x %.1f mm, DPI: %d)", filename, journal, w_mm, h_mm, dpi))
}
