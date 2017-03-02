#import matplotlib.pyplot as plt

from Utilitaires.pca import pca
from carac import *
from classes import *

oeuvres = [('dumas', 1), ('dumas', 2), ('dumas', 3), ('dumas', 4), ('dumas', 5),
           ('maquet', 2), ('maquet', 3),
           ('maupassant', 1), ('maupassant', 2), ('maupassant', 3),
           ('hugo', 1),('hugo', 2), ('hugo', 3),
           ('proust', 1), ('proust', 2), ('proust', 3),
           ('balzac', 1), ('balzac', 2), ('balzac', 3)]  # Les trois mousquetaires : Dumas 5

"""
# Dérivée discrète
derivee_textes = []
for i in range(len(liste_textes)-1):
    derivee_textes.append(np.array(liste_textes[i+1].vecteur)-np.array(liste_textes[i].vecteur))

# Dérivée seconde discrète
derivee_seconde_textes = []
for i in range(len(derivee_textes)-1):
    derivee_seconde_textes.append(derivee_textes[i+1]-derivee_textes[i])"""


def c_n(y, time, period, n):
    c = y * np.exp(-1j * 2 * n * np.pi * time / period)
    return c.sum() / c.size


def fourier(tab, n_min, n_max):
    time = np.linspace(0, 1, len(tab))
    period = 1
    return [c_n(tab, time, period, n) for n in range(n_min, n_max)]


def fourier_texte(oeuvre, composante_max):
    taille_creneau = 1000

    liste_textes = []
    auteur = oeuvre.auteur
    numero = oeuvre.numero
    langue = oeuvre.langue

    L = len(oeuvre.tags)
    k = 0
    while k < min(100000, L) - taille_creneau:
        mots = oeuvre.mots[k:k + taille_creneau]
        texte_brut = " ".join(mots)
        racines = oeuvre.racines[k:k + taille_creneau]
        POS = oeuvre.POS[k:k + taille_creneau]
        T = Texte(auteur, numero, langue, k // taille_creneau, texte_brut, mots, racines, POS)
        liste_textes.append(T)
        k += taille_creneau // 10
        # print(k / (L - taille_creneau))

    analyseur = Analyseur([freq_gram, plus_courants, freq_ponct, freq_stopwords])

    for texte in liste_textes:
        analyseur.analyser(texte)

    vecteurs = []
    for texte in liste_textes:
        vecteurs.append(np.array(texte.vecteur))

    # Moyen-âge
    for i in range(len(vecteurs) - 5):
        vecteurs[i] = (vecteurs[i] + vecteurs[i + 1] + vecteurs[i + 2] + vecteurs[i + 3] + vecteurs[i + 5]) / 5

    # vecteurs = derivee_seconde_textes
    vecteurs = pca(vecteurs)

    # xr = [v[0] for v in vecteurs]
    # yr = [v[1] for v in vecteurs]

    return [fourier(vecteurs[i], 0, 5000) for i in range(min(len(vecteurs), composante_max))]


def norme_pondere(tab):
    return sum([(i**2)*abs(tab[i])**2 for i in range(len(tab))])

x_tab = []
y_tab = []
for o in oeuvres:
    oeuvre = Oeuvre(o[0], o[1])
    res = fourier_texte(oeuvre, 10)
    print(oeuvre.auteur)
    print(sum([norme_pondere(x)/10 for x in res]))
    print("=========")

