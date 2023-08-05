from unittest import TestCase

import cavcalc as cc
import numpy as np


class InputUnitsTestCase(TestCase):
    def test_default1(self):
        out = cc.calculate(L=1, gs=0.9)
        given = out.constant_dependents()

        L, L_u = given[cc.Parameter.CAV_LENGTH]
        g, g_u = given[cc.Parameter.GFACTOR_SINGLE]

        self.assertEqual(L_u, "m")
        self.assertEqual(g_u, "")

        self.assertAlmostEqual(L, 1.0, delta=1e-14)
        self.assertAlmostEqual(g, 0.9, delta=1e-14)

    def test_default2(self):
        out = cc.calculate(R1=0.99, R2=0.999, gouy=1.3)
        given = out.constant_dependents()

        R1, R1_u = given[cc.Parameter.REFLECTIVITY_ITM]
        R2, R2_u = given[cc.Parameter.REFLECTIVITY_ETM]
        gouy, gouy_u = given[cc.Parameter.GOUY]

        self.assertEqual(R1_u, "")
        self.assertEqual(R2_u, "")
        self.assertEqual(gouy_u, "radians")

        self.assertAlmostEqual(R1, 0.99, delta=1e-14)
        self.assertAlmostEqual(R2, 0.999, delta=1e-14)
        self.assertAlmostEqual(gouy, 1.3, delta=1e-14)

    def test_length1(self):
        out = cc.calculate(L=(4, "km"), Rc1=1934, Rc2=2245)
        given = out.constant_dependents()

        L, L_u = given[cc.Parameter.CAV_LENGTH]
        Rc1, Rc1_u = given[cc.Parameter.ROC_ITM]
        Rc2, Rc2_u = given[cc.Parameter.ROC_ETM]

        self.assertEqual(L_u, "km")
        self.assertEqual(Rc1_u, "m")
        self.assertEqual(Rc2_u, "m")

        self.assertAlmostEqual(L, 4, delta=1e-14)
        self.assertAlmostEqual(Rc1, 1934, delta=1e-14)
        self.assertAlmostEqual(Rc2, 2245, delta=1e-14)

    def test_length2(self):
        lengths = np.linspace(1, 10, 100)
        out = cc.calculate(L=(lengths, "km"), gs=-0.9)
        given = out.constant_dependents()
        given.update(out.arraylike_dependents())

        L, L_u = given[cc.Parameter.CAV_LENGTH]
        gs, gs_u = given[cc.Parameter.GFACTOR_SINGLE]

        self.assertEqual(L_u, "km")
        self.assertEqual(gs_u, "")

        for l1, l2 in zip(lengths, L):
            self.assertAlmostEqual(l1, l2, delta=1e-14)

        self.assertAlmostEqual(gs, -0.9, delta=1e-14)
