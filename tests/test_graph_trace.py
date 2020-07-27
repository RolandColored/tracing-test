import unittest

from tracing.graph import Graph, GraphException


class TestGraphTrace(unittest.TestCase):

    def setUp(self):
        with open('test_graph.txt', 'r') as file:
            graph_definition = file.read()
            self.test_graph = Graph(graph_definition)

    def test_total_avg_latency(self):
        self.assertEqual(9, self.test_graph.total_avg_latency("A-B-C"))
        self.assertEqual(5, self.test_graph.total_avg_latency("A-D"))
        self.assertEqual(13, self.test_graph.total_avg_latency("A-D-C"))
        self.assertEqual(22, self.test_graph.total_avg_latency("A-E-B-C-D"))

        with self.assertRaises(GraphException) as context:
            self.test_graph.total_avg_latency("A-E-D")
        self.assertTrue('no such trace' in str(context.exception))

    def test_shortest_trace(self):
        self.assertEqual(9, self.test_graph.shortest_trace("A", "C"))
        self.assertEqual(9, self.test_graph.shortest_trace("B", "B"))


if __name__ == '__main__':
    unittest.main()
