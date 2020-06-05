from typing import List, Dict


# adjacency_matrix param should contain the distance cost only
# this function takes in a Dict of analysis and incorporate it into the original distance cost
# the formula to calculate cost:
# distance_weightage * distance cost + sentiment_weightage * sentiment cost of destination city
def include_sentiment_analysis(adjacency_matrix: List[List[float]], analysis: Dict,
                               distance_weightage: float = 0.5, sentiment_weightage: float = 0.5) -> List[List[float]]:

    n = len(adjacency_matrix)

    # i = from, j = to, adjacency_matrix[i][j] = cost from i to j
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_cost = adjacency_matrix[i][j]
                sentiment_cost = analysis[j]
                adjacency_matrix[i][j] = distance_weightage * distance_cost + sentiment_weightage * sentiment_cost

    return adjacency_matrix
