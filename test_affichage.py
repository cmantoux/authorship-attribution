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

oeuvres_training_set = [("balzac",k) for k in range(1,2)] + [("maupassant",k) for k in range(1,2)]
oeuvres_eval_set =  [("balzac",k) for k in range(3,4)] + [("maupassant",k) for k in range(3,4)]
taille_morceaux = 1000
analyseur = Analyseur([freq_gram, plus_courants, freq_ponct])
classifieur = SVM()

P = Probleme(oeuvres_training_set, oeuvres_eval_set, taille_morceaux, analyseur, classifieur, langue = "fr")

#P.resoudre() equivalent a

P.creer_textes(equilibrage = False)
P.analyser(normalisation = True)
P.appliquer_classifieur()
P.evaluer()
P.interpreter()

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")
