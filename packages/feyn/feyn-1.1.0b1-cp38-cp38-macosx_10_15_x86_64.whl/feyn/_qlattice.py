import os
import typing

import requests

from ._register import Register

import _feyn
from feyn import Graph, QGraph

import socket

class QLattice:
    """
    The QLattice is a potentially very large lattice that links registers to
    each other through a set of interaction cells.

    QLattice incorporates all the knowledge learned about the probabilities of
    relations between registers and interaction cells.

    Through abzu algorithm we can extract QGraphs from the QLattice.
    """
    QLATTICE_BASE_URI = os.environ.get('QLATTICE_BASE_URI') or 'http://localhost:5000'

    def __init__(self, url=None, reset=False) -> None:
        """Construct a new 'QLattice' object.

        Keyword Arguments:
            url {str} -- URL of where your QLattice is running.
            reset {bool} -- Clears all learnings in the QLattice. Potentially very dangerous. Think twice before setting this to True! (default: {False})
        """
        if url is None:
            url = f"{self.QLATTICE_BASE_URI}/api/v1/qlattice"
        elif '/api/v1/qlattice' not in url:
            url = f"{url}/api/v1/qlattice"

        self.url = url
        self.agent_id = socket.gethostname()  # Hostname for now. Will do something better when authz is in place

        self._load_qlattice(reset)

    def get_register(self, label: str, register_type: str = "fixed", loss=_feyn.DEFAULT_LOSS) -> Register:
        """Get a reference to a QLattice register. If the register doesn't exist, allocate a new one.
        Arguments:
            label {str} -- Name of the register.
            register_type {str} -- Register type, either "fixed" or "cat". (numerical or categorical)
            loss {[str, function]} -- Loss function to use for optimization operations. This only applies when used as output register.
        Returns:
            Register -- The register instance.
        """

        req = requests.put("%s/register" % self.url,
                            headers={ "Agent-Id": self.agent_id },
                            json={
                                'celltype': register_type,
                                'label': label
                            })
        req.raise_for_status()

        if req.status_code == 200:
            self._load_qlattice()

        reg = req.json()

        res = Register(register_type, reg['label'], reg['location'])

        if register_type == "fixed":
            res.loss = loss

        return res

    def get_qgraph(self, inputs: typing.List[Register], output: Register, steps: int = 3) -> QGraph:
        """Extract QGraph from inputs registers to output register.

        Arguments:
            inputs {typing.List[Register]} -- Input registers.
            output {Register} -- Output register.

        Returns:
            QGraph -- The QGraph instance from the inputs to the output.
        """

        req = requests.post("%s/simulation" % self.url,
                            headers={ "Agent-Id": self.agent_id },
                            json={
                                'inputs': [reg.to_dict() for reg in inputs],
                                'output': output.to_dict(),
                                'steps': steps
                            })

        req.raise_for_status()

        graph = req.json()

        qgraph = QGraph(inputs, output, graph)

        return qgraph

    def update(self, graph: Graph) -> None:
        """ Update QLattice with learnings from a graph.

        Arguments:
            graph {Graph} -- Graph with learnings worth storing.
        """
        req = requests.post("%s/update" % self.url,
                            headers={ "Agent-Id": self.agent_id },
                            json=graph._to_dict()
                            )

        req.raise_for_status()

    def _load_qlattice(self, reset=False):
        req = requests.get( self.url,
                            headers={ "Agent-Id": self.agent_id },
                            params={'reset': reset})
        req.raise_for_status()
        qlattice = req.json()

        self.width = qlattice['width']
        self.height = qlattice['height']

        self.registers = [Register(reg['celltype'], reg['label'], reg['location']) for reg in qlattice['registers']]

    def __repr__(self):
        return "<Abzu QLattice[%i,%i] '%s'>" % (self.width, self.height, self.url)
