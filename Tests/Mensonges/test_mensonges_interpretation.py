from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/psc")
from carac_gramm import *
from carac_lettres import *
from carac_ponct import *
from carac_complexite import *
from carac_stopwords import *
from classes import Analyseur, Probleme
from Apprentissage.svm import SVM
from Apprentissage.reseau_textes import reseau_neurones
from Apprentissage.Bayes import Bayes
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

a4 = Markov_Lettres(langue = "fr")
a5 = Freq_Ponct(langue = "fr")
a6 = Freq_Stopwords(langue = "fr")
a7 = Complexite_Grammaticale(langue = "fr", saut=1)
a8 = Complexite_Vocabulaire()
a9 = Longueur_Phrases()

liste_fonctions_entiere = [a1,a2,a3,a4,a5,a6,a7,a8]
liste_fonctions = [a2]

id_training_set = [[("veriteXshake_morceau",1)], [("mensongeXshake_morceau",1)]]
categories = ["verite"] + ["mensonge"]
id_eval_set = [[("veriteXshake_morceau",2)], [("mensongeXshake_morceau",2)]]
categories_supposees = ["verite"] + ["mensonge"]

taille_morceaux = 800
analyseur = Analyseur(liste_fonctions)
classifieur = SVM()

P = Probleme(id_training_set, categories, id_eval_set, categories_supposees, taille_morceaux, analyseur, classifieur, langue = "fr", full_text = False)
P.creer_textes()
P.analyser()
P.appliquer_classifieur()
P.interpreter()
#P.afficher()
#P.evaluer()
#P.afficher_graphique()
