from unittest import TestCase

import cavcalc as cc
from cavcalc.output import is_dual


class QuadrantsExistTestCase(TestCase):
    def test_w0_dual_for_gcav(self):
        out = cc.calculate("w0", L=(4, "km"), g=0.83)
        w0 = out.get()

        self.assertTrue(is_dual(w0))

        w0_lower, w0_upper = w0
        # they should not be equal
        self.assertNotAlmostEqual(w0_lower.v, w0_upper.v)

        # and w0_lower should be smaller than w0_upper
        self.assertTrue(w0_lower.v < w0_upper.v)
