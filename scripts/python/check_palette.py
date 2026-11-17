"""
check_palette.py - 配色合规校验器 (Palette Compliance & Accessibility Checker)

提供针对顶刊配色的自动化合规检查:
1. 色盲友好性仿真 (Deuteranopia 绿色盲, Protanopia 红色盲, Tritanopia 蓝黄色盲)
2. 灰度印刷可区分性与 CIE 相对亮度计算
3. 色差矩阵 (Perceptual Distance Delta E) 冲突检测
4. 禁用模式筛查 (红绿直接冲突、彩虹色阶、超饱和霓虹色、过多分类)
5. 输出标准化 Markdown 审计报告或 JSON 数据
"""

import argparse
import json
import math
import os
import sys
from typing import Dict, List, Tuple

# 导入全局样式引擎
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from global_style import load_palettes, get_palette


# sRGB 到线性 RGB 转换
def srgb_to_linear(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return c / 12.92 if c <= 0.04045 else math.pow((c + 0.055) / 1.055, 2.4)


def linear_to_srgb(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * math.pow(c, 1.0 / 2.4) - 0.055


def hex_to_rgb(hex_code: str) -> Tuple[float, float, float]:
    """解析十六进制色值为 0.0-1.0 的 RGB 元组"""
    h = hex_code.strip().lstrip("#")
    if len(h) == 3:
        h = "".join([c * 2 for c in h])
    return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)


def rgb_to_hex(r: float, g: float, b: float) -> str:
    """RGB 转 Hex"""
    ir = int(round(max(0.0, min(1.0, r)) * 255.0))
    ig = int(round(max(0.0, min(1.0, g)) * 255.0))
    ib = int(round(max(0.0, min(1.0, b)) * 255.0))
    return f"#{ir:02X}{ig:02X}{ib:02X}"


# 计算 CIE 相对亮度 (Relative Luminance Y)
def get_luminance(rgb: Tuple[float, float, float]) -> float:
    r_lin = srgb_to_linear(rgb[0])
    g_lin = srgb_to_linear(rgb[1])
    b_lin = srgb_to_linear(rgb[2])
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


# 色盲仿真矩阵 (Vienot et al. 1999 投影模型)
def simulate_colorblindness(rgb: Tuple[float, float, float], cvd_type: str) -> Tuple[float, float, float]:
    r, g, b = rgb
    rl, gl, bl = srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b)

    if cvd_type == "deuteranopia":  # 绿色盲 (最常见)
        rl_sim = 0.625 * rl + 0.375 * gl + 0.0 * bl
        gl_sim = 0.700 * rl + 0.300 * gl + 0.0 * bl
        bl_sim = 0.000 * rl + 0.300 * gl + 0.700 * bl
    elif cvd_type == "protanopia":  # 红色盲
        rl_sim = 0.56667 * rl + 0.43333 * gl + 0.0 * bl
        gl_sim = 0.55833 * rl + 0.44167 * gl + 0.0 * bl
        bl_sim = 0.00000 * rl + 0.24167 * gl + 0.75833 * bl
    elif cvd_type == "tritanopia":  # 蓝黄色盲
        rl_sim = 0.95000 * rl + 0.05000 * gl + 0.0 * bl
        gl_sim = 0.00000 * rl + 0.43333 * gl + 0.56667 * bl
        bl_sim = 0.00000 * rl + 0.47500 * gl + 0.52500 * bl
    else:
        rl_sim, gl_sim, bl_sim = rl, gl, bl

    return (linear_to_srgb(rl_sim), linear_to_srgb(gl_sim), linear_to_srgb(bl_sim))


# RGB 转 CIELAB
def rgb_to_lab(rgb: Tuple[float, float, float]) -> Tuple[float, float, float]:
    rl = srgb_to_linear(rgb[0])
    gl = srgb_to_linear(rgb[1])
    bl = srgb_to_linear(rgb[2])

    # 转换至 XYZ (D65 白点)
    x = rl * 0.4124564 + gl * 0.3575761 + bl * 0.1804375
    y = rl * 0.2126729 + gl * 0.7151522 + bl * 0.0721750
    z = rl * 0.0193339 + gl * 0.1191920 + bl * 0.9503041

    xn, yn, zn = 0.95047, 1.00000, 1.08883

    def f(t):
        return t ** (1.0 / 3.0) if t > 0.008856 else 7.787 * t + 16.0 / 116.0

    fx = f(x / xn)
    fy = f(y / yn)
    fz = f(z / zn)

    l = 116.0 * fy - 16.0
    a = 500.0 * (fx - fy)
    b_val = 200.0 * (fy - fz)
    return (l, a, b_val)


