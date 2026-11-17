"""
test_sciplotting.py - 全场景科研绘图自动化回归测试套件 (Test Suite)
"""

import os
import sys
import tempfile
import unittest

# 注入 scripts/python 路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts", "python")
sys.path.insert(0, PYTHON_SCRIPTS_DIR)

from global_style import (
    load_palettes,
    get_palette,
    get_figsize,
    mm_to_inches,
    apply_journal_style,
)
from check_palette import audit_palette
from verify_render import audit_rendered_image
from compose_figure import build_demo_figure
from plot_stats import generate_synthetic_data
from plot_omics import generate_synthetic_omics_data
from plot_survival import generate_synthetic_survival_data, compute_km_survival
from plot_forest import generate_synthetic_meta_data
from plot_benchmark import generate_benchmark_data


class TestGlobalStyle(unittest.TestCase):
    """测试全局样式与色板加载"""

    def test_palettes_json_exists_and_valid(self):
        palettes = load_palettes()
        self.assertIn("categorical", palettes)
        self.assertIn("sequential", palettes)
        self.assertIn("diverging", palettes)
        self.assertIn("fluorescence", palettes)
        self.assertIn("accent", palettes)

    def test_get_palette_retrieval(self):
        colors = get_palette("nature_main_5")
        self.assertEqual(len(colors), 5)
        self.assertEqual(colors[0], "#4E79A7")

        okabe = get_palette("okabe_ito_8")
        self.assertEqual(len(okabe), 8)

    def test_journal_dimensions(self):
        w, h = get_figsize("nature-single", aspect_ratio=0.75)
        expected_w = round(mm_to_inches(89.0), 2)
        self.assertEqual(w, expected_w)
        self.assertGreater(h, 0.0)


class TestPaletteAuditor(unittest.TestCase):
    """测试色彩合规与色盲仿真诊断"""

    def test_nature_palette_compliance(self):
        colors = get_palette("nature_main_5")
        report = audit_palette(colors, "nature_main_5")
        self.assertTrue(report["overall_pass"])
        self.assertEqual(len(report["issues"]), 0)

    def test_okabe_ito_compliance(self):
        colors = get_palette("okabe_ito_8")
        report = audit_palette(colors, "okabe_ito_8")
        self.assertTrue(report["overall_pass"])
        self.assertEqual(len(report["issues"]), 0)

    def test_pure_red_green_rejection(self):
        bad_palette = ["#FF0000", "#00FF00"]
        report = audit_palette(bad_palette, "bad_rg")
        self.assertFalse(report["overall_pass"])
        self.assertGreater(len(report["issues"]), 0)


class TestPlotGenerators(unittest.TestCase):
    """测试各图表生成逻辑与合成数据集构造"""

    def test_stats_data_generation(self):
        df_bar = generate_synthetic_data("bar")
        self.assertFalse(df_bar.empty)
        self.assertIn("Group", df_bar.columns)
        self.assertIn("Value", df_bar.columns)

    def test_omics_data_generation(self):
        df_volcano = generate_synthetic_omics_data("volcano")
        self.assertFalse(df_volcano.empty)
        self.assertIn("log2FC", df_volcano.columns)

    def test_survival_math(self):
        df_surv = generate_synthetic_survival_data()
        self.assertFalse(df_surv.empty)
        times = df_surv["Time"].values
        events = df_surv["Status"].values
        ut, sp, ci_l, ci_u = compute_km_survival(times, events)
        self.assertEqual(sp[0], 1.0)
        self.assertTrue(all(0.0 <= p <= 1.0 for p in sp))

    def test_forest_data_generation(self):
        df_meta = generate_synthetic_meta_data()
        self.assertFalse(df_meta.empty)
        self.assertIn("HR", df_meta.columns)

    def test_benchmark_data_generation(self):
        df_pareto = generate_benchmark_data("pareto")
        self.assertFalse(df_pareto.empty)


class TestComposeAndVerify(unittest.TestCase):
    """测试多子图拼版与视觉质检"""

    def test_composer_and_qc(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_out = os.path.join(tmpdir, "test_fig.png")
            build_demo_figure(journal="nature-double", output_path=test_out)
            self.assertTrue(os.path.exists(test_out))

            qc_report = audit_rendered_image(test_out, journal_key="nature-double")
            self.assertIn(qc_report["status"], ["PASS", "WARN"])


if __name__ == "__main__":
    unittest.main()
