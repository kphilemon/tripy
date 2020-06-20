from typing import List, Dict
from math import inf
import matplotlib.pyplot as plt
import numpy as np
adj_matrix = [
        [0, 1, 2, 3],
        [1, 0, 4, 5],
        [2, 4, 0, 6],
        [3, 5, 6, 0]
    ]

scores = {0: 10, 1: 30, 2: 50, 3: 50.00000001}  # [0,1,2,3] because score diff of 2 and 3 is 0.0000000002 (< 2%)
scores = {0: 10, 1: 30, 2: 50, 3: 100} 

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


class ModifiedTspSolver(TspSolver):

    def __init__(self, adjacency_matrix: List[List[float]], score , start: int = 0) -> None:
        super().__init__(adjacency_matrix, start)

        # caching all routes to prevent expensive execution
        # key: cost, value: [[nodes of a route]]
        self._score=score
        self._routes = {}

    def min_cost(self) -> float:
        self._solve()
        return min(self._routes)

    def best_route(self) -> List[int]:
        self._solve()
        return self._routes[self.min_cost()][0]

    def routes(self):
    	self._solve()
    	return self._routes


    def _solve(self) -> None:
        if self._solved:
            return

        # starting point might have changed, so clear it first
        self._routes.clear()

        route = [self._start]
        nodes = [x for x in range(self._N) if x != self._start]
        self._tsp(route, nodes, 0)
        self._routes=self._score_calculation()

        # prevent re-execute
        self._solved = True
    def _score_calculation(self):
        route_modified_key = {}
        y, x = zip(*self._routes.items())
        total_distance = sum(y)
        if len(self._routes) == 1:
            route_modified_key = self._routes
        else:
            for key in self._routes:
                for i in self._routes[key]:
                    n = 2**len(self._matrix)
                    score = 0
                    for j in i:
                        score += self._score[j] * n
                        n /= 2
                    score += total_distance - key
                    if score in route_modified_key:
                        route_modified_key[score].append(i)
                    else:
                        route_modified_key[score] = [i]
        return route_modified_key
        
    # route param requires a list with starting node in it, else it will give key error
    def _tsp(self, route: List[int], nodes: List[int], cost: float) -> None:
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
        nearestNode = 0
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
                self._tsp(route=route + [nodes[n]], nodes=nodes[:n] + nodes[n + 1:],
                              cost=cost + self._matrix[route[-1]][nodes[n]])
            #if distance between node n and nearest node from current node, and sentiment score different more than 0.02
            if self._matrix[route[-1]][nodes[n]] - shortest_distance <= shortest_distance * 0.4:
                if self._score[nodes[n]] - self._score[nearest]  >= 0.02:
                    self._tsp(route=route + [nodes[n]], nodes=nodes[:n] + nodes[n + 1:],
                              cost=cost + self._matrix[route[-1]][nodes[n]])
# solver = ModifiedTspSolver(adj_matrix, scores)
# print(solver.routes())
KUALA_LUMPUR = 0
JAKARTA = 1
BANGKOK = 2
TAIPEI = 3
HONG_KONG = 4
TOKYO = 5
BEIJING = 6
SEOUL = 7

NAME_BY_INDEX = {
    KUALA_LUMPUR: 'KualaLumpur',
    JAKARTA: 'Jakarta',
    BANGKOK: 'Bangkok',
    TAIPEI: 'Taipei',
    HONG_KONG: 'HongKong',
    TOKYO: 'Tokyo',
    BEIJING: 'Beijing',
    SEOUL: 'Seoul'
}
class Sentiment_graph:
    def __init__(self):
        self.sentiment = {0: 10, 1: 30, 2: 50, 3: 50.00000001}

    def plot_graph(self,width):
        n = len(self.sentiment)
        x, y = zip(*self.sentiment.items())
        x1 = list(x)
        for i in range(len(x)):
            x1[i] = NAME_BY_INDEX[x[i]]

        index  = np.arange(n)
        plt.subplot(1,1,1)
        plt.bar(index, y)
        plt.ylabel("Sentiment Score")
        scale_factor = 0.2
        ymin, ymax = plt.ylim()
        plt.ylim(min(y) - 0.1, ymax)
        plt.title("Sentiment Score for all country")
        plt.xticks(index+width/2, x1)
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()

asd = Sentiment_graph()
asd.plot_graph(0.36)
