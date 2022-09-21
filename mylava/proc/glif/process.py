from lava.magma.core.process.process import AbstractProcess
from lava.magma.core.process.variable import Var
from lava.magma.core.process.ports.ports import InPort, OutPort


class GLIF(AbstractProcess):
    
    def __init__(self, shape=(1,), one_time_constant=True, initial_current=0.0,
                 initial_voltage=0.0, current_time_constant=0.0, capacitance=0.0,
                 resistance=0.0, threshold=0.0, reset=0.0, resting=0.0,
                 refractory_period=0.0, n_AS_currents=2, initial_AS_currents=0.0,
                 after_spike_time_constants=0.0, after_spike_amplitude=0.0,
                 **kwargs):
        super().__init__()
        # TODO: Lava tutorials use a "blah = kwargs.pop('blah', default)"
        #       scheme. Is this actually important, or is using standard
        #       keyword arguments like this acceptable?
        # TODO: reasonable default values
        as_shape = shape + (n_AS_currents,)
        if one_time_constant:
            tc_shape = (1,)
            as_tc_shape = (1, n_AS_currents)
        else:
            tc_shape = shape
            as_tc_shape = as_shape

        self.amplitude_in = InPort(shape=shape)
        self.spikes_out = OutPort(shape=shape)
        self.current = Var(shape=shape, init=initial_current)  
        self.voltage = Var(shape=shape, init=initial_voltage)
        self.current_time_constant = Var(
            shape=tc_shape, init=current_time_constant
            )
        # TODO: option to have these be shape (1,) similar to time constants?
        self.capacitance = Var(shape=shape, init=capacitance)
        self.resistance = Var(shape=shape, init=resistance)
        self.threshold = Var(shape=shape, init=threshold)
        self.reset = Var(shape=shape, init=reset)
        self.resting = Var(shape=shape, init=resting)
        self.refractory_period = Var(shape=shape, init=refractory_period)

        self.after_spike_currents = Var(shape=as_shape, init=initial_AS_currents)
        self.last_AS_currents = Var(shape=as_shape, init=0.0)
        self.after_spike_time_constants = Var(
            shape=as_tc_shape, init=after_spike_time_constants
            )
        self.after_spike_amplitude = Var(shape=as_shape, init=after_spike_amplitude)


    def print_variables(self):
        """Prints all variables of a GLIF process and their values."""
        # TODO: Currently copied from the tutorial LIF, will need to be updated
        #       to match the new variable names. Just putting this here to remind
        #       myself to include a similar method for debugging/testing.
        sp = 3 * "  "
        print("Variables of the LIF:")
        print(sp + "u:    {}".format(str(self.u.get())))
        print(sp + "v:    {}".format(str(self.v.get())))
        print(sp + "du:   {}".format(str(self.du.get())))
        print(sp + "dv:   {}".format(str(self.dv.get())))
        print(sp + "bias: {}".format(str(self.bias.get())))
        print(sp + "vth:  {}".format(str(self.vth.get())))
