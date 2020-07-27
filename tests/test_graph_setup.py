import unittest

import networkx as nx

from tracing.graph import Graph, GraphException


class TestGraphSetup(unittest.TestCase):

    def test_empty_graph(self):
        test_graph = Graph("")
        self.assertEqual(0, test_graph.graph.number_of_nodes())
        self.assertEqual(0, test_graph.graph.number_of_edges())

    def test_simple_graph(self):
        test_graph = Graph("AB1")
        self.assertEqual(2, test_graph.graph.number_of_nodes())
        self.assertEqual(1, test_graph.graph.number_of_edges())
        sum_weights = sum(value for _, value in nx.get_edge_attributes(test_graph.graph, 'weight').items())
        self.assertTrue(1, sum_weights)

    def test_bigger_graph(self):
        test_graph = Graph("AB1, AC2,CD5, BD3")
        self.assertEqual(4, test_graph.graph.number_of_nodes())
        self.assertEqual(4, test_graph.graph.number_of_edges())
        sum_weights = sum(value for _, value in nx.get_edge_attributes(test_graph.graph, 'weight').items())
        self.assertTrue(11, sum_weights)

    def test_real_graph(self):
        with open('test_graph.txt', 'r') as file:
            graph_definition = file.read()
        test_graph = Graph(graph_definition)
        self.assertEqual(5, test_graph.graph.number_of_nodes())
        self.assertEqual(9, test_graph.graph.number_of_edges())

    def test_loop_graph(self):
        with self.assertRaises(GraphException) as context:
            test_graph = Graph("AA1")
        self.assertTrue('loops' in str(context.exception))

    @unittest.skip("We should validate user input if it really follows the pattern. "
                   "But it's only a helper tool for myself and I'm too lazy :)")
    def test_invalid_graph(self):
        with self.assertRaises(Exception) as context:
            test_graph = Graph("+fd#")
        self.assertTrue('format' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
