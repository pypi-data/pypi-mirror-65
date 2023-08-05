# -*- coding: utf-8 -*-

__all__ = ["InvertLightCurveOp"]

import numpy as np
import theano
import theano.tensor as tt
from theano import gof

from .get_cl import GetClOp
from .limbdark import LimbDarkOp

get_cl = GetClOp()
limbdark = LimbDarkOp()


class InvertLightCurveOp(gof.Op):
    def __init__(self, maxiter=100, tol=1e-10):
        self.maxiter = int(maxiter)
        self.tol = float(tol)

        # Set up the problem using Theano ops
        c_norm = tt.dvector()
        b = tt.dscalar()
        delta = tt.dscalar()
        log_r = tt.dscalar()
        r = tt.exp(log_r)
        f, dfdcl, dfdb, dfdr = limbdark(c_norm, b, r, 1.0)
        value = delta + f

        # We'll need test vals to keep PyMC3 happy
        c_norm.tag.test_value = np.array([0.0])
        b.tag.test_value = 0.0
        delta.tag.test_value = 0.0
        r.tag.test_value = 0.0

        # Compile the objective function (this is all a little meta)
        self.func = theano.function(
            [log_r, c_norm, b, delta], [value, r * dfdr]
        )

        super(InvertLightCurveOp, self).__init__()

    def make_node(self, c_norm, b, delta):
        in_args = [
            tt.as_tensor_variable(c_norm),
            tt.as_tensor_variable(b),
            tt.as_tensor_variable(delta),
        ]
        out_args = [in_args[2].type()]
        return gof.Apply(self, in_args, out_args)

    def infer_shape(self, node, shapes):
        return (shapes[2],)

    def perform(self, node, inputs, outputs):
        c_norm, b, delta = inputs
        shape = np.shape(b)

        b = np.atleast_1d(b)
        delta = np.atleast_1d(delta)
        if b.ndim != 1 or b.shape != delta.shape:
            raise ValueError("dimension mismatch")

        r = np.zeros_like(b)
        for n in range(len(b)):
            args = (c_norm, b[n], delta[n])
            x = 0.5 * np.log(delta[n])
            for i in range(self.maxiter):
                f, fp = self.func(x, *args)
                x -= f / fp
                if f <= self.tol:
                    break
            if i == self.maxiter:
                print("didn't converge")
            r[n] = np.exp(x)

        outputs[0][0] = r.reshape(shape)

    def grad(self, inputs, gradients):
        c_norm, b, delta = inputs
        r = self(*inputs)
        br = gradients[0]

        f, dfdcl, dfdb, dfdr = limbdark(
            c_norm, b, r, tt.ones_like(tt.as_tensor_variable(b))
        )

        bcl = -tt.sum(dfdcl * (br / dfdr)[None, :], axis=1)
        bb = -dfdb * br / dfdr
        bdelta = -br / dfdr

        return bcl, bb, bdelta

    def R_op(self, inputs, eval_points):
        if eval_points[0] is None:
            return eval_points
        return self.grad(inputs, eval_points)
