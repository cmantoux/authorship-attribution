import matplotlib.pyplot as plt

from Utilitaires.pca import pca
from carac import *
from classes import *

oeuvre = Oeuvre('maupassant', 5)  # Les trois mousquetaires : Dumas 5

taille_creneau = 10000

liste_textes = []
auteur = oeuvre.auteur
numero = oeuvre.numero
langue = oeuvre.langue

L = len(oeuvre.tags)
k = 0
while k < min(100000,L)-taille_creneau:
    mots = oeuvre.mots[k:k+taille_creneau]
    texte_brut = " ".join(mots)
    racines = oeuvre.racines[k:k+taille_creneau]
    POS = oeuvre.POS[k:k+taille_creneau]
    T = Texte(auteur, numero, langue, k // taille_creneau, texte_brut, mots, racines, POS)
    liste_textes.append(T)
    k += taille_creneau // 100
    print(k/(L-taille_creneau))

analyseur = Analyseur([freq_gram, plus_courants, freq_ponct, freq_stopwords])

k = 0
for texte in liste_textes:
    analyseur.analyser(texte)
    print(k/len(liste_textes))
    k += 1

vecteurs = []
k = 0
for texte in liste_textes:
    vecteurs.append(np.array(texte.vecteur))
    print(k/len(liste_textes))
    k += 1

# Moyen-âge
k = 0
for i in range(len(vecteurs)-5):
    vecteurs[i] = (vecteurs[i]+vecteurs[i+1]+vecteurs[i+2]+vecteurs[i+3]+vecteurs[i+5])/5
    print(k/len(liste_textes))
    k += 1

"""
# Dérivée discrète
derivee_textes = []
for i in range(len(liste_textes)-1):
    derivee_textes.append(np.array(liste_textes[i+1].vecteur)-np.array(liste_textes[i].vecteur))

# Dérivée seconde discrète
derivee_seconde_textes = []
for i in range(len(derivee_textes)-1):
    derivee_seconde_textes.append(derivee_textes[i+1]-derivee_textes[i])"""


# vecteurs = derivee_seconde_textes
vecteurs = pca(vecteurs)
print("PCA terminée")
plt.plot([v[0] for v in vecteurs], [v[1] for v in vecteurs])
plt.show()
