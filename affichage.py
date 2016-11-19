import matplotlib.pyplot as plt
from pca import pca
import numpy as np



markers_list = ["s", "o", "d", "x", "+", "p", "h", "H", "D", "*", "v", "^", "<", ">", "1", "2", "3", "4", "8"]
colors_list = ["r", "b", "g", "c", "m", "y", "k"]

nb_markers = len(markers_list)
nb_colors = len(colors_list)

def afficher_points(classifieur):
    p = classifieur.p
    p_ref = classifieur.p_ref
    nb_textes, nb_auteurs = p.shape
    nouveaux_vecteurs = pca([t.vecteur for t in classifieur.eval_set])
    textes_justes_par_auteur = [[] for j in range(nb_auteurs)]
    textes_faux_par_auteur = [[] for j in range(nb_auteurs)]
    for i in range(nb_textes):
        for j in range(nb_auteurs):
            if p[i,j] == 1:
                j_sup = j
            if p_ref[i,j] == 1:
                j_reel = j
        if j_sup == j_reel:
            textes_justes_par_auteur[j_sup].append(nouveaux_vecteurs[i])
        else:
            textes_faux_par_auteur[j_sup].append(nouveaux_vecteurs[i])
    for j in range(nb_auteurs):
        J = textes_justes_par_auteur[j]
        F = textes_faux_par_auteur[j]
        if len(J) > 0:
            XJ = [v[0] for v in J]
            YJ = [v[1] for v in J]
            plt.plot(XJ,YJ,linestyle = "None", color = colors_list[j], marker = markers_list[1])
        if len(F) > 0:
            XF = [v[0] for v in F]
            YF = [v[1] for v in F]
            plt.plot(XF, YF, linestyle="None", color=colors_list[j], marker=markers_list[2])
    plt.show()


p_ref = np.array([[1, 0, 0, 0],
                  [1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])

p = np.array([[0, 0, 1, 0],
              [1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 0, 1],
              [1, 0, 0, 0],
              [0, 0, 0, 1]])

vecteurs = [[0,1], [2,8], [8,2], [2,3], [7,1], [3,3]]

def test_afficher():
    nb_textes, nb_auteurs = p.shape
    nouveaux_vecteurs = pca(vecteurs)
    textes_justes_par_auteur = [[] for j in range(nb_auteurs)]
    textes_faux_par_auteur = [[] for j in range(nb_auteurs)]
    for i in range(nb_textes):
        for j in range(nb_auteurs):
            if p[i, j] == 1:
                j_sup = j
            if p_ref[i, j] == 1:
                j_reel = j
        if j_sup == j_reel:
            textes_justes_par_auteur[j_sup].append(nouveaux_vecteurs[i])
        else:
            textes_faux_par_auteur[j_sup].append(nouveaux_vecteurs[i])
    for j in range(nb_auteurs):
        J = textes_justes_par_auteur[j]
        F = textes_faux_par_auteur[j]
        if len(J) > 0:
            XJ = [v[0] for v in J]
            YJ = [v[1] for v in J]
            plt.plot(XJ, YJ, linestyle="None", color=colors_list[j], marker=markers_list[0])
        if len(F) > 0:
            XF = [v[0] for v in F]
            YF = [v[1] for v in F]
            plt.plot(XF, YF, linestyle="None", color=colors_list[j], marker=markers_list[1])
    plt.show()

#test_afficher()