from typing import List
from geopy.distance import distance

from tripy.geo.locations import ALL_LOCATIONS, COORDINATES_BY_INDEX


def adjacency_matrix() -> List[List[float]]:
    n = len(ALL_LOCATIONS)
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n - 1):
        for j in range(i + 1, n):
            matrix[i][j] = matrix[j][i] = distance_km(i, j)

    return matrix


def distance_km(a: int, b: int) -> float:
    if a not in ALL_LOCATIONS:
        raise ValueError('First location not supported!')
    if b not in ALL_LOCATIONS:
        raise ValueError('Second location not supported!')

    return distance(COORDINATES_BY_INDEX[a], COORDINATES_BY_INDEX[b]).km


if __name__ == '__main__':
    m = adjacency_matrix()

    for row in m:
        print(row)

