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

