import numpy as np
from Utilitaires import product

def freqs(X,items):
    res = np.zeros((len(items)))
    for x in X:
        if x in items:
            res[items.index(x)]+=1
    S = np.sum(res)
    if (S>0):
        res = res / np.sum(res)
    return list(res)

def markov(saut,X,states):

    Nij = np.zeros((len(states),len(states)))
    N = np.zeros((len(states)))

    res = []

    for i in range(len(X)-saut):
        if (X[i] in states and  X[i+saut] in states):
            Nij[states.index(X[i]),states.index(X[i+saut])] +=1
            N[states.index(X[i])]+=1
    for i in range(len(states)):
        if (N[i]>0):
            Nij[i, :] /= N[i]

    for i in range(len(states)):
        for j in range(len(states)):
            res.append(Nij[i,j])

    return res

def serie_temporelle(X,s):
    idx = np.where(X==s)[0]
    v = idx[1:]-idx[:-1]
    return [np.mean(v),np.std(v),np.min(v),np.max(v),np.percentile(v,25),np.percentile(v,50),np.percentile(v,75)]

def log_serie_temporelle(X,s):
    idx = np.where(X==s)[0]
    v = idx[1:]-idx[:-1]
    v = np.log(v)
    moy = np.mean(v)
    sig = np.std(v)
    u3 = np.mean(np.power(v-moy,3))
    u4 = np.mean(np.power(v-moy,4))
    S = u3/(sig**3)
    K = u4/(sig**4)
    return [moy,sig,S,K]