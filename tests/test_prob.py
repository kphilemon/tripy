# from typing import List, Dict
# from math import inf

# adj_matrix = [
#         [0, 1, 0.6, 0.5],
#         [1, 0, 4, 5],
#         [2, 4, 0, 6],
#         [3, 5, 6, 0]
#     ]
# scores = {0: 10, 1: 30, 2: 50, 3: 40}

# class TspSolver:
#     def __init__(self, adjacency_matrix: List[List[float]], start: int = 0) -> None:
#         if len(adjacency_matrix) <= 2:
#             raise Exception('TSP on 0, 1, or 2 nodes does not make any sense!')
#         if len(adjacency_matrix) != len(adjacency_matrix[0]):
#             raise Exception('Square matrix required for adjacency matrix!')
#         if not 0 <= start < len(adjacency_matrix):
#             raise IndexError('Starting node must be 0 <= s < N!')

#         self._matrix = adjacency_matrix
#         self._start = start  # starting node
#         self._solved = False
#         self._N = len(self._matrix)

#     @property
#     def start(self) -> int:
#         return self._start

#     @start.setter
#     def start(self, start: int) -> None:
#         if self._start != start:
#             if not 0 <= start < self._N:
#                 raise IndexError('Starting node must be 0 <= s < N!')

#             self._start = start
#             self._solved = False  # flag to false so that the algorithm can be execute again

#     def min_cost(self) -> float:
#         raise NotImplementedError('Min cost method not implemented!')

#     def best_route(self) -> List[int]:
#         raise NotImplementedError('Best route method not implemented!')


# class NaiveTspSolver(TspSolver):

#     def __init__(self, adjacency_matrix: List[List[float]], score , start: int = 0) -> None:
#         super().__init__(adjacency_matrix, start)

#         # caching all routes to prevent expensive execution
#         # key: cost, value: [[nodes of a route]]
#         self._score=score
#         self._routes = {}

#     def min_cost(self) -> float:
#         self._solve()
#         return min(self._routes)

#     def best_route(self) -> List[int]:
#         self._solve()
#         return self._routes[self.min_cost()][0]

#     def routes(self):
#     	self._solve()
#     	return self._routes


#     def _solve(self) -> None:
#         if self._solved:
#             return

#         # starting point might have changed, so clear it first
#         self._routes.clear()

#         route = [self._start]
#         nodes = [x for x in range(self._N) if x != self._start]
#         self._tsp(route, nodes, 0)

#         # prevent re-execute
#         self._solved = True

#     # route param requires a list with starting node in it, else it will give key error
#     def _tsp(self, route: List[int], nodes: List[int], cost: float) -> None:
#         if len(nodes) == 0:
#             cost = round(cost, 4)
#             if cost in self._routes:
#                 self._routes[cost].append(route)
#             else:
#                 self._routes[cost] = [route]
#             return
#         nearest = 0
#         shortestD = inf
#         for m in range(len(nodes)):
#         	if self._matrix[route[-1]][nodes[m]] < shortestD:
#         		shortestD = self._matrix[route[-1]][nodes[m]]
#         		nearest = nodes[m]

#         print("nearest", nearest)
#         print("shortest", shortestD)
#         for n in range(len(nodes)):
#         	if nodes[n] == nearest:
#         		print("yo: ", n)
#         		self._tsp(route=route + [nodes[n]], nodes=nodes[:n] + nodes[n + 1:],
# 		                      cost=cost + self._matrix[route[-1]][nodes[n]])
#         	if self._matrix[route[-1]][nodes[n]] - shortestD <= shortestD * 0.4:
#         		print("almost", nodes[n])
#         		print("n: ", self._score[nodes[n]], "nearest: ", self._score[nearest])
#         		print (self._score[nodes[n]] -self._score[nearest] >= 0.02)
#         		if self._score[nodes[n]] -self._score[nearest] >= 0.02:
#         			print("nanii :" ,n)
#         			self._tsp(route=route + [nodes[n]], nodes=nodes[:n] + nodes[n + 1:], cost=cost + self._matrix[route[-1]][nodes[n]])

