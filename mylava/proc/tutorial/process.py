from lava.magma.core.process.process import AbstractProcess
from lava.magma.core.process.variable import Var
from lava.magma.core.process.ports.ports import InPort, OutPort


# Define LIF, same as core library (for tutorial)
class LIF(AbstractProcess):
    """Leaky-Integrate-and-Fire (LIF) neural Process.

    LIF dynamics abstracts to:
    u[t] = u[t-1] * (1-du) + a_in                              # neuron current
    v[t] = v[t-1] * (1-dv) + u[t] + bias_mant * 2 ** bias_exp  # neuron voltage
    s_out = v[t] > vth                                         # spike if threshold is exceeded
    v[t] = 0                                                   # reset at spike

    Parameters
    ----------
    du: Inverse of decay time-constant for current decay.
    dv: Inverse of decay time-constant for voltage decay.
    bias_mant: Mantissa part of neuron bias.
    bias_exp: Exponent part of neuron bias, if needed. Mostly for fixed point
              implementations. Unnecessary for floating point
              implementations. If specified, bias = bias_mant * 2**bias_exp.
    vth: Neuron threshold voltage, exceeding which, the neuron will spike.
    """
    def __init__(self, **kwargs):
        super().__init__()
        shape = kwargs.get("shape", (1,))
        du = kwargs.pop("du", 0)
        dv = kwargs.pop("dv", 0)
        bias_mant = kwargs.pop("bias_mant", 0)
        bias_exp = kwargs.pop("bias_exp", 0)
        vth = kwargs.pop("vth", 10)

        self.shape = shape
        self.a_in = InPort(shape=shape)
        self.s_out = OutPort(shape=shape)
        self.u = Var(shape=shape, init=0)
        self.v = Var(shape=shape, init=0)
        self.du = Var(shape=(1,), init=du)
        self.dv = Var(shape=(1,), init=dv)
        self.bias_mant = Var(shape=shape, init=bias_mant)
        self.bias_exp = Var(shape=shape, init=bias_exp)
        self.vth = Var(shape=(1,), init=vth)
