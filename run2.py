import sys
from collections import deque


def is_gate(node: str) -> bool:
    return 'A' <= node <= 'Z'


def bfs_find_target_and_path(graph: dict[str, list[str]], start: str) -> tuple[str, list[str]]:
    queue = deque([start])
    prev = {start: None}
    dist = {start: 0}

    target_gate = None
    min_dist = float('inf')

    while queue:
        current = queue.popleft()

        for neighbor in graph[current]:
            if neighbor not in dist:
                dist[neighbor] = dist[current] + 1
                prev[neighbor] = current
                queue.append(neighbor)

                if is_gate(neighbor):
                    if dist[neighbor] < min_dist:
                        min_dist = dist[neighbor]
                        target_gate = neighbor
                    elif dist[neighbor] == min_dist and neighbor < target_gate:
                        target_gate = neighbor

    if target_gate is None:
        return None, []

    path = []
    current = target_gate
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()

    return target_gate, path


def parse_edges(edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    vertex_neighbours = {}
    for u, v in edges:
        if u not in vertex_neighbours:
            vertex_neighbours[u] = []
        if v not in vertex_neighbours:
            vertex_neighbours[v] = []
        vertex_neighbours[u].append(v)
        vertex_neighbours[v].append(u)

    for node in vertex_neighbours:
        vertex_neighbours[node].sort()

    return vertex_neighbours


def get_all_gate_edges(graph: dict[str, list[str]]) -> list[tuple[str, str]]:
    edges = []
    for node in graph:
        if is_gate(node):
            for neighbor in graph[node]:
                if not is_gate(neighbor):
                    edges.append((node, neighbor))
    return edges


def solve(edges: list[tuple[str, str]]) -> list[str]:
    graph = parse_edges(edges)
    virus_pos = "a"
    result = []

    while True:
        gate_edges = get_all_gate_edges(graph)
        if not gate_edges:
            break

        chosen_edge = None
        for gate, node in sorted(gate_edges):
            graph[gate].remove(node)
            graph[node].remove(gate)

            _, path = bfs_find_target_and_path(graph, virus_pos)

            safe = (len(path) < 2 or not is_gate(path[1]))

            graph[gate].append(node)
            graph[node].append(gate)
            graph[gate].sort()
            graph[node].sort()

            if safe:
                chosen_edge = (gate, node)
                break

        if chosen_edge is None:
            break

        gate, node = chosen_edge
        graph[gate].remove(node)
        graph[node].remove(gate)
        result.append(f"{gate}-{node}")

        _, path = bfs_find_target_and_path(graph, virus_pos)
        if len(path) > 1:
            virus_pos = path[1]
        else:
            break

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