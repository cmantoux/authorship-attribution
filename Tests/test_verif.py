from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/psc")
from carac_gramm import *
from carac_lettres import *
from carac_ponct import *
from carac_complexite import *
from carac_stopwords import *
from classes import Analyseur, Verification
from Verification.similarite import Similarity
from Verification.unmasking import Unmasking
from Apprentissage.svm import SVM
from Interpretation.importance_composantes import importance, gain_information

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

#liste_fonctions = [a1,a2,a3,a4,a5,a6,a7,a8,a9]
liste_fonctions = [a1,a6,a8]
analyseur = Analyseur(liste_fonctions)

verificateur = Unmasking()
#verificateur = Similarity()

id_oeuvres_base =[[("dumas",k) for k in range(1,3)], [("balzac",k) for k in range(1,3)]]
categories_base = ["dumas"] + ["balzac"]

id_oeuvres_calibrage = [[("dumas",k) for k in range(3,5)] ,[("balzac",k) for k in range(3,5)]]
categories_calibrage = ["dumas"] + ["balzac"]

id_oeuvres_disputees = [[("dumas",k) for k in range(5,7)] ,[("balzac",k) for k in range(5,7)]]
categories_disputees = ["dumas"] + ["balzac"]

V = Verification(id_oeuvres_base, categories_base, id_oeuvres_calibrage, categories_calibrage, id_oeuvres_disputees, categories_disputees, taille_morceaux, analyseur, verificateur)
V.resoudre()