from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/psc")
from carac_gramm import *
from carac_lettres import *
from carac_ponct import *
from carac_complexite import *
from carac_stopwords import *
from classes import *
from Apprentissage.svm import SVM
from Interpretation.importance_composantes import importance, gain_information
from Evaluation import evaluation_externe as ee
import random

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
a8 = Complexite_Vocabulaire()
a9 = Longueur_Phrases()

liste_fonctions_entiere = [a1,a2,a3,a4,a5,a6,a7,a8]
liste_fonctions = [a2]

id_oeuvres =[ [("veriteX",0), ("mensongeX",0)], [("veriteY",0),("mensongeY",0)] ]
categories = ["X"] + ["Y"]

taille_morceaux = 700
analyseur = Analyseur(liste_fonctions)

def createur_classifieur():
    return SVM()

C = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, createur_classifieur, pourcentage_eval = 0.1, nombre_essais = 20, leave_one_out = True)
C.resoudre()
