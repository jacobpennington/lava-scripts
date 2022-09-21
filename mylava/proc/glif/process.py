from lava.magma.core.process.process import AbstractProcess
from lava.magma.core.process.variable import Var
from lava.magma.core.process.ports.ports import InPort, OutPort


class GLIF(AbstractProcess):

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
