from itertools import combinations
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
        self.duplicate_graph = self._clone_with_duplicate_nodes()

        if nx.number_of_selfloops(self.graph) > 0:
            raise GraphException("loops are not allowed")

    def total_avg_latency(self, trace: str) -> int or str:
        """
        Calculates the average latency for the given trace.
        :param trace: trace in the format "A-B-C"
        :return: average latency or "NO SUCH TRACE"
        """
        node_path = trace.split("-")
        edge_path = list(pairwise(node_path))
        edges = [self.graph.get_edge_data(u, v) for u, v in edge_path]
        if None in edges:
            return "NO SUCH TRACE"
        return sum(edge["weight"] for edge in edges)

    def number_of_traces(self, start_node: str, end_node: str, max_hops: int, min_hops: int = 1) -> int:
        """
        Finds the number of traces originating in start_node and ending in end_node with a maximum of max_hops hop
        :param start_node: the source node
        :param end_node: the target node
        :param max_hops: maximum number of hops to look for
        :param min_hops: minimum number of hops to look for
        :return: number of traces
        """
        all_max_length_paths = list(self._traverse_for_path(start_node, max_hops))
        mixed_length_paths = list(all_max_length_paths)

        for length in range(min_hops, max_hops):
            shorter_paths = [path[0:length+1] for path in all_max_length_paths]
            mixed_length_paths += shorter_paths

        return len([path for path in set(mixed_length_paths) if path[-1] == end_node])

    def shortest_trace(self, start_node: str, end_node: str) -> int:
        """
        Finds the shortest path through our trace graph.
        :param start_node: the source node
        :param end_node: the target node
        :return: total path costs
        """
        return nx.shortest_path_length(self.duplicate_graph, start_node+"'", end_node, "weight")

    def _traverse_for_path(self, current_node: str, hops_left: int) -> list:
        if hops_left == 0:
            yield current_node
        else:
            for successor in self.graph.successors(current_node):
                for path in self._traverse_for_path(successor, hops_left - 1):
                    yield current_node + path

    def _clone_with_duplicate_nodes(self):
        # The method shortest_path_length checks for start_node==end_node and returns 0.
        # But we don't want to allow these traces so we need to do a trick.
        # We will clone the graph and add for each node a duplicate node' with all original outgoing edges.
        graph_clone = self.graph.copy()
        outgoing_edges = graph_clone.edges()
        new_start_edges = [(u + "'", v, graph_clone.get_edge_data(u, v)["weight"]) for u, v in outgoing_edges]
        graph_clone.add_weighted_edges_from(new_start_edges)
        return graph_clone

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

