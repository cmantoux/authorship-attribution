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
from Apprentissage.Bayes import Bayes
from Apprentissage.reseau_textes import reseau_neurones
from Interpretation.importance_composantes import importance, gain_information
from Evaluation import evaluation_externe as ee
import random
import matplotlib.pyplot as plt

def createur_classifieur():
    return SVM()

a1 = Freq_Gram(langue = "fr") # tres bien

a2 = Markov_Gram(langue = "fr",saut=1) # tres bien
a21 = Markov_Gram(langue = "fr",saut=1)
a22 = Markov_Gram(langue = "fr",saut=2)
a23 = Markov_Gram(langue = "fr",saut=3)
a24 = Markov_Gram(langue = "fr",saut=4)

a3 = Freq_Ngrammes(langue = "fr",n=1) # tres bien
a31 = Freq_Ngrammes(langue = "fr",n=1)
a32 = Freq_Ngrammes(langue = "fr",n=2)
a33 = Freq_Ngrammes(langue = "fr",n=3)
a34 = Freq_Ngrammes(langue = "fr",n=4)

a4 = Markov_Lettres(langue = "fr") # bof
a5 = Freq_Ponct(langue = "fr") # bof
a6 = Freq_Stopwords(langue = "fr") # bien

a7 = Complexite_Grammaticale(langue = "fr", saut=1) # mieux avec petits morceaux
a71 = Complexite_Grammaticale(langue = "fr", saut=1)
a72 = Complexite_Grammaticale(langue = "fr", saut=2)
a73 = Complexite_Grammaticale(langue = "fr", saut=3)
a74 = Complexite_Grammaticale(langue = "fr", saut=4)

a8 = Complexite_Vocabulaire() # bien
a9 = Longueur_Phrases() # bcp mieux avec petits morceaux

liste_fonctions_entiere = [a1,a2,a3,a4,a5,a6,a7,a8]
liste_fonctions = [a1]

id_oeuvres = [ [("veriteXshake",0)], [("mensongeXshake",0)] ]
id_oeuvres2 = [ [("veriteX",k) for k in range(1,63)], [("mensongeX",k) for k in range(1,49)] ]
categories = ["vérité"] + ["mensonge"]

def test_tailles():
    
    plt.close()

    liste_tailles = list(range(300,1400,500))
    fonctions_possibles = [[a2], [a6], [a7], [a9]]
    noms = ["Markov_Gram", "Freq_Stopwords", "Complexite_Grammaticale", "Longueur_Phrases"]
    precisions = [ [], [], [], [], [] ]
    
    for taille_morceaux in liste_tailles:
        for i in range(len(fonctions_possibles)):
            analyseur = Analyseur(fonctions_possibles[i])
            C = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, createur_classifieur, pourcentage_eval = 0.5, nombre_essais = 10, leave_one_out = True, full_text=False)
            C.resoudre()
            precisions[i].append(C.prec)
    
    
    for i in range(len(fonctions_possibles)):
        plt.plot(liste_tailles, precisions[i], label=noms[i], marker="o")
    plt.legend(loc="best")
    plt.xlabel("Taille des morceaux (nb mots)")
    plt.ylabel("Précision de l'attribution")
    plt.title("Détection de mensonges avec différents analyseurs")
    plt.savefig("test_tailles_mensonges.png")