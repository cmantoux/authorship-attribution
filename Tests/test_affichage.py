from time import time

from carac import freq_stopwords, freq_gram, freq_ponct
from classes import Analyseur, Probleme
from Apprentissage.svm import SVM

d = time()

oeuvres_training_set =[("zola",k) for k in range(1,3)] + [("balzac",k) for k in range(1,3)] + [("maupassant",k) for k in range(1,3)]
oeuvres_eval_set = [("maupassant",k) for k in range(3,5)] + [("balzac",k) for k in range(3,5)]
taille_morceaux = 1000

analyseur = Analyseur([freq_stopwords, freq_gram, freq_ponct])
classifieur = SVM()

P = Probleme(oeuvres_training_set, oeuvres_eval_set, taille_morceaux, analyseur, classifieur, langue = "fr")

#P.resoudre() equivalent a

P.creer_textes()
P.analyser()
P.appliquer_classifieur()


P.afficher()

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")