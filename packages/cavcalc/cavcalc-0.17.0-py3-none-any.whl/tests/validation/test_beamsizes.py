import math
from unittest import TestCase

import cavcalc as cc
from cavcalc.utilities import CavCalcError
import numpy as np


class SymmetricTestCase(TestCase):
    ### Tests using ET-LF and HF values from design studies
    def test_ET_LF_reference_from_curvatures(self):
        """ET-LF design study reference parameters."""
        out_w0 = cc.calculate("w0", L=(10, "km"), Rc=5580, wl=(1550, "nm"))
        w0 = out_w0.get()
        self.assertEqual(w0.units, "cm")

        w0_ref = 2.898614178477818
        self.assertAlmostEqual(w0.v, w0_ref)

        out_w = cc.calculate("w", L=(10, "km"), Rc=5580, wl=(1550, "nm"))
        w = out_w.get()
        self.assertEqual(w.units, "cm")

        w_ref = 8.99070017493683
        self.assertAlmostEqual(w.v, w_ref)

    def test_ET_LF_reference_from_gsingles(self):
        """ET-LF design study reference parameters."""
        out_w0 = cc.calculate(
            "w0", L=(10, "km"), gs=-0.7921146953405018, wl=(1550, "nm")
        )
        w0 = out_w0.get()
        self.assertEqual(w0.units, "cm")

        w0_ref = 2.898614178477818
        self.assertAlmostEqual(w0.v, w0_ref)

        out_w = cc.calculate("w", L=(10, "km"), gs=-0.7921146953405018, wl=(1550, "nm"))
        w = out_w.get()
        self.assertEqual(w.units, "cm")

        w_ref = 8.99070017493683
        self.assertAlmostEqual(w.v, w_ref)

    def test_ET_LF_reference_from_rtgouy(self):
        """ET-LF design study reference parameters."""
        out_w0 = cc.calculate(
            "w0", L=(10, "km"), gouy=(284.7671490713067, "deg"), wl=(1550, "nm")
        )
        w0 = out_w0.get()
        self.assertEqual(w0.units, "cm")

        w0_ref = 2.898614178477818
        self.assertAlmostEqual(w0.v, w0_ref)

        out_w = cc.calculate(
            "w", L=(10, "km"), gouy=(284.7671490713067, "deg"), wl=(1550, "nm")
        )
        w = out_w.get()
        self.assertEqual(w.units, "cm")

        w_ref = 8.99070017493683
        self.assertAlmostEqual(w.v, w_ref)

    def test_ET_LF_reference_from_div(self):
        """ET-LF design study reference parameters."""
        out_w0 = cc.calculate(
            "w0", L=(10, "km"), div=(0.00097524570348501, "deg"), wl=(1550, "nm")
        )
        w0 = out_w0.get()
        self.assertEqual(w0.units, "cm")

        w0_ref = 2.898614178477818
        self.assertAlmostEqual(w0.v, w0_ref)

        out_w = cc.calculate(
            "w", L=(10, "km"), div=(0.00097524570348501, "deg"), wl=(1550, "nm")
        )
        w = out_w.get()
        self.assertEqual(w.units, "cm")

        w_ref = 8.99070017493683
        self.assertAlmostEqual(w.v, w_ref)

    def test_ET_HF_reference_from_curvatures(self):
        """ET-HF design study reference parameters."""
        out_w0 = cc.calculate("w0", L=(10, "km"), Rc=5070)
        w0 = out_w0.get()
        self.assertEqual(w0.units, "cm")

        w0_ref = 1.4155098269129294
        self.assertAlmostEqual(w0.v, w0_ref)

        out_w = cc.calculate("w", L=(10, "km"), Rc=5070)
        w = out_w.get()
        self.assertEqual(w.units, "cm")

        w_ref = 12.046693153452932
        self.assertAlmostEqual(w.v, w_ref)

    def test_ET_HF_reference_from_gsingles(self):
        """ET-HF design study reference parameters."""
        out_w0 = cc.calculate("w0", L=(10, "km"), gs=-0.9723865877712032)
        w0 = out_w0.get()
        self.assertEqual(w0.units, "cm")

        w0_ref = 1.4155098269129294
        self.assertAlmostEqual(w0.v, w0_ref)

        out_w = cc.calculate("w", L=(10, "km"), gs=-0.9723865877712032)
        w = out_w.get()
        self.assertEqual(w.units, "cm")

        w_ref = 12.046693153452932
        self.assertAlmostEqual(w.v, w_ref)

    def test_ET_HF_reference_from_rtgouy(self):
        """ET-HF design study reference parameters."""
        out_w0 = cc.calculate("w0", L=(10, "km"), gouy=(333.00818274722457, "deg"))
        w0 = out_w0.get()
        self.assertEqual(w0.units, "cm")

        w0_ref = 1.4155098269129294
        self.assertAlmostEqual(w0.v, w0_ref)

        out_w = cc.calculate("w", L=(10, "km"), gouy=(333.00818274722457, "deg"))
        w = out_w.get()
        self.assertEqual(w.units, "cm")

        w_ref = 12.046693153452932
        self.assertAlmostEqual(w.v, w_ref)

    def test_ET_HF_reference_from_div(self):
        """ET-HF design study reference parameters."""
        out_w0 = cc.calculate("w0", L=(10, "km"), div=(0.0013708864977292857, "deg"))
        w0 = out_w0.get()
        self.assertEqual(w0.units, "cm")

        w0_ref = 1.4155098269129294
        self.assertAlmostEqual(w0.v, w0_ref)

        out_w = cc.calculate("w", L=(10, "km"), div=(0.0013708864977292857, "deg"))
        w = out_w.get()
        self.assertEqual(w.units, "cm")

        w_ref = 12.046693153452932
        self.assertAlmostEqual(w.v, w_ref)

    ### Edge case tests - i.e. critically stable and unstable

    def test_w0_for_gsingle_minus_unity(self):
        """Waist size should be zero for gs = -1 (concentric cavity)."""
        out = cc.calculate("w0", L=1, gs=-1)
        w0 = out.get()
        self.assertEqual(w0.units, "cm")
        self.assertEqual(w0.v, 0.0)

    def test_w0_for_gsingle_plus_unity(self):
        """Division by zero error should occur for gs = +1  when computing w0."""
        self.assertRaises(CavCalcError, cc.calculate, "w0", **{"L": 1, "gs": 1})

    def test_w_for_gsingle_abs_unity(self):
        """Division by zero error should occur for gs = +/- 1  when computing w."""
        self.assertRaises(CavCalcError, cc.calculate, "w", **{"L": 1, "gs": -1})
        self.assertRaises(CavCalcError, cc.calculate, "w", **{"L": 1, "gs": 1})

    # TODO dual quadrant tests


class AsymmetricTestCase(TestCase):
    # TODO asymmetric cavity beam-size reference tests (e.g. use known values from aLIGO design)

    ### Edge case tests - i.e. critically stable and unstable

    def test_w0_for_g1g2_minus_unity(self):
        """Waist size should be zero for g1 = g2 = -1 (concentric cavity)."""
        out = cc.calculate("w0", L=1, g1=-1, g2=-1)
        w0 = out.get()
        self.assertEqual(w0.units, "cm")
        self.assertEqual(w0.v, 0.0)

    def test_w0_for_g1g2_unstable(self):
        out_upper_left_quad = cc.calculate("w0", L=1, g1=-0.9, g2=0.5)
        w0_u = out_upper_left_quad.get()
        self.assertEqual(w0_u.units, "cm")
        self.assertTrue(math.isnan(w0_u.v))

        out_lower_right_quad = cc.calculate("w0", L=1, g1=0.7, g2=-0.2)
        w0_l = out_lower_right_quad.get()
        self.assertEqual(w0_l.units, "cm")
        self.assertTrue(math.isnan(w0_l.v))
