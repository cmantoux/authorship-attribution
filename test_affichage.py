from time import time
import numpy as np
from affichage import afficher_points

from classes import Oeuvre,Texte,Analyseur,Classifieur,Probleme

from svm import SVM

from carac import *

d = time()

liste_id_oeuvres =[("zola",k) for k in range(1,12)] + [("balzac",k) for k in range(1,8)]
taille_morceaux = 7000
analyseur = Analyseur([freq_gram, plus_courants, freq_ponct, freq_stopwords])
classifieur = SVM()

P = Probleme(liste_id_oeuvres, taille_morceaux, analyseur, classifieur)

P.resoudre()

#afficher_points(P.classifieur)

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")