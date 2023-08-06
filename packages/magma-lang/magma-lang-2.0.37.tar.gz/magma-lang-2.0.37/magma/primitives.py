from .bit import Bit
from .bits import Bits
from .circuit import DeclareCoreirCircuit
from .t import In, Out


def make_Defines(name, port, direction):
    def simulate(self, value_store, state_store):
        pass

    def Define(width):
        return DeclareCoreirCircuit(
            name,
            port, direction(Bits[width]),
            coreir_name=name,
            coreir_lib="coreir",
            coreir_genargs={"width": width},
            simulate=simulate
        )

    def DefineCorebit():
        return DeclareCoreirCircuit(
            f"corebit_{name}",
            port, direction(Bit),
            coreir_name=name,
            coreir_lib="corebit",
            simulate=simulate
        )
    return Define, DefineCorebit


DefineUndriven, DefineCorebitUndriven = make_Defines("undriven", "O", Out)
DefineTerm, DefineCorebitTerm = make_Defines("term", "I", In)
