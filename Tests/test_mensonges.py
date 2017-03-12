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
from Interpretation.importance_composantes import importance, gain_information


d = time()

id_training_set =[[("verite",k) for k in range(1,31)], [("mensonge",k) for k in range(1,31)]]
categories = ["verite"] + ["mensonge"]
id_eval_set = [[("verite",k) for k in range(31,61)] ,[("mensonge",k) for k in range(31,61)]]
categories_supposees = ["verite"] + ["mensonge"]

taille_morceaux = 5000

a1 = Freq_Gram(langue = "fr")
a2 = Markov_Gram(langue = "fr",saut=1)

a21 = Markov_Gram(langue = "fr",saut=1)
a22 = Markov_Gram(langue = "fr",saut=2)
a23 = Markov_Gram(langue = "fr",saut=3)
a24 = Markov_Gram(langue = "fr",saut=4)

a3 = Freq_Ngrammes(langue = "fr",n=1)
a4 = Markov_Lettres(langue = "fr")
a5 = Freq_Ponct(langue = "fr")
a6 = Longueur_Phrases()
a7 = Complexite_Grammaticale(langue = "fr", saut=1)
a8 = Complexite_Vocabulaire()
a9 = Freq_Stopwords(langue = "fr")

#liste_fonctions = [a1,a2,a3,a4,a5,a6,a7,a8,a9]
liste_fonctions = [a6]
analyseur = Analyseur(liste_fonctions)
classifieur = SVM()

P = Probleme(id_training_set, categories, id_eval_set, categories_supposees, taille_morceaux, analyseur, classifieur, langue = "fr", full_text = True)

#P.resoudre()

# equivalent à

P.creer_textes()
P.analyser()
P.appliquer_classifieur()
P.interpreter()
P.afficher()
print("")
P.evaluer()

#P.afficher_graphique()

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")