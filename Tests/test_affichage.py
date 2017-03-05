from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/psc")
from carac_gramm import *
from carac_lettres import *
from carac_ponct import *
from carac_complexite import *
from carac_stopwords import *
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
classifieur = SVM()

P = Probleme(id_training_set, categories, id_eval_set, categories_supposees, taille_morceaux, analyseur, classifieur, langue = "fr")

P.resoudre()

# equivalent à

#P.creer_textes()
#P.analyser()
#P.appliquer_classifieur()
#P.interpreter()
#P.afficher()
#P.afficher_graphique()

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")