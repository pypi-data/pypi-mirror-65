import _feyn

class Register:
    """
    Registers are the main interaction point with the QLattice, IO interfaces.
    Users connect registers with their data concepts, columns in their dataset or stores.
    """
    def __init__(self, celltype, label, location) -> None:
        """Construct a new 'Register' object.

        Arguments:
            celltype {str} -- Either "cont" or "cat" (continous or categorical).
            label {str} -- Name of the register, so that you can find it again later.
                           Usually the column name in your dataset, or the name of the concept this register represents.
            location {tuple(int, int, int)} -- Location in the QLattice.
        """
        self.celltype = celltype
        self.label = label
        self.location = location
        self._loss = None
    
    @property
    def loss(self):
        return self._loss

    @loss.setter
    def loss(self, loss):
        if self.celltype != "fixed":
            raise ValueError("Only fixed registers support loss")
            
        if type(loss).__name__ == "function":
            loss = loss.__name__

        self._loss = loss
    
    def to_dict(self):
        return {
            'celltype': self.celltype,
            'label': self.label
        }

