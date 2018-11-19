import numpy as np

def floyd_warshall(adj_matrix):
    V = adj_matrix.shape[0]
    for k in xrange(V):
        for i in xrange(V):
            for j in xrange(V):
                adj_matrix[i][j] = min(adj_matrix[i][j], adj_matrix[i][k],
                        adj_matrix[k][j])
    return adj_matrix

