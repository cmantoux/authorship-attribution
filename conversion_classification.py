import numpy as np

def classification_to_clusters(classification):
    nb_textes = len(classification)
    auteurs = list(set([c[1] for c in classification]))
    nb_auteurs = len(auteurs)
    clusters = [[] for a in auteurs]
    for c in classification:
        t = c[0]
        vecteur = t.vecteur
        auteur_reel = c[1]
        auteur_suppose = c[2]
        clusters[auteurs.index(auteur_suppose)].append(t)
    return clusters

def classification_to_matrices(classification):
    nb_textes = len(classification)
    auteurs = list(set([item[1] for item in classification]))
    nb_auteurs = len(auteurs)
    p = np.zeros((nb_textes,nb_auteurs))
    p_ref = np.zeros((nb_textes,nb_auteurs))
    for i in range(nb_textes):
        item = classification[i]
        auteur_reel = item[1]
        auteur_suppose = item[2]
        p[i,auteurs.index(auteur_suppose)] = 1
        p_ref[i,auteurs.index(auteur_reel)] = 1
    return p,p_ref