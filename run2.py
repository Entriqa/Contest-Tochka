import sys
from heapq import heappop, heappush


def is_lock(letter: str) -> bool:
    return 'A' <= letter <= 'Z'


def dijkstra(graph: dict[str, list[str]], start: str) -> tuple[dict[str, str], str] | None:
    pq = [(0, start)]
    prev = {gate: ""  for gate in graph.keys()}
    dist = {gate: 1000  for gate in graph.keys()}
    dist[start] = 0
    min_dist = 1000
    min_gate = "Z"

    while pq:
        cost, knot = heappop(pq)
        for v in graph[knot]:
            new_cost = cost + 1
            if new_cost < dist[v]:
                dist[v] = new_cost
                prev[v] = knot
                heappush(pq, (new_cost, v))
                if is_lock(v):
                    if min_dist > dist[v]:
                        min_dist = dist[v]
                        min_gate = v
                    if v < min_gate and dist[v] <= min_dist:
                        min_gate = v
            if min_dist < dist[v]:
                 return prev, min_gate
    return prev, min_gate


def parse_edges(edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    vertex_neighbours = dict()
    for u, v in edges:
        if u not in vertex_neighbours.keys():
            vertex_neighbours[u] = []
            vertex_neighbours[u].append(v)
        else:
            vertex_neighbours[u].append(v)
        if v not in vertex_neighbours.keys():
            vertex_neighbours[v] = []
            vertex_neighbours[v].append(u)
        else:
            vertex_neighbours[v].append(u)
    return vertex_neighbours


def is_all_gates_isolated(edges_neighbours: dict[str, list[str]]) -> bool:
    return all(not edges_neighbours[c] for c in edges_neighbours.keys() if is_lock(c))


def first_and_last_edges_of_path(path: dict[str, str],  start_vertex: str, gate: str) -> tuple[tuple[str, str], tuple[str, str]]:
    first_edge = [(key, value) for key, value in path.items() if value == start_vertex][0]
    last_edge = (gate, path[gate])
    return first_edge, last_edge


def solve(edges: list[tuple[str, str]]) -> list[str]:
    result = []
    start_vertex = "a"
    vertex_neighbours = parse_edges(edges)

    while not is_all_gates_isolated(vertex_neighbours):
        path, gate = dijkstra(vertex_neighbours, start_vertex)
        if not any(path.values()):
            break
        first_edge, last_edge = first_and_last_edges_of_path(path, start_vertex, gate)
        vertex_neighbours[last_edge[0]].remove(last_edge[1])
        vertex_neighbours[last_edge[1]].remove(last_edge[0])
        result.append(f"{last_edge[0]}-{last_edge[1]}")
        start_vertex = first_edge[0]

    return result


def main():
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.append((node1, node2))

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
