from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from carac import *
from classes import Analyseur, Probleme
from Clustering.kmeans import Kmeans
from Apprentissage.reseau_textes import reseau_neurones
from Apprentissage.svm import SVM
from Interpretation.importance_composantes import importance, gain_information


d = time()

id_training_set =[[("proust",k) for k in range(1,3)], [("balzac",k) for k in range(1,3)]]
categories = ["categorie1"] + ["categorie2"]
id_eval_set = [[("proust",k) for k in range(3,5)] ,[("balzac",k) for k in range(3,5)]]
categories_supposees = ["categorie1"] + ["categorie2"]

taille_morceaux = 5000

analyseur = Analyseur([freq_ponct, freq_gram])
classifieur = SVM()


P = Probleme(id_training_set, categories, id_eval_set, categories_supposees, taille_morceaux, analyseur, classifieur, langue = "fr")

#P.resoudre() equivalent a

P.creer_textes()
P.analyser()
P.appliquer_classifieur()
P.afficher()
P.interpreter()
#P.afficher_graphique()

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")