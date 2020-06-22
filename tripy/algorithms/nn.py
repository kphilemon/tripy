from typing import List, Dict
from tripy.algorithms.tsp import TspSolver
from math import inf

# this nearest neighbour algorithm is a variant that makes decision with additional information (sentiment score)
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


class ModifiedNearestNeighbourSolver(TspSolver):

    def __init__(self, adjacency_matrix: List[List[float]], score, start: int = 0) -> None:
        super().__init__(adjacency_matrix, start)

        # caching all routes to prevent expensive execution
        # key: cost, value: [[nodes of a route]]
        self._routes = {}
        self._score = score

    def all_route(self) -> Dict:
        self._solve()
        return self._routes

    def max_score(self) -> float:
        self._solve()
        return max(self._routes)

    def best_route(self) -> List[int]:
        self._solve()
        return self._routes[self.max_score()][0]

    def _solve(self) -> None:
        if self._solved:
            return

        # starting point might have changed, so clear it first
        self._routes.clear()

        route = [self._start]
        nodes = [x for x in range(self._N) if x != self._start]
        self._nnsolver(route, nodes, 0)
        self._routes=self._score_calculation()

        # prevent re-execute
        self._solved = True

    def _score_calculation(self):
        route_modified_score = {}
        y, x = zip(*self._routes.items())
        total_distance = sum(y)
        y = [total_distance - i for i in y]
        total_total_distance = sum(y)
        total_score = 0
        for key in self._routes:
            for i in self._routes[key]:
                n = 5**len(self._matrix)
                score = 0
                for j in i:
                    score += self._score[j] * n
                    n /= 5
                total_score += score

        if len(self._routes) == 1:
            route_modified_score = self._routes
        else:
            for key in self._routes:
                for i in self._routes[key]:
                    n = 5**len(self._matrix)
                    score = 0
                    for j in i:
                        score += self._score[j] * n
                        n /= 5
                    print("-----------------------score: ", score/total_score, "\n----------------------distance: ",(total_distance - key)/total_total_distance)
                    score =(score/total_score) + ((total_distance - key)/total_total_distance)
                    print("-----------------------combined: ", score)
                    if score in route_modified_score:
                        route_modified_score[score].append(i)
                    else:
                        route_modified_score[score] = [i]
        return route_modified_score
        
    # route param requires a list with starting node in it, else it will give key error
    def _nnsolver(self, route: List[int], nodes: List[int], cost: float) -> None:
        if len(nodes) == 0:
            cost = round(cost, 4)
            if cost in self._routes:
                self._routes[cost].append(route)
            else:
                self._routes[cost] = [route]
            return
        #Get the nearest node from current node
        shortest_distance = inf
        furthest_distance = 0
        nearest = 0
        highestScore = 0
        for m in range(len(nodes)):
            if self._matrix[route[-1]][nodes[m]] < shortest_distance:
                shortest_distance = self._matrix[route[-1]][nodes[m]]
                nearest = nodes[m]
            if self._score[nodes[m]] > highestScore:
                highestScore = self._score[nodes[m]]
            if self._matrix[route[-1]][nodes[m]] > furthest_distance:
                furthest_distance = self._matrix[route[-1]][nodes[m]]

        for n in range(len(nodes)):
            if nodes[n] == nearest:
                self._nnsolver(route=route + [nodes[n]], nodes=nodes[:n] + nodes[n + 1:],
                              cost=cost + self._matrix[route[-1]][nodes[n]])
            #if distance between node n and nearest node from current node, and sentiment score different more than 0.02
            elif self._matrix[route[-1]][nodes[n]] - shortest_distance <= shortest_distance * 0.4:
                if self._score[nodes[n]] - self._score[nearest]  >= self._score[nearest] * 0.02:
                    self._nnsolver(route=route + [nodes[n]], nodes=nodes[:n] + nodes[n + 1:],
                              cost=cost + self._matrix[route[-1]][nodes[n]])