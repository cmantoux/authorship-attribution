from time import time

from carac import *
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
from classes import Analyseur,Classifieur,Probleme
from Interpretation.importance_composantes import importance, gain_information
from Clustering.kmeans import Kmeans
from Apprentissage.svm import SVM
            

d = time()

oeuvres_training_set =[("dumas",1)]
oeuvres_eval_set1 = [("dumas",2)]
oeuvres_eval_set2 = [("zola",1)]
taille_morceaux = 5000
analyseur = Analyseur([freq_gram])
classifieur = Kmeans()

P = Probleme(oeuvres_training_set, oeuvres_eval_set1, taille_morceaux, analyseur, classifieur, langue = "fr")

P.oeuvres_eval_set[0].auteur = "dumasbis"

P.creer_textes(equilibrage = False)
P.analyser()
P.appliquer_classifieur()

importances = gain_information(classifieur.clusters)
ordre = sorted(list(range(nb_composantes)), key = lambda i : importances[i])

for t in P.liste_textes:
    t.vecteur = np.array([t.vecteur[ordre[i]] for i in range(nb_composantes)])

precisions = []
for k in range(0,nb_composantes,1):
    print(k)
    for t in P.liste_textes:
        t.vecteur = t.vecteur[:nb_composantes-k]
    classifieur.classifier(P.training_set,P.eval_set)
    precisions.append(classifieur.precision)

classifieur = Kmeans()

P = Probleme(oeuvres_training_set, oeuvres_eval_set2, taille_morceaux, analyseur, classifieur, langue = "fr")

P.creer_textes(equilibrage = False)
P.analyser()
P.appliquer_classifieur()

importances = gain_information(classifieur.clusters)
ordre = sorted(list(range(nb_composantes)), key = lambda i : importances[i])

for t in P.liste_textes:
    t.vecteur = np.array([t.vecteur[ordre[i]] for i in range(nb_composantes)])

precisions2 = []
for k in range(0,nb_composantes,1):
    print(k)
    for t in P.liste_textes:
        t.vecteur = t.vecteur[:nb_composantes-k]
    classifieur.classifier(P.training_set,P.eval_set)
    precisions2.append(classifieur.precision)

plt.plot(list(range(0,nb_composantes,1)), precisions)
plt.plot(list(range(0,nb_composantes,1)), precisions2)


f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")
