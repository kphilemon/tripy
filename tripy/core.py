from typing import List, Dict


# adjacency_matrix param should contain the distance cost only
# this function takes in a Dict of sentiment score and incorporate it into the original distance cost
# the formula to calculate final cost:
# distance_weightage * (distance cost / max distance) + sentiment_weightage * sentiment score of destination city
def include_sentiment_score(adjacency_matrix: List[List[float]], sentiment_score: Dict,
                            distance_weightage: float = 0.5, sentiment_weightage: float = 0.5) -> List[List[float]]:
    n = len(adjacency_matrix)

    # make a deep copy and find out the max distance
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    max_distance = 0

    for i in range(n - 1):
        for j in range(i + 1, n):
            distance = adjacency_matrix[i][j]
            if distance > max_distance:
                max_distance = distance

            matrix[i][j] = matrix[j][i] = distance

    # i = from, j = to, adjacency_matrix[i][j] = cost from i to j
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_cost = matrix[i][j] / max_distance
                sentiment_cost = sentiment_score[j]
                matrix[i][j] = distance_weightage * distance_cost + sentiment_weightage * sentiment_cost

    return matrix
