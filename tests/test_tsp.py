import time

from tripy.algorithms.tsp import DpTspSolver, NaiveTspSolver
import tripy.geo.distance as distance
import tripy.geo.locations as locations

if __name__ == '__main__':
    # adj_matrix = [
    #     [0, 0.268188, 1.0861600, 0.284266, 2.1870300, 2.90507, 1.06443, 0.641625, 0.191624, 3.44142],
    #     [0.1609330, 0, 0.6911510, 0.464564, 1.4049800, 1.96431, 0.168696, 0.654258, 1.41509, 2.98196],
    #     [0.3580770, 0.379707, 0, 1.249930, 0.0821726, 0.408356, 1.74232, 2.37079, 2.95341, 3.90037],
    #     [0.0818823, 0.223001, 1.0921200, 0, 2.1872100, 2.89526, 0.942284, 0.56915, 0.872503, 2.75427],
    #     [0.3714430, 0.397651, 0.0423335, 1.289620, 0, 0.315516, 1.82914, 2.46966, 3.06793, 3.87276],
    #     [0.4166200, 0.46945, 0.1776410, 1.441470, 0.2664210, 0, 2.15881, 2.82956, 3.44337, 3.90929],
    #     [0.1427810, 0.0377101, 0.7089300, 0.438806, 1.4446600, 2.01924, 0, 0.526249, 1.24782, 3.13342],
    #     [0.0799607, 0.135875, 0.8962080, 0.246239, 1.8121500, 2.45884, 0.488912, 0, 0.76215, 3.14592],
    #     [0.0228630, 0.281361, 1.0688800, 0.361399, 2.1552200, 2.86474, 1.10989, 0.729676, 0, 3.6366],
    #     [0.4020280, 0.580519, 1.3821200, 1.117020, 2.6638000, 3.18444, 2.72886, 2.94897, 3.56066, 0],
    # ]

    # adj_matrix = [
    #     [0, 2, 9, 10],
    #     [1, 0, 6, 4],
    #     [15, 7, 0, 8],
    #     [6, 3, 12, 0]
    # ]

    # adj_matrix = [
    #     [0, 0.268188, 1.0861600, 0.284266, 2.1870300, 2.90507, 1.06443, 0.641625],
    #     [0.1609330, 0, 0.6911510, 0.464564, 1.4049800, 1.96431, 0.168696, 0.654258],
    #     [0.3580770, 0.379707, 0, 1.249930, 0.0821726, 0.408356, 1.74232, 2.37079],
    #     [0.0818823, 0.223001, 1.0921200, 0, 2.1872100, 2.89526, 0.942284, 0.56915],
    #     [0.3714430, 0.397651, 0.0423335, 1.289620, 0, 0.315516, 1.82914, 2.46966],
    #     [0.4166200, 0.46945, 0.1776410, 1.441470, 0.2664210, 0, 2.15881, 2.82956],
    #     [0.1427810, 0.0377101, 0.7089300, 0.438806, 1.4446600, 2.01924, 0, 0.526249],
    #     [0.0799607, 0.135875, 0.8962080, 0.246239, 1.8121500, 2.45884, 0.488912, 0],
    # ]
    #
    # dp = DpTspSolver(adj_matrix)
    # naive = NaiveTspSolver(adj_matrix)
    #
    # for solver in (dp, naive):
    #     start = time.perf_counter()
    #     for i in range(len(adj_matrix)):
    #         solver.start = i
    #         print('Starting node:', solver.start)
    #         print('Best route:', solver.best_route())
    #         print('Cost:', solver.min_cost())
    #     end = time.perf_counter()
    #
    #     print(f'elapsed time: {end - start}')
    #     print(f'average time: {(end - start) / len(adj_matrix)}\n')

    m = distance.adjacency_matrix()
    solver = DpTspSolver(m)

    _sum = 0
    for i in range(len(m)):
        start = time.perf_counter()
        solver.start = i
        print(f'Starting node: {locations.NAME_BY_INDEX[i]}')
        print(f'Best route: {locations.indices_to_names(*solver.best_route())}')
        print(f'Cost: {solver.min_cost()}km')
        end = time.perf_counter()
        elapsed = end - start
        _sum += elapsed
        print(f'Elapsed time: {elapsed}\n')

    print(f'Average time: {_sum / len(m)}')
