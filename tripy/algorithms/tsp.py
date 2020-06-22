from typing import List, Dict
from math import inf


class TspSolver:
    def __init__(self, adjacency_matrix: List[List[float]], start: int = 0) -> None:
        if len(adjacency_matrix) <= 2:
            raise Exception('TSP on 0, 1, or 2 nodes does not make any sense!')
        if len(adjacency_matrix) != len(adjacency_matrix[0]):
            raise Exception('Square matrix required for adjacency matrix!')
        if not 0 <= start < len(adjacency_matrix):
            raise IndexError('Starting node must be 0 <= s < N!')

        self._matrix = adjacency_matrix
        self._start = start  # starting node
        self._solved = False
        self._N = len(self._matrix)

    @property
    def start(self) -> int:
        return self._start

    @start.setter
    def start(self, start: int) -> None:
        if self._start != start:
            if not 0 <= start < self._N:
                raise IndexError('Starting node must be 0 <= s < N!')

            self._start = start
            self._solved = False  # flag to false so that the algorithm can be execute again

    def min_cost(self) -> float:
        raise NotImplementedError('Min cost method not implemented!')

    def best_route(self) -> List[int]:
        raise NotImplementedError('Best route method not implemented!')



class NaiveTspSolver(TspSolver):

    def __init__(self, adjacency_matrix: List[List[float]], start: int = 0) -> None:
        super().__init__(adjacency_matrix, start)
        # caching all routes to prevent expensive execution
        # key: cost, value: [[nodes of a route]]
        self._routes = {}

    def min_cost(self) -> float:
        self._solve()
        return min(self._routes)

    def best_route(self) -> List[int]:
        self._solve()
        return self._routes[self.min_cost()][0]

    def _solve(self) -> None:
        if self._solved:
            return

        # starting point might have changed, so clear it first
        self._routes.clear()

        route = [self._start]
        nodes = [x for x in range(self._N) if x != self._start]
        self._tsp(route, nodes, 0)

        # prevent re-execute
        self._solved = True

    # route param requires a list with starting node in it, else it will give key error
    def _tsp(self, route: List[int], nodes: List[int], cost: float) -> None:
        if len(nodes) == 0:
            cost = round(cost, 4)
            if cost in self._routes:
                self._routes[cost].append(route)
            else:
                self._routes[cost] = [route]
            return

        for n in range(len(nodes)):
            self._tsp(route=route + [nodes[n]], nodes=nodes[:n] + nodes[n + 1:],
                      cost=cost + self._matrix[route[-1]][nodes[n]])


class DpTspSolver(TspSolver):

    def __init__(self, adjacency_matrix: List[List[float]], start: int = 0) -> None:
        super().__init__(adjacency_matrix, start)
        self._min_cost = 0
        self._best_route = []
        self._END_STATE = (1 << self._N) - 1  # all bits are set to 1 (meaning all the nodes have been visited)

    def min_cost(self) -> float:
        self._solve()
        return self._min_cost

    def best_route(self) -> List[int]:
        self._solve()
        return self._best_route

    def _solve(self) -> None:
        if self._solved:
            return

        cost_memo = {}
        node_memo = {}
        state = 1 << self._start
        self._min_cost = self._tsp(self._start, state, cost_memo, node_memo)
        self._best_route = self._build_route(self._start, state, node_memo)

        # prevent re-execute
        self._solved = True

    def _tsp(self, curr: int, state: int, cost_memo: Dict, node_memo: Dict) -> float:
        if state == self._END_STATE:
            return 0  # because we are not going back to starting

        if (curr, state) in cost_memo:
            return cost_memo[(curr, state)]

        min_cost = inf
        next_node = -1
        for _next in range(self._N):
            # skip if _next has been visited
            if state & (1 << _next) != 0:
                continue

            next_state = state | (1 << _next)
            cost = round(self._matrix[curr][_next] + self._tsp(_next, next_state, cost_memo, node_memo), 4)
            if cost < min_cost:
                min_cost = cost
                next_node = _next

        node_memo[(curr, state)] = next_node
        cost_memo[(curr, state)] = min_cost
        return min_cost

    def _build_route(self, curr: int, state: int, node_memo: Dict) -> List[int]:
        route = [curr]

        while True:
            if (curr, state) not in node_memo:
                break
            next_node = node_memo[(curr, state)]
            route.append(next_node)
            curr = next_node
            state = state | (1 << next_node)

        return route

# def permute(a: List, b: List) -> Iterator:
#     if len(b) == 0:
#         yield a
#
#     for n in range(len(b)):
#         yield from permute(a + [b[n]], b[:n] + b[n + 1:])
