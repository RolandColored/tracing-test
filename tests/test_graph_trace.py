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
        self.assertEqual("NO SUCH TRACE", self.test_graph.total_avg_latency("A-E-D"))

    def test_number_of_traces(self):
        self.assertEqual(2, self.test_graph.number_of_traces("C", "C", 3))
        self.assertEqual(3, self.test_graph.number_of_traces("A", "C", 4, 4))

    def test_shortest_trace(self):
        self.assertEqual(9, self.test_graph.shortest_trace("A", "C"))
        self.assertEqual(9, self.test_graph.shortest_trace("B", "B"))

    def test_number_of_traces_shorter(self):
        self.assertEqual(7, self.test_graph.number_of_traces_shorter("C", "C", 30))


if __name__ == '__main__':
    unittest.main()
