class InstWrapper:
    def __init__(self, inst):
        self.inst = inst
    if attr in self.circuit.interface.ports.keys():
        return PortWrapper(self.circuit.interface.ports[attr], self)
