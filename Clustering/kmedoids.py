import numpy as np
from classes import Classifieur

def distance(x,y):
    return np.sum(np.abs(x-y))


def build(l,k):
    N = len(l)
    
    dis = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            dis[i][j] = distance(l[i].vecteur,np.array(l[j].vecteur))
    
    S = []
    U = list(range(N))
            
    i0 = np.argmin(np.sum(dis,axis  = 0))
    S.append(i0)
    U.remove(i0)
    
    while len(S) < k:
        
        D = np.zeros((len(U)))
        for j in range(len(U)):
            d = [dis[U[j]][i] for i in S]
            D[j] = min(d)
            
        G = np.zeros((len(U)))
        
        for i in range(len(U)):
            g = sum([ max(D[j] - dis[U[i]][U[j]],0) for j in range(len(U))])
            G[i] = g
            
        i = U[np.argmax(G)]
        S.append(i)
        U.remove(i)
    
    return S,U,dis
    
def swap(S,U,dis):
    T = np.zeros((len(S),len(U)))
    D = np.zeros((len(U)))
    E = np.zeros((len(U)))
    while T.min() <= 0:
        
        for j in range(len(U)):
            d = [dis[U[j]][i] for i in S]
            D[j] = min(d)
            d.remove(D[j])
            E[j] = min(d)
        
        for i in range(len(S)):
            for h in range(len(U)):
                K = 0
                for j in range(len(U)):
                    if j!=h:
                        if dis[S[i]][U[j]] > D[j]:
                            K += min(dis[U[j]][U[h]] - D[j], 0)
                        else:
                            K += min(dis[U[j]][U[h]],E[j]) - D[j]
                T[i][h] = K
                
        (i,h) = np.unravel_index(T.argmin(), T.shape)
        print(T[i][h])
        if T[i][h]<0:
            xi = S[i]
            xh = U[h]
            S.append(xh)
            S.remove(xi)
            U.append(xi)
            U.remove(xh)
        
def clusterize(l,S,U,dis):
    
    c = [ [l[s]] for s in S]
    for j in range(len(U)):
        i = np.argmin([dis[U[j]][i] for i in S])
        c[i].append(l[U[j]])
    return c

class KMedoids(Classifieur):
    
    def __init__(self):
        print("Création du classifieur KMedoids")
        pass
    
    def classifier(self, liste_textes):
        auteurs_differents = set([texte.auteur for texte in liste_textes])
        k = len(auteurs_differents)
        S,U,dis = build(liste_textes,k)
        swap(S,U,dis)
        clusters = clusterize(liste_textes,S,U,dis)
        return clusters
        
    def afficher(self, liste_textes, clusters):
        print("Résultats du classificateur KMean sur le corpus étudié :")
        
        k = len(clusters)
        auteurs = list(set([texte.auteur for texte in liste_textes]))

        for i in range(k):
            nb_oeuvres_par_auteur = {}
            for auteur in auteurs:
                nb_oeuvres_par_auteur[auteur] = 0
                
            for t in clusters[i]:
                nb_oeuvres_par_auteur[t.auteur] +=1
            for auteur in auteurs:
                nb_oeuvres_par_auteur[auteur] =  "{0:.0f}%".format( 100 * nb_oeuvres_par_auteur[auteur] / len(clusters[i]))    
            print("Cluster numero {}".format(i+1))
            print(nb_oeuvres_par_auteur)
        

