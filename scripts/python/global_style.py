"""
global_style.py - 顶刊风格全局配置模块 (Global Publication Style Engine)

为 Matplotlib 提供符合 Nature, Science, Cell 等顶刊硬规范的全局样式参数、
尺寸计算、色板加载与矢量图导出工具。
"""

import json
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple, Union

# 路径常量
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
PALETTES_JSON_PATH = os.path.join(SKILL_ROOT, "assets", "palettes.json")

# 期刊尺寸定义 (单位: 毫米 mm)
JOURNAL_SPECS_MM = {
    "nature-single": {"width": 89.0, "max_height": 247.0},
    "nature-1.5": {"width": 120.0, "max_height": 247.0},
    "nature-double": {"width": 180.0, "max_height": 247.0},
    "science-single": {"width": 55.0, "max_height": 250.0},
    "science-1.5": {"width": 120.0, "max_height": 250.0},
    "science-double": {"width": 178.0, "max_height": 250.0},
    "cell-single": {"width": 85.0, "max_height": 235.0},
    "cell-1.5": {"width": 114.0, "max_height": 235.0},
    "cell-double": {"width": 174.0, "max_height": 235.0},
    "pnas-single": {"width": 86.0, "max_height": 225.0},
    "pnas-double": {"width": 178.0, "max_height": 225.0},
    "lancet-single": {"width": 85.0, "max_height": 240.0},
    "lancet-double": {"width": 175.0, "max_height": 240.0},
    "nejm-single": {"width": 86.0, "max_height": 230.0},
    "nejm-double": {"width": 178.0, "max_height": 230.0},
}


def mm_to_inches(mm: float) -> float:
    """将毫米转换为英寸"""
    return mm / 25.4


