from time import time

from Representation.affichage import afficher_points
from carac import *
from classes import Analyseur, Probleme
from Apprentissage.svm import SVM
from Apprentissage.reseau_textes import reseau_neurones


d = time()

oeuvres_training_set =[("zola",k) for k in range(1,3)] + [("balzac",k) for k in range(1,3)]
oeuvres_eval_set = [("zola",k) for k in range(3,5)] + [("balzac",k) for k in range(3,5)]
taille_morceaux = 1000
analyseur = Analyseur([freq_gram, plus_courants, freq_ponct, freq_stopwords])
classifieur = reseau_neurones()

P = Probleme(oeuvres_training_set, oeuvres_eval_set, taille_morceaux, analyseur, classifieur, langue = "fr", )

P.resoudre()

afficher_points(P.classifieur)

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")