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
    
    def classifier(self, training_set, eval_set):
        self.liste_textes = training_set + eval_set
        self.eval_set = eval_set
        self.training_set = training_set
        auteurs = list(set([texte.auteur for texte in self.liste_textes]))
        k = len(auteurs)
        S,U,dis = build(self.liste_textes,k)
        swap(S,U,dis)
        clusters = clusterize(self.liste_textes,S,U,dis)
        auteurs_par_cluster = ["?" for i in range(k)]
        for j in range(k):
            nb_oeuvres_par_auteur = {}
            for auteur in auteurs:
                nb_oeuvres_par_auteur[auteur] = 0
            for t in clusters[j]:
                nb_oeuvres_par_auteur[t.auteur] +=1
            auteur_max = "?"
            nb_max = 0
            for auteur in auteurs:
                if nb_oeuvres_par_auteur[auteur] > nb_max :
                    nb_max = nb_oeuvres_par_auteur[auteur]
                    auteur_max = auteur
            auteurs_par_cluster[j] = auteur_max
        n = len(self.eval_set)
        self.precision = 0
        self.p = np.zeros((n,k))
        self.p_ref = np.zeros((n,k))
        for i in range(n):
            t = self.eval_set[i]
            auteur_reel = t.auteur
            for j in range(k):
                if t in clusters[j]:
                    auteur_suppose = auteurs_par_cluster[j]
            j_reel = auteurs.index(auteur_reel)
            j_sup = auteurs.index(auteur_suppose)
            self.p[i,j_sup] = 1
            self.p_ref[i,j_reel] = 1
            if j_sup == j_reel :
                self.precision += 1
        self.precision /= n
        self.clusters = clusters
        
    def afficher(self):
        print("Résultats du classificateur KMean sur le corpus étudié :")
        print("Précision : " + str(self.precision))
        

