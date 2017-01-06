import numpy as np
from scipy.stats import gaussian_kde
from statsmodels.nonparametric.kde import KDEUnivariate
from sklearn.neighbors import KernelDensity
from scipy.integrate import quad


def importance(clusters):
    """la variable clusters est une liste où l'élément i est la liste des textes classifiés chez l'auteur numero i par l'algorithme}
        cette fonction estime le rôle de chaque composante des vecteurs dans la classification obtenue en comparant la variance moyenne de chaque composante au sein des clusters avec la distance inter-clusters => plus ce quotient est grand, plus la composante en question est pertinente"""
    nb_clusters = len(clusters)
    nb_composantes = len(clusters[0][0].vecteur)
    moyennes_clusters = []
    ecarts_intra_clusters = [0 for k in range(nb_composantes)]
    ecarts_inter_clusters = [0 for k in range(nb_composantes)]
    nb_clusters = 0
    for c in clusters:
        if len(c) > 0:
            nb_clusters+=1
            D = np.array([t.vecteur for t in c])
            M = D.mean(axis = 0)
            V = D.var(axis = 0)
            S = np.sqrt(V)
            moyennes_clusters.append(M)
            ecarts_intra_clusters += S
    ecarts_intra_clusters /= nb_clusters
    n = 0
    for i in range(nb_clusters):
        for j in range(nb_clusters):
            if i != j:
                n += 1
                M1 = moyennes_clusters[i]
                M2 = moyennes_clusters[j]
                dist = np.abs(M1 - M2)
                ecarts_inter_clusters += dist
    ecarts_inter_clusters = [e / n for e in ecarts_inter_clusters]
    importance_composantes = np.zeros((len(ecarts_inter_clusters)))
    for i in range(len(importance_composantes)):
        if ecarts_intra_clusters[i] == 0:
            importance_composantes[i] = 0
        else:
            importance_composantes[i] = ecarts_inter_clusters[i]/ecarts_intra_clusters[i]
    return importance_composantes


def entropie(vecteurs):
    """Retourne l'entropie d'un tableau de vecteurs dont les composantes sont supposées distribuées selon une gaussienne : va aider à calculer le gain en information de chaque composante"""
    E = np.log(np.var(vecteurs,axis = 0))
    for i in range(len(E)):
        if E[i] == - np.inf:
            E[i] = - 100000
    return E

def gain_information(clusters):
    nb_composantes = len(clusters[0][0].vecteur)
    S = sum(len(c) for c in clusters)
    gains = np.array([0. for k in range(nb_composantes)])
    info_intrinseque = np.array([0. for k in range(nb_composantes)])
    tous_vecteurs = []
    for c in clusters:
        vecteurs = [t.vecteur for t in c]
        Si = len(vecteurs)
        tous_vecteurs.extend(vecteurs)
        gains -= (Si/S)*entropie(vecteurs)
        info_intrinseque -= (Si/S)*np.log(Si/S)
    gains += entropie(tous_vecteurs)
    gains /= info_intrinseque
    return gains

