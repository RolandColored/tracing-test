import sys

from tracing.graph import Graph


if len(sys.argv) != 2:
    print("Please provide the path to the graph definition text file (and nothing else)")
    exit(1)

path = sys.argv[1]
with open(sys.argv[1], 'r') as file:
    graph_definition = file.read()
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
print(f'10. {graph.number_of_traces_shorter("C", "C", 30)}')

