from typing import List
import itertools
import threading

import networkx as nx

import _feyn

from ._register import Register
from .losses import get_loss_function
from feyn import DotRenderer, Graph

class QGraph:
    """
    The QGraph is generated from the QLattice and contains all theoretically possible combinations for given Input Registers to output Registers.

    It is tuned to solve a specific task, so we can evaluate its performance and extract learnings to send back to our QLattice.

    This is equivalent to a model in other frameworks.
    """
    def __init__(self, input_registers: List[Register], output_register: Register, graph_dict: dict):
        """Construct a new 'QGraph' object.
        
        Arguments:
            input_registers {List[Register]} -- Input registers in this QGraph
            output_register {List[Register]} -- Output register for the QGraph
            graph_dict {dict} -- A dictionary containing the QGraph descriptor.
        """
        # TODO: Documentation: What are the keys graph_dict?
        self.G = nx.readwrite.json_graph.node_link_graph(graph_dict)

        self.input_registers = {reg.label: reg for reg in input_registers}
        self.output_register = output_register
                
        self.out_reg_dict = graph_dict["out_reg"]

        self.graphs = self._extract_graphs()
        self._is_tuned = False

    def render(self):
        """ Render Qgraph.
        
        Note: Requires that you have GraphViz installed on your system.

        Returns:
            graphviz.Digraph -- GraphViz representation.
        """
        return DotRenderer.renderqgraph(self.G)

    def head(self, n=5):
        """ Render most probable Graphs.

        Keyword Arguments:
            n {int} -- Number of graphs to display (default: {5}).
        """
        import IPython
        for i in range(n):
            IPython.display.display(self.graphs[i])


    def fit(self, data, epochs=10, show="graph", threads=1):
        """ Fit Qgraph with given samples.

        Arguments:
            data {Iterable} -- Training data including both input at expected values.

        Keyword Arguments:
            epochs {int} -- Number of epochs to run (default: {10}).
            show -- Controls status display. Must be either None, "graph", "text", or a user defined callback function
        """

        # Magic support for pandas DataFrame
        if type(data).__name__ == "DataFrame":
            data = {col: data[col].values for col in data.columns}

        if threads!=1:
            print("Warning: concurrency is experimental and may cause segfaults. Do not use with categorical registers yet")

        _best_ix = 0
        _counter = itertools.count()
        _terminate = False
        
        def update_display():
            nonlocal _best_ix, _counter

            status = "Loss: %.6f" % (self.graphs[_best_ix].loss_epoch)

            if show == "graph":
                import IPython
                dot = DotRenderer.rendergraph(self.graphs[_best_ix])
                dot.attr(label="\n"+status)
                IPython.display.clear_output(wait=True)
                IPython.display.display(dot)

            elif show == "text":
                print(status)
            elif callable(show):
                show(self, self.graphs[_best_ix])
            elif show is None:
                pass
            else:
                raise Exception("show must be either None, 'graph' or 'text', or a callback function")


        def fitting_thread():
            nonlocal _terminate, _best_ix, _counter, epochs, self
            while not _terminate:
                ix = next(_counter)
                if ix >= len(self.graphs):
                    return
                g = self.graphs[ix]
                g._tune(data, data[self.output_register.label], epochs)
                if g.loss_ema <= self.graphs[_best_ix].loss_ema:
                    _best_ix = ix
                    update_display()

        threadlist = [threading.Thread(target=fitting_thread) for num in range(threads)]
        try:
            [t.start() for t in threadlist]
            [t.join() for t in threadlist]
        finally:
            _terminate=True
            [t.join() for t in threadlist]

        self.graphs.sort(key=lambda g: g.loss_ema, reverse=False)

    def tune(self, X, Y, epochs=10, showgraph=True, edgepenalty=0.001, extra_info=None, callback=None):
        """ Tune Qgraph with given samples.

        Arguments:
            X {Iterable} -- Input values.
            Y {Iterable} -- Expected output.

        Keyword Arguments:
            epochs {int} -- Number of epochs to run (default: {10}).
            showgraph {bool} -- show a live updated graph sample.
            edgepenalty {float} -- Penalty configuration (default: {0.001}).
        """

        # Magic support for pandas DataFrame and Series
        if type(X).__name__ == "DataFrame":
            X = {col: X[col].values for col in X.columns}

        if type(Y).__name__ == "Series":
            Y = Y.values

        if showgraph and not DotRenderer.can_render:
            print(DotRenderer.cannot_render_msg)
            showgraph = False
        
        for epoch in range(epochs):
            for wg in self.graphs:
                wg._tune(X, Y, 1)

            # Sort by decreasing loss after adding penalty for number of edges
            self.graphs.sort(key=lambda g: g.loss_ema * g.edge_count ** edgepenalty, reverse=False)

            status = "\nEpoch %i: Loss: %.6f" % (epoch, self.graphs[0].loss_ema)

            if extra_info is not None:
                status = f"{status}\n{extra_info}"
                
            if showgraph:
                import IPython
                dot = DotRenderer.rendergraph(self.graphs[0])
                dot.attr(label=status)
                IPython.display.clear_output(wait=True)
                IPython.display.display(dot)
            else:
                print(status)
            
            if callback:
                callback(self, epoch)
        
        self._is_tuned = True

    def select(self, data, func=None, loss=None, sort=None, n=5):
        """ Get a list of graphs filtered and sorted. 
        You can provide data to predict on and sort on that loss too.
        
        Keyword Arguments:
            data {tuple} -- (X, y) (default: {None})
            func {[type]} -- Function to filter the graph collection (default: {None})
            It should return True or False to include the graph or not.
            loss {[type]} -- Only applies if data is provided. (default: {None})
            this is the loss function to use when using validation datset
        """

        # Magic support for pandas DataFrame
        if type(data).__name__ == "DataFrame":
            data = {col: data[col].values for col in data.columns}

        if loss is None:
            loss = _feyn.DEFAULT_LOSS

        loss_func = get_loss_function(loss)

        data_losses = {}
        for graph in self.graphs:
            l = loss_func(data[self.output_register.label], graph.predict(data))
            data_losses[graph] = l


        graph_collection = self.graphs.copy()
        if func is not None:
            graph_collection = list(filter(func, graph_collection))

        def func_wrapper(g):
            loss = data_losses[g]

            if sort is not None:
                return sort(g, loss)
            else:
                return loss

        graph_collection.sort(key=lambda g : func_wrapper(g), reverse=False)
        
        return graph_collection[0:n]


    def _extract_graphs(self) -> List[Graph]:
        graphs = set()

        for nodeid, data in self.G.nodes(data=True):
            if data["type"] != "reg":
                graphs.add(self._prune(nodeid))

        return sorted(graphs, key=lambda n: n.strength, reverse=True)

    def _prune(self, nodeid: int) -> Graph:
        needed = nx.algorithms.dag.ancestors(self.G, nodeid)
        needed.add(nodeid)
        subgraph = self.G.subgraph(needed)

        # The following algorithm builds a 1D array of nodes
        # that preserverves execution order
        nodelist = []
        current = [nodeid]
        while len(current) > 0:
            node = current.pop(0)
            if node in nodelist:
                nodelist.remove(node)
            nodelist.insert(0, node)
            for pred in subgraph.predecessors(node):
                current.append(pred)

        # Build a graph with the interactions
        sz = len(nodelist)+1
        graph = Graph(sz, self.output_register)

        for i, nodeid in enumerate(nodelist):
            data = subgraph.nodes[nodeid]

            interaction = Graph._get_interaction(data)
            graph[i] = interaction

            if data["type"]=="reg":
                interaction.set_source(0, -1)
                continue

            interaction.linkdata = [None, None]

            for pred, _, data in subgraph.in_edges(nodeid, data=True):
                source_idx = nodelist.index(pred)
                ordinal = data["ord"]
                interaction.set_source(ordinal, source_idx)
                interaction.linkdata[ordinal] = data

        out_reg = Graph._get_interaction(self.out_reg_dict)
        out_reg.linkdata = [{"ord": 0}]

        out_reg.set_source(0, sz-2)
        out_reg.loss = self.output_register.loss

        graph[sz-1] = out_reg

        graph.strength = self.G.nodes[nodeid]["output_strength"]

        return graph

    def __repr__(self):
        regcnt = 0
        double = 0
        single = 0
        for n, data in self.G.nodes.data():
            if data["type"] == "reg":
                regcnt += 1

            else:
                legs = data["legs"]
                if legs == 1:
                    single += 1
                else:
                    double += 1

        out_label = self.output_register.label
        return "QGraph for '%s' <size: %i (%i registers, %i singles, %i doubles)>" % (out_label, regcnt+double+single, regcnt, single, double)