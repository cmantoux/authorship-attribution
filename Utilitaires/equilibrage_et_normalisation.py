# -*- coding: utf-8 -*-
from time import localtime
import numpy as np
import random
import math

def nb_time():
    lt = localtime()
    a = int(str(lt.tm_year) + str(lt.tm_yday) + str(lt.tm_mon) + str(lt.tm_mday) + str(lt.tm_hour))
    return a

seed = nb_time()

def get_seed():
    global seed
    return seed

def change_seed():
    global seed
    seed = random.randint(1,2**30-1)

def normaliser1(D):
    """ argument : une matrice D
        chaque ligne de la matrice D correspond à un point du feature space, autrement dit à un vecteur de données
        chaque colonne de la matrice D correspond à une composante des vecteurs de données
        cette fonction normalise en centrant et en réduisant chaque composante avec sa moyenne et son écart-type"""
    M = D.mean(axis = 0)
    V = D.var(axis = 0)
    A = np.zeros(D.shape)
    for i in range(D.shape[0]):
        for j in range(D.shape[1]):
            if V[j] == 0:
                A[i][j] = 0
            else:
                A[i][j] = (D[i][j] - M[j])/np.sqrt(V[j])
    for i in range(len(A)):
        for j in range(len(A[0])):
            if math.isnan(A[i,j]):
                A[i,j] = 0
    return A

def normaliser2(D):
    """ argument : une matrice D
        chaque ligne de la matrice D correspond à un point du feature space, autrement dit à un vecteur de données
        chaque colonne de la matrice D correspond à une composante des vecteurs de données
        cette fonction normalise par translation et dilatation affine : [min,max] devient [0,1]"""
    m = D.min(axis = 0)
    M = D.max(axis = 0)
    A = (D-m)/(M-m)
    return A


# M = np.arange(12).reshape(3,4)
#
# print(M)
#
# print(normaliser1(M))
# print(normaliser2(M))

def random_sample(seed,l,n):
    rs = seed
    l2 = []
    ind = []
    while len(l2)<n:
        x = rs % len(l)
        if x not in ind:
            l2.append(l[x])
            ind.append(x)
        rs = (1103515245 * rs + 12345) % (2**16)
    return l2

def equilibrer1(liste_textes):
    textes_par_auteur = {}
    for t in liste_textes:
        if t.auteur in textes_par_auteur.keys():
            textes_par_auteur[t.auteur].append(t)
        else:
            textes_par_auteur[t.auteur] = [t]
    n = min([len(l) for l in textes_par_auteur.values()])
    print("Graine utilisée : {}".format(seed))
    print("Nombre de textes par auteur après équilibrage : " + str(n))
    liste_textes2 = []
    for l in textes_par_auteur.values():
        liste_textes2.extend(random_sample(get_seed(),l,n))
    return liste_textes2

def equilibrer2(liste_textes):
    textes_par_auteur = {}
    for t in liste_textes:
        if t.auteur in textes_par_auteur.keys():
            textes_par_auteur[t.auteur].append(t)
        else:
            textes_par_auteur[t.auteur] = [t]
    n = min([len(l) for l in textes_par_auteur.values()])
    print("Nombre de textes par auteur après équilibrage : " + str(n))
    for a in textes_par_auteur.keys():
        while len(textes_par_auteur[a]) > n:
            s = random.sample(textes_par_auteur[a],2)
            t1 = s[0]
            t2 = s[1]
            v1 = np.array(t1.vecteur)
            v2 = np.array(t2.vecteur)
            v3 = (v1+v2)/2
            t1.vecteur = list(v3)
            textes_par_auteur[a].remove(t2)
    liste_textes2 = []
    for l in textes_par_auteur.values():
        liste_textes2.extend(l)
    return liste_textes2