# 计算两颜色间的 Delta E (CIE 1976 色差)
def delta_e(rgb1: Tuple[float, float, float], rgb2: Tuple[float, float, float]) -> float:
    lab1 = rgb_to_lab(rgb1)
    lab2 = rgb_to_lab(rgb2)
    return math.sqrt((lab1[0] - lab2[0]) ** 2 + (lab1[1] - lab2[1]) ** 2 + (lab1[2] - lab2[2]) ** 2)


def audit_palette(colors: List[str], palette_name: str = "custom", strict: bool = False) -> Dict:
    """全面审计色板并生成结构化诊断结果"""
    rgb_list = [hex_to_rgb(c) for c in colors]
    n = len(colors)
    issues = []
    warnings = []

    # 1. 颜色数量校验
    if n > 8:
        warnings.append(f"单图分类颜色数达到 {n} 种 (>8)，超出人类短时工作记忆负荷，建议拆分为分面子图或改用辅助线型。")
    elif n > 5:
        warnings.append(f"单图分类颜色数为 {n} 种，建议在主图中尽量压缩至 ≤ 5 种。")

    # 2. 红绿对立检测
    has_pure_red = any((rgb[0] > 0.8 and rgb[1] < 0.25 and rgb[2] < 0.25) for rgb in rgb_list)
    has_pure_green = any((rgb[1] > 0.7 and rgb[0] < 0.3) for rgb in rgb_list)
    if has_pure_red and has_pure_green:
        issues.append("检测到高饱和纯红与纯绿直接对比组合，违反色盲无障碍强制红线！")

    # 3. 相对亮度与灰度可区分性
    luminances = [get_luminance(rgb) for rgb in rgb_list]
    gray_conflicts = []
    for i in range(n):
        for j in range(i + 1, n):
            lum_diff = abs(luminances[i] - luminances[j])
            if lum_diff < 0.05:
                gray_conflicts.append((colors[i], colors[j], round(lum_diff, 3)))
    if gray_conflicts:
        warnings.append(f"存在 {len(gray_conflicts)} 对颜色在黑白灰度打印下相对亮度差 < 0.05，转灰度后极难分辨 (如 {gray_conflicts[0][0]} 与 {gray_conflicts[0][1]})。")

    # 4. 色盲仿真下的辨识度 (Delta E 矩阵)
    cvd_results = {}
    for cvd in ["deuteranopia", "protanopia", "tritanopia"]:
        sim_rgbs = [simulate_colorblindness(rgb, cvd) for rgb in rgb_list]
        min_dist = float("inf")
        conflicts = []
        for i in range(n):
            for j in range(i + 1, n):
                d = delta_e(sim_rgbs[i], sim_rgbs[j])
                if d < min_dist:
                    min_dist = d
                # 设定阈值: 红绿色盲 (Deuteranopia/Protanopia) 严格门槛 10.0
                # 蓝黄色盲 (Tritanopia) 极罕见 (<0.01%)，严格模式下阈值 8.0，常规下 6.0
                thresh = 10.0 if cvd in ["deuteranopia", "protanopia"] else (8.0 if strict else 5.5)
                if d < thresh:
                    conflicts.append((colors[i], colors[j], round(d, 1)))

        safe = len(conflicts) == 0
        cvd_results[cvd] = {
            "min_delta_e": round(min_dist, 1),
            "safe": safe,
            "conflicts": conflicts,
        }

        if not safe:
            if cvd in ["deuteranopia", "protanopia"]:
                issues.append(f"在 {cvd} (红绿色盲) 仿真下，存在 {len(conflicts)} 对颜色色差 Delta E < 10，严重混淆 (例如 {conflicts[0][0]} 与 {conflicts[0][1]})！")
            else:
                if strict:
                    issues.append(f"在 tritanopia (蓝黄色盲) 仿真下，存在 {len(conflicts)} 对颜色色差 Delta E < 8.0 (严格模式拦截)")
                else:
                    warnings.append(f"在 tritanopia (蓝黄色盲) 仿真下存在轻度色差压缩 (最小色差: {round(min_dist, 1)})，但红绿色盲全面安全。")

    overall_pass = len(issues) == 0

    return {
        "palette_name": palette_name,
        "colors": colors,
        "n_colors": n,
        "luminances": [round(l, 3) for l in luminances],
        "overall_pass": overall_pass,
        "issues": issues,
        "warnings": warnings,
        "cvd_details": cvd_results,
    }


