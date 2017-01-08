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

print()
print("Test de SVM")

#P.classifieur = SVM()
#P.appliquer_classifieur()
#P.evaluer()

print()
print("Test de reseau_neurones")

#P.classifieur = reseau_neurones()
#P.appliquer_classifieur()
#P.evaluer()

print()
print("Test de Bayes")

#P.classifieur = Bayes()
#P.appliquer_classifieur()
#P.evaluer()

print()
print("Test de Apriori")

#P.classifieur = Apriori()
#P.appliquer_classifieur()
#P.evaluer()

print()
print("Test de Kmeans")

#P.classifieur = Kmeans()
#P.appliquer_classifieur()
#P.evaluer()

print()
print("Test de Kmedoids")

#P.classifieur = KMedoids()
#P.appliquer_classifieur()
#P.evaluer()

print()
print("Test de kPPV")

#P.classifieur = kPPV()
#P.appliquer_classifieur()
#P.evaluer()

#afficher_points(P.classifieur)

=======

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")
