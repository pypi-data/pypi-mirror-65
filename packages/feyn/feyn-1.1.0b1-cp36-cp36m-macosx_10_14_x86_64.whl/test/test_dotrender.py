import unittest
import feyn

class TestDotRender(unittest.TestCase):
    def _create_graph(self):
        # It was not easy to figure out how to create this programatically.
        # So I have just grabbed an example from a notebook.
        # TODO: Create this programatically, so the test does not break on
        # changes in _from_dict.
        return feyn.Graph._from_dict({
            'directed': True,
            'multigraph': True,
            'nodes': [{
                'id': 0,
                'celltype': 'cont',
                'location': (0, -1, -1),
                'legs': 1,
                'gluamine': 0,
                'label': 'in',
                'state': {
                    'variance': 13206.6435546875,
                    'absmax': 192.6171875,
                }
            }, {
                'id': 1,
                'celltype': 'cont',
                'location': (2, -1, -1),
                'legs': 1,
                'gluamine': 0,
                'label': 'out',
                'state': {
                    'variance': 0.06923199445009232,
                    'absmax': 1.0,
                }
            }],
            'links': [
                {'source': 0, 'target': 1, 'ord': 0}
            ]
        })

    def xtest_rendergraph_returns_none_when_graphviz_is_not_installed(self):
        self.assertFalse(feyn.DotRenderer.can_render, "Sanity check for graphviz not being installed")
        
        # Should not crash
        g = self._create_graph()
        dot = feyn.DotRenderer.rendergraph(g)
        self.assertIsNone(dot)
