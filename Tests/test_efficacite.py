from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/psc")
from Carac.carac_gramm import *
from Carac.carac_lettres import *
from Carac.carac_ponct import *
from Carac.carac_complexite import *
from Carac.carac_stopwords import *
from classes import *
from Apprentissage.svm import SVM
from Apprentissage.Bayes import Bayes
from Apprentissage.reseau_textes import reseau_neurones
from Clustering.kmeans import Kmeans
from Clustering.kmedoids import KMedoids
from Interpretation.importance_composantes import importance, gain_information
from Evaluation import evaluation_externe as ee
import random
import numpy as np
import matplotlib.pyplot as plt

a1 = Freq_Gram(langue = "fr")

a2 = Markov_Gram(langue = "fr",saut=1)
a21 = Markov_Gram(langue = "fr",saut=1)
a22 = Markov_Gram(langue = "fr",saut=2)
a23 = Markov_Gram(langue = "fr",saut=3)
a24 = Markov_Gram(langue = "fr",saut=4)

a3 = Freq_Ngrammes(langue = "fr",n=1)
a31 = Freq_Ngrammes(langue = "fr",n=1)
a32 = Freq_Ngrammes(langue = "fr",n=2)
a33 = Freq_Ngrammes(langue = "fr",n=3)
a34 = Freq_Ngrammes(langue = "fr",n=4)

a4 = Markov_Lettres(langue = "fr")
a5 = Freq_Ponct(langue = "fr")
a6 = Freq_Stopwords(langue = "fr")

a7 = Complexite_Grammaticale(langue = "fr", saut=1)
a71 = Complexite_Grammaticale(langue = "fr", saut=1)
a72 = Complexite_Grammaticale(langue = "fr", saut=2)
a73 = Complexite_Grammaticale(langue = "fr", saut=3)
a74 = Complexite_Grammaticale(langue = "fr", saut=4)

a8 = Complexite_Vocabulaire()
a9 = Longueur_Phrases()

aGram = Analyseur("Grammaire",[a1])
aLettres= Analyseur("Lettres",[a3,a4])
aPonct = Analyseur("Ponctuation",[a5])

analyseur = Analyseur("Tout",[aGram,aPonct])
analyseur.numeroter()

taille_morceaux = 1000

## Cross-Validation

id_oeuvres = [ [("balzac",k) for k in range(1,4)], [("stendhal",k) for k in range(1,3)], [("flaubert",k) for k in [1,3,4]] ]
categories = ["balzac","stendhal", "flaubert"]

def createur_classifieur():
    return SVM()

#C = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, createur_classifieur, pourcentage_eval = 0.5, nombre_essais = 10, leave_one_out = False, full_text=False)
#C.resoudre()

log_tailles = list(np.arange(3.5,3.6,0.2))
precisions = []

def test_taille():
    global precisions
    global categories
    for log_taille_morceaux in log_tailles:
        taille_morceaux = int(np.power(10,log_taille_morceaux))
        C = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, createur_classifieur, pourcentage_eval = 0.5, nombre_essais = 10, leave_one_out = True, full_text=False)
        C.resoudre()
        precisions.append(C.prec)

def plot_taille():
    plt.plot(log_tailles, precisions)
    plt.xlabel("Taille des morceaux (log)")
    plt.ylabel("Precision de la cross-validation")
    plt.savefig("influence_taille.png")

## Probleme

# classifieur = SVM()
# 
# id_training_set = [[("dumas",k) for k in range(1,3)],[("proust",k) for k in range(1,3)]]
# categories = ["D","P"]
# 
# id_eval_set = [[("dumas",k) for k in range(1,3)],[("proust",k) for k in range(3,5)]]
# categories_supposees = ["D","P"]
# 
# P = Probleme(id_training_set, categories, id_eval_set, categories_supposees, taille_morceaux, analyseur, classifieur, langue = "fr", full_text = False)
# P.creer_textes()
# P.analyser()
# P.appliquer_classifieur()
# P.interpreter()
# P.afficher()
# P.evaluer()
# P.afficher_graphique()
