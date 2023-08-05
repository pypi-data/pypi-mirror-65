# -*- coding: utf-8 -*-

import numpy as np
import theano
import theano.tensor as tt
from theano.tests import unittest_tools as utt

from ...light_curves import LimbDarkLightCurve
from .limbdark import LimbDarkOp
from .invert_light_curve import InvertLightCurveOp


class TestInvertLightCurve(utt.InferShapeTester):
    def setUp(self):
        super(TestInvertLightCurve, self).setUp()
        self.op_class = InvertLightCurveOp
        self.op = InvertLightCurveOp()

    def get_args(self):
        c = tt.vector()
        b = tt.vector()
        delta = tt.vector()
        f = theano.function([c, b, delta], self.op(c, b, delta))

        c_val = LimbDarkLightCurve([0.3, 0.1]).c_norm.eval()
        b_val = np.linspace(-1.0, 1.0, 100)
        ror_val = np.linspace(0.5, 0.01, len(b_val))
        delta_val = -LimbDarkOp()(c_val, b_val, ror_val, np.ones_like(b_val))[
            0
        ].eval()

        return f, [c, b, delta], [c_val, b_val, delta_val], ror_val

    def test_basic(self):
        f, _, in_args, expect = self.get_args()
        out = f(*in_args)
        print(in_args)
        print(out)
        print(expect)

        import matplotlib.pyplot as plt

        plt.plot(in_args[1], out)
        plt.plot(in_args[1], expect)
        plt.plot(in_args[1], np.sqrt(in_args[2]))
        plt.savefig("face.pdf")

        utt.assert_allclose(out, expect)

    def test_infer_shape(self):
        f, args, arg_vals, _ = self.get_args()
        self._compile_and_check(args, self.op(*args), arg_vals, self.op_class)

    def test_grad(self):
        _, _, in_args, _ = self.get_args()
        # func = lambda *args: self.op(*args)  # NOQA
        utt.verify_grad(self.op, in_args)
