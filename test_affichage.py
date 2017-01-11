from time import time

d = time()

from carac import *
from classes import Analyseur, Probleme
from Clustering.kmeans import Kmeans
from Apprentissage.reseau_textes import reseau_neurones
from Apprentissage.svm import SVM
from Interpretation.importance_composantes import importance, gain_information

d = time()

oeuvres_training_set =[("proust",k) for k in range(1,3)] + [("balzac",k) for k in range(1,3)] + [("dumas",k) for k in range(1,3)]
oeuvres_eval_set = [("proust",k) for k in range(3,5)] + [("balzac",k) for k in range(3,5)] + [("dumas",k) for k in range(3,5)]
taille_morceaux = 4000


analyseur = Analyseur([freq_lettres, plus_courants])
classifieur = reseau_neurones()

P = Probleme(oeuvres_training_set, oeuvres_eval_set, taille_morceaux, analyseur, classifieur, langue = "fr")

#P.resoudre() equivalent a

P.creer_textes(equilibrage = False)
P.analyser(normalisation = True)
P.appliquer_classifieur()
P.afficher_graphique()
P.afficher_graphique(poids_composantes=importance)
print("coucou")
P.afficher_graphique(poids_composantes=gain_information)

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")

P.afficher()