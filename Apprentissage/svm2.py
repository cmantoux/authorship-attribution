import numpy as np
import numpy.linalg as alg

def k(x,y):
    return np.dot(x,y)

X = np.array([[1,2,3], [2,8,1], [4,9,9], [7,1,2], [-1,-2,-4], [-3,-3,-3], [-1,0,-9]])
Y = np.array([1,1,1,1,-1,-1,-1])
lam = 1
w = np.array([0,1,2])
b = 3

def f(w,b):
    n = X.shape[0]
    S = 0
    for i in range(n):
        S += max(0,1-Y[i]*(k(X[i],w)-b))
    S /= n
    S += lam*np.square(alg.norm(w))
    return S