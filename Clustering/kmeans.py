import numpy as np
from classes import Classifieur
from Utilitaires.pca import pca
import matplotlib.pyplot as plt

def distance(x,y):
    """Calcule la distance entre les vecteurs x et y."""
    return np.linalg.norm(y-x)

def mean(l):
    """Calcule le vecteur isobarycentre de la liste de textes l."""
    N = len(l)
    s = np.sum([t.vecteur for t in l], axis = 0)
    return s/N

def centroids_init(l,k):
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
    
    return [np.array(l[s].vecteur) for s in S]

def k_means(l,k):
    """Cette fonction retourne une partion en k clusters de la liste de textes déterminé par l'algorithme des k_moyennes"""

    new_centroids = centroids_init(l,k)
    old_centroids = np.array([new_centroids[0]]* k)
    
    while distance(new_centroids,old_centroids) !=0:
        
        clusters = [[] for i in range(k)]
        
        for t in l:
            i = np.array([distance(t.vecteur,new_centroids[j]) for j in range(k)]).argmin()
            clusters[i].append(t)
        
        old_centroids = np.copy(new_centroids)
        for i in range(k):
            new_centroids[i] = mean(clusters[i])
        
    return clusters
    
markers_list = ["o", "s", "p", "*", "h", "H", "+", "x", "D", "d", "v", "^", "<", ">", "1", "2", "3", "4", "8"]
colors_list = ["b", "g", "r", "c", "m", "y", "k"]

nb_markers = len(markers_list)
nb_colors = len(colors_list)

def clusters_plot(clusters):
    """ Cette fonction dessine en 2D chaque cluster de la liste des clusters passée en argument"""
    plt.close()
    k = len(clusters)
    vecteurs = []
    for c in clusters:
        for t in c:
            vecteurs.append(t.vecteur)
    vecteurs = pca(vecteurs)
    x = 0
    for i in range(k):
        A = []
        B = []
        for t in clusters[i]:
            v = vecteurs[x]
            A.append(v[0])
            B.append(v[1])
            x+=1
        plt.plot(A,B,'.',color = colors_list[i % nb_colors], label = 'cluster {}'.format(i))
    plt.legend(loc = 'best')
    plt.show()

    
class Kmeans(Classifieur):
    
    def __init__(self):
        print("Création du classifieur KMeans")
        pass
    
    def classifier(self, training_set, eval_set):
        self.liste_textes = training_set + eval_set
        self.eval_set = eval_set
        self.training_set = training_set
        auteurs = list(set([texte.auteur for texte in self.liste_textes]))
        k = len(auteurs)
        clusters = k_means(self.liste_textes,k)
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


        