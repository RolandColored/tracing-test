import unittest

from tracing.graph import Graph


class TestGraphTrace(unittest.TestCase):

    def setUp(self):
        with open('test_graph.txt', 'r') as file:
            graph_definition = file.read()
            self.test_graph = Graph(graph_definition)

    def test_avg_latency(self):
        self.assertEqual(9, self.test_graph.avg_latency("A-B-C"))


if __name__ == '__main__':
    unittest.main()
