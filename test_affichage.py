from time import time

d = time()

from Representation.affichage import afficher_points
from carac import *
from classes import Analyseur, Probleme
from Apprentissage.svm import SVM
from Apprentissage.Bayes import Bayes
from Apprentissage.reseau_textes import reseau_neurones
from Apprentissage.Apriori import Apriori
from Clustering.kmeans import Kmeans
from Clustering.kmedoids import KMedoids
from Clustering.kPPV import kPPV

d = time()

oeuvres_training_set =[("zola",k) for k in range(1,3)] + [("balzac",k) for k in range(1,3)] + [("maupassant",k) for k in range(1,3)]
oeuvres_eval_set = [("zola",k) for k in range(3,5)] + [("balzac",k) for k in range(3,5)]
taille_morceaux = 3000
analyseur = Analyseur([freq_gram, plus_courants, freq_ponct, freq_stopwords])
classifieur = SVM()

P = Probleme(oeuvres_training_set, oeuvres_eval_set, taille_morceaux, analyseur, classifieur, langue = "fr")

#P.resoudre() equivalent a

P.creer_textes(equilibrage = False)
P.analyser(normalisation = True)
P.appliquer_classifieur()

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")

P.afficher_graphique()