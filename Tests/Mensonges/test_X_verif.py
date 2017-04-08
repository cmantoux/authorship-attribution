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
from Apprentissage.reseau_textes import reseau_neurones
from Apprentissage.Bayes import Bayes
from Interpretation.importance_composantes import importance, gain_information
from Verification.similarite import Similarity
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
liste_fonctions = [a1,a3,a5]

#verificateur = Unmasking()
verificateur = Similarity()

taille_morceaux = 1000
analyseur = Analyseur(liste_fonctions)

id_oeuvres_base =[[("veriteXshake_morceau",1)]]
categories_base = ["X"]

id_oeuvres_calibrage = [[("veriteYshake_morceau",1)]]
categories_calibrage = ["Y"]

id_oeuvres_disputees = [[("veriteXshake_morceau",2)], [("veriteYshake_morceau",2)]]
categories_disputees = ["X"] + ["Y"]

V = Verification(id_oeuvres_base, categories_base, id_oeuvres_calibrage, categories_calibrage, id_oeuvres_disputees, categories_disputees, taille_morceaux, analyseur, verificateur)
V.resoudre()