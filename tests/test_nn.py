#from tripy.algorithms.nn import NearestNeighbourSolver
from typing import List, Dict

class NearestNeighbourSolver:
    def __init__(self, adjacency_matrix: List[List[float]], sentiment_score: Dict, start: int = 0) -> None:
        if len(adjacency_matrix) <= 2:
            raise Exception('Nearest neighbour on 0, 1, or 2 nodes does not make any sense!')
        if len(adjacency_matrix) != len(adjacency_matrix[0]):
            raise Exception('Square matrix required for adjacency matrix!')
        if len(sentiment_score) < len(adjacency_matrix):
            raise Exception('Insufficient sentiment score!')
        if not 0 <= start < len(adjacency_matrix):
            raise IndexError('Starting node must be 0 <= s < N!')

        self._matrix = adjacency_matrix
        self._scores = sentiment_score
        self._start = start  # starting node
        self._solved = False
        self._N = len(self._matrix)
        self._cost = 0
        self._best_route = []

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

    def cost(self) -> float:
        self._solve()
        return self._cost

    def best_route(self) -> List[int]:
        self._solve()
        return self._best_route

    def _solve(self) -> None:
        if self._solved:
            return

        unvisited = [i for i in range(self._N) if i != self._start]
        route = [self._start]
        curr = self._start
        cost = 0

        while len(unvisited) > 0:
            distances = [self._matrix[curr][i] for i in unvisited]
            scores = [self._scores[i] for i in unvisited]

            # sort unvisited nodes by distances & by scores
            sorted_by_distance = [n for _, n in sorted(zip(distances, unvisited))]
            sorted_by_score = [n for _, n in sorted(zip(scores, unvisited), reverse=True)]

            # set next to the nearest node
            _next = sorted_by_distance[0]

            for node in sorted_by_score:
                # no need to check other nodes with lower score
                if _next == node:
                    break

                # go to a further node with better score, which difference of distance is not more than 40%
                if (self._matrix[curr][node] - self._matrix[curr][_next]) / self._matrix[curr][_next] <= 0.4:
                    # go only if the difference of score is not less than 2%
                    if (self._scores[node] - self._scores[_next]) / self._scores[_next] >= 0.02:
                        _next = node
                        break

            # visit next node
            cost += self._matrix[curr][_next]
            unvisited.remove(_next)
            route.append(_next)
            curr = _next

        self._best_route = route
        self._cost = cost
        self._solved = True

if __name__ == '__main__':
    adj_matrix = [
        [0, 1, 2, 3],
        [1, 0, 4, 5],
        [2, 4, 0, 6],
        [3, 5, 6, 0]
    ]

    # scores = {0: 10, 1: 30, 2: 50, 3: 50.00000001}  # [0,1,2,3] because score diff of 2 and 3 is 0.0000000002 (< 2%)
    scores = {0: 10, 1: 30, 2: 50, 3: 100}  # [0,1,3,2] because 3 has better score and distance diff is 25% (<= 40%)

    solver = NearestNeighbourSolver(adj_matrix, scores)

    print(solver.best_route())
    print(solver.cost())
