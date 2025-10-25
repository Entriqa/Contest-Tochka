import sys
from heapq import heappop, heappush

ENERGY = {"A": 1, "B": 10, "C": 100, "D": 1000}
AVAILABLE_POS = [0, 1, 3, 5, 7, 9, 10]
ROOM_ENTRANCES = [2, 4, 6, 8]


def parse_labyrinth(lines: list[str]) -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]:
    hall = tuple(['.' for _ in range(11)])
    rooms_lines = tuple([line for line in lines if any(c in "ABCD" for c in line)])
    rooms_ind = [3, 5, 7, 9]
    rooms = tuple([tuple([line[ind] for line in rooms_lines]) for ind in rooms_ind])
    return hall, rooms


def is_end(rooms: tuple[tuple[str, ...], ...]) -> bool:
    for i, room in enumerate(rooms):
        if any(c != "ABCD"[i] for c in room):
            return False
    return True


def all_moves(hall: tuple[str, ...], rooms: tuple[tuple[str, ...], ...]) -> list[tuple[int, tuple[tuple[str], tuple[tuple[str]]]]]:
    room_size = len(rooms[0])
    moves = []

    for pos, elem in enumerate(hall):
        if elem == ".":
            continue
        elem_room = "ABCD".index(elem)

        if any(c not in (".", elem) for c in rooms[elem_room]):
            continue

        path_clear = all(hall[c] == '.' for c in range(min(pos, ROOM_ENTRANCES[elem_room]) + 1,
                                                       max(pos, ROOM_ENTRANCES[elem_room])))
        if not path_clear:
            continue

        for room_pos in range(room_size - 1, -1, -1):
            if rooms[elem_room][room_pos] == ".":
                room_depth = room_pos
                break
        else:
            continue

        steps = abs(pos - ROOM_ENTRANCES[elem_room]) + room_depth + 1
        cost = steps * ENERGY[elem]

        new_hall = list(hall)
        new_hall[pos] = '.'
        new_rooms = [list(room) for room in rooms]
        new_rooms[elem_room][room_depth] = elem
        moves.append((cost, (tuple(new_hall), tuple(tuple(room) for room in new_rooms))))

    for pos, room in enumerate(rooms):
        target_type = 'ABCD'[pos]
        if all(c in ('.', target_type) for c in room):
            continue

        room_depth = 0
        alpha = ""
        for depth_pos in range(room_size):
            if room[depth_pos] != '.':
                room_depth = depth_pos
                alpha = room[depth_pos]
                break

        for hpos in AVAILABLE_POS:
            step = 1 if hpos > ROOM_ENTRANCES[pos] else -1
            path_clear = all(hall[p] == '.' for p in range(ROOM_ENTRANCES[pos] + step, hpos + step, step))
            if not path_clear:
                continue

            steps = abs(hpos - ROOM_ENTRANCES[pos]) + room_depth + 1
            cost = steps * ENERGY[alpha]

            new_hall = list(hall)
            new_hall[hpos] = alpha
            new_rooms = [list(room) for room in rooms]
            new_rooms[pos][room_depth] = '.'
            moves.append((cost, (tuple(new_hall), tuple(tuple(room) for room in new_rooms))))

    return moves


def dijkstra(start_state: tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]) -> int | None:
    pq = [(0, start_state)]
    best = {start_state: 0}

    while pq:
        cost, state = heappop(pq)
        if cost > best[state]:
            continue
        hallway, rooms = state
        if is_end(rooms):
            return cost
        for move_cost, new_state in all_moves(*state):
            new_cost = cost + move_cost
            if new_cost < best.get(new_state, 10**12):
                best[new_state] = new_cost
                heappush(pq, (new_cost, new_state))
    return None


def solve(lines: list[str]) -> int:
    state = parse_labyrinth(lines)
    return dijkstra(state) or 0


def main():
    # Чтение входных данных
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main()