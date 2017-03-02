# -*- coding: utf-8 -*-
import numpy as np



def distance(texte1, texte2):
    """ Distance entre les textes passés en arguments """
    
    return np.linalg.norm(texte1.vecteur - np.array(texte2.vecteur))


def huberts_interne(textes,p):
    """ Statistique de Huberts interne pour la partition p"""
    N = len(textes)
    M = N*(N-1)/1
    num_clusters = [np.where(p[i] ==1)[0][0] for i in range(N)]
    
    gamma = 0
    for i in range(N):
        for j in range(i+1,N):
            gamma += distance(textes[i],textes[j]) * (1-int(num_clusters[i] == num_clusters[j]))
    return gamma/M