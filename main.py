from tracing.graph import Graph

graph_definition = "AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7"

graph = Graph(graph_definition)


print(f'1. {graph.total_avg_latency("A-B-C")}')
print(f'2. {graph.total_avg_latency("A-D")}')
print(f'3. {graph.total_avg_latency("A-D-C")}')
print(f'4. {graph.total_avg_latency("A-E-B-C-D")}')
print(f'5. {graph.total_avg_latency("A-E-D")}')
print(f'6. {graph.number_of_traces("C", "C", 3)}')
print(f'7. {graph.number_of_traces("A", "C", 4, 4)}')
print(f'8. {graph.shortest_trace("A", "C")}')
print(f'9. {graph.shortest_trace("B", "B")}')
print(f'10. {None}')