def load_palettes() -> Dict:
    """加载结构化色板库 assets/palettes.json"""
    if not os.path.exists(PALETTES_JSON_PATH):
        raise FileNotFoundError(f"Palettes file not found at: {PALETTES_JSON_PATH}")
    with open(PALETTES_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_palette(name: str, category: Optional[str] = None) -> List[str]:
    """
    根据名称检索色板色值列表。
    支持分类色、连续色、分歧色、荧光色与强调色。
    """
    data = load_palettes()
    if category and category in data:
        cat_data = data[category]
        if name in cat_data:
            entry = cat_data[name]
            return entry["colors"] if isinstance(entry, dict) and "colors" in entry else entry
    
    # 全局搜寻
    for cat_name, cat_dict in data.items():
        if isinstance(cat_dict, dict) and name in cat_dict:
            entry = cat_dict[name]
            if isinstance(entry, dict) and "colors" in entry:
                return entry["colors"]
            elif isinstance(entry, list):
                return entry
            elif isinstance(entry, dict) and "channels" in entry:
                return entry["colors"]
    
    # 强调色单独处理
    if "accent" in data and name in data["accent"]:
        val = data["accent"][name]
        return val if isinstance(val, list) else [val]
        
    raise KeyError(f"Palette '{name}' not found in {PALETTES_JSON_PATH}")


def get_figsize(journal_key: str = "nature-single", aspect_ratio: float = 0.75) -> Tuple[float, float]:
    """
    根据期刊预设和长宽比计算标准画布宽高 (英寸)。
    例如: nature-single -> 89mm 宽，高度按比例计算。
    """
    key = journal_key.lower().strip()
    if key not in JOURNAL_SPECS_MM:
        # 降级默认按 nature-single
        key = "nature-single"
    spec = JOURNAL_SPECS_MM[key]
    width_in = mm_to_inches(spec["width"])
    height_in = width_in * aspect_ratio
    max_height_in = mm_to_inches(spec["max_height"])
    if height_in > max_height_in:
        height_in = max_height_in
    return (round(width_in, 2), round(height_in, 2))


def apply_journal_style(
    journal: str = "nature",
    font_family: str = "Arial",
    base_font_size: float = 7.0,
    line_width: float = 0.8
):
    """
    配置全局 Matplotlib rcParams，严格适配 Nature / Science / Cell 标准。
    - 字体: Arial / Helvetica 无衬线
    - 字体嵌入: Type 42 (TrueType)，禁止 Type 3 栅格化文字
    - 线条: 0.8pt 坐标轴，刻度线外凸
    - 去除上右边框
    """
    mpl.rcParams.update({
        # 字体引擎与嵌入
        "font.family": "sans-serif",
        "font.sans-serif": [font_family, "Helvetica", "DejaVu Sans", "Arial", "sans-serif"],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "text.usetex": False,

        # 字号阶梯 (7pt 基准)
        "font.size": base_font_size,
        "axes.titlesize": base_font_size + 1.0,
        "axes.labelsize": base_font_size,
        "xtick.labelsize": base_font_size - 0.5,
        "ytick.labelsize": base_font_size - 0.5,
        "legend.fontsize": base_font_size - 0.5,
        "legend.title_fontsize": base_font_size,
        "figure.titlesize": base_font_size + 2.0,

        # 坐标轴与线宽
        "axes.linewidth": line_width,
        "axes.edgecolor": "#262626",
        "axes.labelcolor": "#262626",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,

        # 刻度线
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "xtick.minor.size": 2.0,
        "ytick.minor.size": 2.0,
        "xtick.major.width": line_width * 0.8,
        "ytick.major.width": line_width * 0.8,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.color": "#262626",
        "ytick.color": "#262626",

        # 折线与点
        "lines.linewidth": 1.2,
        "lines.markersize": 4.0,
        "patch.linewidth": line_width,

        # 图例
        "legend.frameon": False,
        "legend.borderpad": 0.2,
        "legend.handlelength": 1.0,
        "legend.handletextpad": 0.4,

        # 绘图底色与 DPI
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
        "savefig.facecolor": "#FFFFFF",
        "savefig.edgecolor": "#FFFFFF",
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,
    })


def despine(ax, top: bool = True, right: bool = True, left: bool = False, bottom: bool = False):
    """移除坐标轴指定外边框"""
    if top:
        ax.spines["top"].set_visible(False)
    if right:
        ax.spines["right"].set_visible(False)
    if left:
        ax.spines["left"].set_visible(False)
    if bottom:
        ax.spines["bottom"].set_visible(False)


def add_significance_bracket(
    ax,
    x1: float,
    x2: float,
    y: float,
    h: float,
    text: str = "***",
    text_offset: float = 0.005,
    lw: float = 0.8,
    color: str = "#262626"
):
    """
    在指定位置绘制统计学显著性横线与星号/p值标注。
    x1, x2: 两端 X 坐标
    y: 横线基础 Y 坐标
    h: 两端下折钩状高差
    text: 标注文字，如 '*', '**', '***', 'P = 0.003', 'ns'
    """
    # 绘制下折横线: (x1, y - h) -> (x1, y) -> (x2, y) -> (x2, y - h)
    ax.plot([x1, x1, x2, x2], [y - h, y, y, y - h], lw=lw, c=color, clip_on=False)
    # 标注文本居中
    ax.text((x1 + x2) * 0.5, y + text_offset, text, ha='center', va='bottom', color=color,
            fontsize=ax.yaxis.label.get_fontsize() - 0.5, clip_on=False)


def save_figure(fig, filepath: str, dpi: int = 600, transparent: bool = False):
    """
    保存高分辨率图表。支持 PDF (首选矢量), SVG, EPS, PNG, TIFF。
    自动保证目录存在，采用无损压缩与抗锯齿。
    """
    out_dir = os.path.dirname(filepath)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    
    ext = os.path.splitext(filepath)[1].lower()
    save_kwargs = {
        "dpi": dpi,
        "bbox_inches": "tight",
        "pad_inches": 0.05,
        "transparent": transparent
    }
    
    if ext in [".pdf", ".eps", ".svg"]:
        # 矢量格式保持无损矢量文字
        fig.savefig(filepath, format=ext[1:], **save_kwargs)
    elif ext in [".tif", ".tiff"]:
        # 高精度 TIFF
        fig.savefig(filepath, format="tiff", pil_kwargs={"compression": "tiff_lzw"}, **save_kwargs)
    else:
        fig.savefig(filepath, **save_kwargs)
    print(f"[OK] Figure successfully saved: {filepath} (Format: {ext.upper() or 'PNG'}, DPI: {dpi})")
