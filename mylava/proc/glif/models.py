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
    current_time_constant: np.ndarray = LavaPyType(float, float)

    # can be float if same for all neurons
    # alternatively, will broadcasting work? i.e. will array with shape (1,)
    # be interpreted as "apply same to all neurons"?
    capacitance: np.ndarray = LavaPyType(np.ndarray, float)
    resistance: np.ndarray = LavaPyType(np.ndarray, float)
    # TODO: multiple thresholds
    threshold: np.ndarray = LavaPyType(np.ndarray, float)
    reset: np.ndarray = LavaPyType(np.ndarray, float)
    resting: np.ndarray = LavaPyType(np.ndarray, float)
    # TODO: how to implement refractory period?
    #       "After a refractory period, δt, the state variables are updated
    #        with a linear dependence on the state before the spike"
    refractory_period: np.ndarray = LavaPyType(np.ndarray, float)
    # TODO: make these shape (n_1, ..., n_m, J) where n_i are the neuron shape
    #       (usually just n_1) and J is the number of post-spike currents
    #       (2 for now to match teeter et al)
    after_spike_currents: np.ndarray = LavaPyType(np.ndarray, float)
    last_AS_currents: np.ndarray = LavaPyType(np.ndarray, float)
    #       Paper actually uses 1/time_constant, so either need to specify
    #       inverse in argument to model or add 1/ in code. I'm leaning toward
    #       the former to avoid extra computations, but that might be unintuitive
    #       in terms of parameter specification.
    after_spike_time_constants: np.ndarray = LavaPyType(np.ndarray, float)
    after_spike_amplitude: np.ndarray = LavaPyType(np.ndarray, float)

    def run_spk(self):
        # This gets run during every spike phase of the simulation
        data_in = self.amplitude_in.recv()
        self._update_currents(data_in)
        self._update_voltage()
        # TODO: add other thresholds, they get updated too
        spikes_out = self.voltage >= self.threshold
        self._process_spikes(spikes_out)
        self.spikes_out.send(spikes_out)

    def _update_currents(self, data_in):
        # TODO: this is the Loihi 1 decay rule, what should glif be?
        self.current[...] *= (1 - self.current_time_constant)
        self.current[...] += data_in  # TODO: how is this weighted?
        self.last_AS_currents[...] = self.after_spike_currents
        self.after_spike_currents[...] *= (1 - self.after_spike_time_constants)
        # AD; related to what I said in the process: think about implementing the post-currents as states with separate dynamics. 
        # then things may be easier.

    def _update_voltage(self):
        dv = (self.current + self._after_spike_currents() - self._leak())
        self.voltage[...] = (1/self.capacitance)*dv

    def _leak(self):
        return (1/self.resistance)*(self.voltage - self.resting)

    def _after_spike_currents(self):
        # TODO: I'm assuming numpy operations aren't allowed on the Loihi 2
        #       version, so would have to do this with for loop(s) I guess?
        return np.sum(self.after_spike_currents, axis=1)

    def _process_spikes(self, spikes_out):
        self.voltage[spikes_out] = 0  # Reset voltage to 0
        # TODO:
        # f_j X I_j(t_-) + delta I_j
        # "f is a fraction of the current implemented after a spike; here it is
        # always set to 1. delta I_j is the amplitude of the spike-induced
        # currents"
        # but from supplementary:
        # "fj = exp (−k_j δt)", where delta_t is "spike cut length"
        # Setting to 1 for now
        self.after_spike_currents += (self.last_AS_current + self.after_spike_amplitude)
