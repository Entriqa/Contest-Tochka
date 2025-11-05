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


def solve(edges: list[tuple[str, str]]) -> list[str]:
    result = []
    virus_position = "a"
    graph = parse_edges(edges)
    target_gate, path_to_gate = bfs_find_target_and_path(graph, virus_position)

    while target_gate:
        node = path_to_gate[-2]
        result.append(f"{target_gate}-{node}")

        graph[target_gate].remove(node)
        graph[node].remove(target_gate)

        target_gate, path_to_gate = bfs_find_target_and_path(graph, virus_position)
        if target_gate:
            virus_position = path_to_gate[1]

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