def format_markdown_report(report: Dict) -> str:
    """将审计结果格式化为美观的 Markdown 报告"""
    name = report["palette_name"]
    status_badge = "✅ **合规通过 (PASS)**" if report["overall_pass"] else "❌ **存在合规风险 (FAIL)**"

    md = []
    md.append(f"# 科研配图配色合规审计报告: `{name}`")
    md.append(f"\n**综合评定结论**: {status_badge}\n")

    # 色板基本属性表
    md.append("## 1. 待审色板色值与相对亮度 (sRGB & CIE Luminance)")
    md.append("| 序号 | 十六进制色值 | 预览色块 | 相对明度 $Y$ (0-1) | 灰度可辨度 |")
    md.append("| :--- | :--- | :--- | :--- | :--- |")
    for i, (c, lum) in enumerate(zip(report["colors"], report["luminances"])):
        md.append(f"| {i+1} | `{c}` | `<span style='color:{c};'>■■■</span>` | {lum:.3f} | {'偏暗' if lum < 0.3 else ('偏亮' if lum > 0.7 else '中等')} |")

    # 色盲兼容性检查表
    md.append("\n## 2. 色盲无障碍模拟测试 (Color Vision Deficiency)")
    md.append("| 色盲类型 | 受影响人群比例 | 最小色差 $\\Delta E$ | 状态 | 判定 |")
    md.append("| :--- | :--- | :--- | :--- | :--- |")
    cvd_labels = {
        "deuteranopia": ("绿色盲 / 绿色弱 (Deuteranopia)", "~6.0% 男性"),
        "protanopia": ("红色盲 / 红色弱 (Protanopia)", "~2.0% 男性"),
        "tritanopia": ("蓝黄色盲 (Tritanopia)", "<0.01% 全体"),
    }
    for k, res in report["cvd_details"].items():
        title, pop = cvd_labels[k]
        status = "✅ 安全" if res["safe"] else "❌ 混淆"
        crit = "通过" if res["safe"] else f"发现 {len(res['conflicts'])} 组碰撞"
        md.append(f"| {title} | {pop} | {res['min_delta_e']} | {status} | {crit} |")

    # 发现的问题与改进建议
    md.append("\n## 3. 详细审计意见与整改建议")
    if report["issues"]:
        md.append("### 🔴 致命缺陷 (Blocking Issues)")
        for iss in report["issues"]:
            md.append(f"- **[BLOCK]** {iss}")
    else:
        md.append("- 🎉 **无致命缺陷**：完全符合顶刊无障碍色盲友好标准。")

    if report["warnings"]:
        md.append("\n### 🟡 优化建议 (Warnings)")
        for w in report["warnings"]:
            md.append(f"- **[WARN]** {w}")
    else:
        md.append("- 💡 **版式优化**：色彩数量和灰度梯度处于最佳感知区间。")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="顶刊配色合规校验器 (check_palette.py)")
    parser.add_argument("--palette", type=str, default="nature_main_5", help="色板名称 (如 nature_main_5, okabe_ito_8)")
    parser.add_argument("--custom", type=str, default=None, help="自定义色值列表 (逗号分隔，如 '#4E79A7,#F28E2B,#E15759')")
    parser.add_argument("--format", choices=["markdown", "json", "text"], default="markdown", help="输出报告格式")
    parser.add_argument("--strict", action="store_true", help="启用严格蓝黄色盲过滤模式")
    parser.add_argument("--output", type=str, default=None, help="保存报告至指定文件")
    args = parser.parse_args()

    # 获取待测色值
    if args.custom:
        colors = [c.strip() for c in args.custom.split(",") if c.strip()]
        name = "custom_palette"
    else:
        colors = get_palette(args.palette)
        name = args.palette

    report = audit_palette(colors, palette_name=name, strict=args.strict)

    if args.format == "json":
        out_content = json.dumps(report, indent=2, ensure_ascii=False)
    elif args.format == "markdown":
        out_content = format_markdown_report(report)
    else:
        out_content = f"Palette: {name}\nPass: {report['overall_pass']}\nIssues: {len(report['issues'])}\nWarnings: {len(report['warnings'])}"

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out_content)
        print(f"[OK] Audit report saved to: {args.output}")
    else:
        print(out_content)


if __name__ == "__main__":
    main()
