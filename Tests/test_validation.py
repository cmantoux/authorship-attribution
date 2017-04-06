from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/psc")
from carac_gramm import *
from carac_lettres import *
from carac_ponct import *
from carac_complexite import *
from carac_stopwords import *
from classes import *
from Clustering.kmeans import Kmeans
from Apprentissage.reseau_textes import reseau_neurones
from Apprentissage.svm import SVM
from Interpretation.importance_composantes import importance, gain_information


d = time()

id_oeuvres =[[("hugo",k) for k in range(3,9)], [("dumas",k) for k in range(3,9)]]
categories = ["categorie1"] + ["categorie2"]

taille_morceaux = 5000

a1 = Freq_Gram(langue = "fr")
a2 = Markov_Gram(langue = "fr",saut = 1)
a3 = Freq_Ngrammes(langue = "fr",n=1)
a4 = Markov_Lettres(langue = "fr")
a5 = Freq_Ponct(langue = "fr")
a6 = Longueur_Phrases()
a7 = Complexite_Grammaticale(langue = "fr", saut= 1)
a8 = Complexite_Vocabulaire()
a9 = Freq_Stopwords(langue = "fr")

liste_fonctions = [a5,a1,a9]
analyseur = Analyseur(liste_fonctions)

def createur_classifieur():
    return SVM()

C = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, createur_classifieur, pourcentage_eval = 0.1, nombre_essais = 20, leave_one_out = True)

C.resoudre()

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")