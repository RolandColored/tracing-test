from typing import List, Tuple

import networkx as nx
from networkx.utils import pairwise


class GraphException(Exception):
    pass


class Graph:

    def __init__(self, definition_str: str):
        """
        Initializes the network using the comma separated list of nodes and weights
        :param definition_str: a string like "AB2, BC4, AC1"
        """
        self.graph = nx.DiGraph()
        self.graph.add_weighted_edges_from(self._parse_definition_str(definition_str))

        if nx.number_of_selfloops(self.graph) > 0:
            raise GraphException("loops are not allowed")

    def total_avg_latency(self, trace: str) -> int:
        """
        Calculates the average latency for the given trace. Raises a GraphException if no such trace exists.
        :param trace: trace in the format "A-B-C"
        :return: average latency
        """
        node_path = trace.split("-")
        edge_path = list(pairwise(node_path))
        edges = [self.graph.get_edge_data(u, v) for u, v in edge_path]
        if None in edges:
            raise GraphException("no such trace")
        return sum(edge["weight"] for edge in edges)

    def shortest_trace(self, start_node: str, end_node: str) -> int:
        """
        Finds the shortest path through our trace graph.
        :param start_node: the source node
        :param end_node: the target node
        :return: total path costs
        """
        if start_node == end_node:
            # The method shortest_path_length checks for this condition and returns 0.
            # But we don't want to allow these traces so we need to do a trick.
            # We will clone the graph and add a fake node start_node' with all original outgoing edges.
            graph_to_use = self.graph.copy()
            outgoing_edges = graph_to_use.edges(nbunch=[start_node])
            new_edges = [(u+"'", v, graph_to_use.get_edge_data(u, v)["weight"]) for u, v in outgoing_edges]
            graph_to_use.add_weighted_edges_from(new_edges)
            start_node = start_node+"'"
        else:
            graph_to_use = self.graph
        return nx.shortest_path_length(graph_to_use, start_node, end_node, "weight")

    @staticmethod
    def _parse_definition_str(definition_str: str) -> List[Tuple]:
        """
        Parses the definition string. For simplicity reasons we assume that the format is always valid
        :param definition_str: see __init__
        :return: list of edge tuples (from, to, weight)
        """
        if definition_str is None or definition_str == "":
            return []
        edges = definition_str.split(",")
        return [(stripped[0], stripped[1], int(stripped[2])) for edge in edges if (stripped := edge.strip())]

