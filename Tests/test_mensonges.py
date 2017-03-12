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

def tester_analyseur(nombres,precisions,liste_fonctions_entiere,fonctions_testees):
    liste_fonctions = [liste_fonctions_entiere[i-1] for i in nombres]
    K=5
    prec = 0
    for k in range(K):
        d = time()
        B = list(range(1,61))
        A = random.sample(B,50)
        for a in A:
            B.remove(a)
        id_training_set =[[("verite",k) for k in A], [("mensonge",k) for k in A]]
        categories = ["verite"] + ["mensonge"]
        id_eval_set = [[("verite",k) for k in B] ,[("mensonge",k) for k in B]]
        categories_supposees = ["verite"] + ["mensonge"]
        taille_morceaux = 5000
        analyseur = Analyseur(liste_fonctions)
        classifieur = SVM()
        P = Probleme(id_training_set, categories, id_eval_set, categories_supposees, taille_morceaux, analyseur, classifieur, langue = "fr", full_text = True)
        P.creer_textes()
        P.analyser()
        P.appliquer_classifieur()
        #P.interpreter()
        #P.afficher()
        #P.evaluer()
        #P.afficher_graphique()
        prec += ee.precision(P.eval_set, P.classifieur.p, P.classifieur.p_ref)/K
        f = time()
        print("Temps d'exécution : " + str(f-d) + "s")
        print("")
    precisions.append(prec)
    fonctions_testees.append(nombres)

precisions = []
fonctions_testees = []

combinaisons_possibles = [[k] for k in range(1,7)] + [[1,2], [3,4], [5,6], [7,8], [1,2,3,4], [1,2,5,6], [1,2,7,8], [3,4,5,6], [3,4,7,8], [5,6,7,8], [1,2,3,4,5,6], [1,2,3,4,7,8], [1,2,5,6,7,8], [3,4,5,6,7,8]]

ajouts = []

def supprimer_doublons(l):
    l2 = []
    for a in l:
        if not a in l2:
            l2.append(a)
    return l2

for nombres in combinaisons_possibles:
    nombres_ameliores = supprimer_doublons(nombres+ajouts)
    tester_analyseur(nombres_ameliores,precisions,liste_fonctions_entiere,fonctions_testees)

for i in range(len(precisions)):
    print(str(fonctions_testees[i]) + " : precision " + str(precisions[i]))