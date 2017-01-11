import numpy as np

def defuzze(p):
    (N,k) = p.shape
    res = np.zeros((N,k))
    for i in range(N):
        j = np.argmax(p[i])
        res[i,j] = 1
    return res
