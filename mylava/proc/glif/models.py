import numpy as np
from lava.magma.core.decorator import implements, requires, tag
from lava.magma.core.resources import CPU
from lava.magma.core.sync.protocols.loihi_protocol import LoihiProtocol
from lava.magma.core.model.py.model import PyLoihiProcessModel
from lava.magma.core.model.py.ports import PyInPort, PyOutPort
from lava.magma.core.model.py.type import LavaPyType

from mylava.proc.glif.process import GLIF


# WIP

@implements(proc=GLIF, protocol=LoihiProtocol)
@requires(CPU)
@tag('floating_pt')  # precision    
class PyGlifModelCPU(PyLoihiProcessModel):

    amplitude_in: PyInPort = LavaPyType(PyInPort.VEC_DENSE, float)
    spikes_out: PyOutPort = LavaPyType(PyOutPort.VEC_DENSE, bool, precision=1)
    current: np.ndarray = LavaPyType(np.ndarray, float)
    voltage: np.ndarray = LavaPyType(np.ndarray, float)
    # v_time_constant: np.ndarray = LavaPyType(float, float)
    u_time_constant: np.ndarray = LavaPyType(float, float)

    # can be float if same for all neurons
    capacitance: np.ndarray = LavaPyType(np.ndarray, float)
    resistance: np.ndarray = LavaPyType(np.ndarray, float)
    # TODO: multiple thresholds
    threshold: np.ndarray = LavaPyType(float, float)
    reset: np.ndarray = LavaPyType(float, float)
    resting: np.ndarray = LavaPyType(float, float)
    after_spike_currents: np.ndarray = LavaPyType(float, float)


    def run_spk(self):
        data_in = self.amplitude_in.recv()

        # TODO: this is the Loihi 1 decay rule, what should glif be?
        self.current[:] = self.current * (1 - self.u_time_constant)
        self.current[:] += data_in  # TODO: how is this weighted?
        self.voltage[:] = self._new_voltage()

        # TODO: add other thresholds, they get updated too
        spikes_out = self.voltage >= self.threshold
        self.voltage[spikes_out] = 0  # Reset voltage to 0
        self.spikes_out.send(spikes_out)

    def _new_voltage(self):
        dv = (self.current + self._after_spike() - self._leak())
        return (1/self.capacitance)*dv

    def _leak(self):
        return (1/self.resistance)*(self.voltage - self.resting)

    def _after_spike(self):
        # TODO: need to update them first
        return sum(self.after_spike_currents)
