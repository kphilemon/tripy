from tripy.algorithms.nn import NearestNeighbourSolver

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
