import unittest
import pandas as pd
import numpy as np

import feyn.losses
from feyn import QLattice


class TestSDK(unittest.TestCase):

    def test_can_add_new_registers(self):
        lt = QLattice(reset=True)

        lt.get_register("Age",)
        lt.get_register("Smoker",)
        lt.get_register("bmi",)

        self.assertEqual(len(lt.registers), 3)

    def test_location_is_assigned_to_registers_automatically(self):
        lt = QLattice(reset=True)

        r1 = lt.get_register("Age",)
        r2 = lt.get_register("Smoker",)

        self.assertNotEqual(r1.location, r2.location)

    def test_register_is_reused(self):
        lt = QLattice(reset=True)

        lt.get_register("Age")
        lt.get_register("Smoker")

        self.assertEqual(len(lt.registers), 2)

        lt.get_register("Smoker")

        self.assertEqual(len(lt.registers), 2)

    def test_qlattice_extracts_qgraphs(self):
        lt = QLattice(reset=True)

        r1 = lt.get_register("Age")
        r2 = lt.get_register("Smoker")
        r3 = lt.get_register("insurable")

        qgraph = lt.get_qgraph([r1, r2], r3)

        qgraph._extract_graphs()

        self.assertGreater(len(qgraph.graphs), 0)

    def test_qgraph_tune(self):
        lt = QLattice(reset=True)

        r1 = lt.get_register("Age")
        r2 = lt.get_register("Smoker")
        r3 = lt.get_register("insurable")

        qgraph = lt.get_qgraph([r1, r2], r3)

        data = pd.DataFrame(np.array([
                [10, 16, 30, 60],
                [0, 1, 0, 1],
                [1, 1, 1, 0]
            ]).T,
            columns=["Age", "Smoker", "insurable"]).astype({
                "Age": "float32",
                "Smoker": "float32",
                "insurable": "float32"
            })

        X = data[["Age", "Smoker"]]
        Y = data["insurable"]

        qgraph.tune(X, Y, showgraph=False)

    def test_can_fetch_graphs_after_updates(self):
        lt = QLattice(reset=True)

        r1 = lt.get_register("Age")
        r2 = lt.get_register("Smoker")
        r3 = lt.get_register("insurable")

        qgraph = lt.get_qgraph([r1, r2], r3)
        lt.update(qgraph.graphs[0])

        qgraph = lt.get_qgraph([r1, r2], r3)

        self.assertGreater(len(qgraph.graphs), 0)

    def test_qgraph_select(self):
        lt = QLattice(reset=True)

        r1 = lt.get_register("Age")
        r2 = lt.get_register("Smoker")
        r3 = lt.get_register("insurable")

        qgraph = lt.get_qgraph([r1, r2], r3)

        data = pd.DataFrame(np.array([
                [10, 16, 30, 60],
                [0, 1, 0, 1],
                [1, 1, 1, 0]
            ]).T,
            columns=["Age", "Smoker", "insurable"]).astype({
                "Age": "float32",
                "Smoker": "float32",
                "insurable": "float32"
            })

        X = data[["Age", "Smoker"]]
        Y = data["insurable"]

        qgraph.tune(X, Y, showgraph=False)

        v_data = pd.DataFrame(np.array([
        [8, 16, 25, 50],
        [0, 0, 1, 1],
        [1, 0, 1, 0]
            ]).T,
            columns=["Age", "Smoker", "insurable"]).astype({
                "Age": "float32",
                "Smoker": "float32",
                "insurable": "float32"
            })
        
        X = v_data[["Age", "Smoker"]]
        y = v_data["insurable"]

        graphs = qgraph.select(v_data)

        self.assertGreater(len(graphs), 0)

        graphs = qgraph.select(v_data, func=lambda g: False )

        self.assertEqual(len(graphs), 0)

        graphs = qgraph.select(v_data, sort=lambda g, loss: loss, n=5)

        self.assertEqual(len(graphs), 5)

        graphs = qgraph.select(v_data, loss=feyn.losses.mean_absolute_error, n=5)

        self.assertEqual(len(graphs), 5)
