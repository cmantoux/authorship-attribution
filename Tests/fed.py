import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from time import time
d = time()

from classes import *
from carac import *
from Apprentissage.svm import SVM

oeuvres_training =[("hamilton",k) for k in range(1,52)] + [("madison",k) for k in range(1,20)] 
oeuvres_eval = [("madison",k) for k in range(31,41)] 
analyseur = Analyseur([freq_gram, freq_ponct, freq_lettres, plus_courants, dif_plus_courants, longueur_mots])
classifieur = SVM()
P = Probleme(oeuvres_training, oeuvres_eval, 1, analyseur, classifieur, langue = "en", full_text = True)
P.resoudre()

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")