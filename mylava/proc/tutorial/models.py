import numpy as np
# implement LIF process, require CPU
from lava.magma.core.decorator import implements, requires, tag
from lava.magma.core.resources import CPU
# Synchronization protocol (how to manage parallel processes)
from lava.magma.core.sync.protocols.loihi_protocol import LoihiProtocol
# base class for leaf processes that use Loihi protocol
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.model.py.ports import PyInPort, PyOutPort
# data type
from lava.magma.core.model.py.type import LavaPyType

# NOTE: relative import will break the part of Lava that searches for
#       process implementations, have to use full import path.
from mylava.proc.tutorial.process import LIF


# Define process model for tutorial LIF
@implements(proc=LIF, protocol=LoihiProtocol)
@requires(CPU)
@tag('floating_pt')  # precision    
class PyLifModel1(PyLoihiProcessModel):
    # These must match up to the ones defined in LIF process
    a_in: PyInPort = LavaPyType(PyInPort.VEC_DENSE, float)
    s_out: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, bool, precision=1)
    u: np.ndarray = LavaPyType(np.ndarray, float)
    v: np.ndarray = LavaPyType(np.ndarray, float)
    bias_mant: np.ndarray = LavaPyType(np.ndarray, float)
    bias_exp: np.ndarray = LavaPyType(np.ndarray, float)
    du: float = LavaPyType(float, float)
    dv: float = LavaPyType(float, float)
    vth: float = LavaPyType(float, float)

    def run_spk(self):
        # Specific to Loihi protocol.
        # recv() and send() handle incoming and outgoing data.  
        a_in_data = self.a_in.recv()
        self.u[:] = self.u * (1 - self.du)
        self.u[:] += a_in_data
        bias = self.bias_mant * (2 ** self.bias_exp)
        self.v[:] = self.v * (1 - self.dv) + self.u + bias
        s_out = self.v >= self.vth
        self.v[s_out] = 0  # Reset voltage to 0
        self.s_out.send(s_out)
