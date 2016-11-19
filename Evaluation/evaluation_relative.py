import numpy as np

def distance(texte1, texte2):
    """ Distance entre les textes passés en arguments """
    
    return np.linalg.norm(texte1.vecteur - np.array(texte2.vecteur))

def distance_clusters_SL(textes,p,i,j):
    """ Distance single-linkage entre les clusters i et j """
    m=float("inf")
    for k in np.where(p[:,i] ==1)[0]:
        for l in np.where(p[:,j] ==1)[0]:
            m = min(m,distance(textes[k],textes[l]))
    return m


def huberts_relatif(textes,p):
    """ Statistique de Huberts relative pour la partition p"""
    N = len(textes)
    M = N*(N-1)/1

    num_clusters = [np.where(p[i] ==1)[0][0] for i in range(N)]
   
    gamma = 0
    for i in range(N):
        for j in range(i+1,N):
            gamma += distance(textes[i],textes[j]) * distance_clusters_SL(textes,p,num_clusters[i],num_clusters[j])
    return gamma/M
 
def diametre_cluster(textes,p,i):
    m=0
    for k in np.where(p[:,i] ==1)[0]:
        for l in np.where(p[:,i] ==1)[0]:
            m = max(m, distance(textes[k],textes[l]))
    return m
    
def dunn(textes,p):
    k = len(p[0])
    dis = np.zeros((k,k))
    diam = np.zeros((k))
    for i in range(k):
        diam[i] = diametre_cluster(textes,p,i)
        for j in range(k):
            dis[i][j] = distance_clusters_SL(textes,p,i,j)
    
    M = float("inf")
    for i in range(k):
        m = float("inf")
        for j in range(k):
            if j!=i:
                m = min(m, dis[i][j] / diam[i])
        M = min(m,M)
        
    return M

def barycentre(textes,p,i):
    d = len(textes[0].vecteur)
    idx = np.where(p[:,i] ==1)[0]
    s = np.zeros((d))
    for j in idx:
        s+=textes[j].vecteur
    return s/len(idx)

def distance_clusters_AL(textes,p,i,j):
    
    return np.linalg.norm(barycentre(textes,p,i) - barycentre(textes,p,j))

def variance_cluster(textes,p,i):
    s = barycentre(textes,p,i)
    idx = np.where(p[:,i] ==1)[0]
    v = sum([np.linalg.norm(textes[j].vecteur - s)**2 for j in idx])
    return v
    

def davies_bouldin(textes,p):
    k = len(p[0])
    dis = np.zeros((k,k))
    v = np.zeros((k))
    for i in range(k):
        v[i] = variance_cluster(textes,p,i)
        for j in range(k):
            dis[i][j] = distance_clusters_AL(textes,p,i,j)
    
    s = 0
    for i in range(k):
        m = 0
        for j in range(k):
            if i!=j:
                m = max(m, (v[i]+v[j]/dis[i][j]))
        s+=m
    return s/k
    