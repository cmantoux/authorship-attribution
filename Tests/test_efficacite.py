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
from Apprentissage.Apriori import Apriori
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

## Taille

id_oeuvres = [ [("balzac",k) for k in range(1,4)], [("stendhal",k) for k in range(1,3)], [("flaubert",k) for k in [1,3,4]] ]
categories = ["balzac","stendhal", "flaubert"]
taille_morceaux = 5000

def createur_classifieur():
    return SVM()

log_tailles = list(np.arange(4,4.8,1))
precisions = []

def test_taille1():
    global precisions
    global categories
    for log_taille_morceaux in log_tailles:
        taille_morceaux = int(np.power(10,log_taille_morceaux))
        C = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, createur_classifieur, pourcentage_eval = 0.3, nombre_essais = 10, leave_one_out = False, full_text=False)
        C.resoudre()
        precisions.append(C.prec)

def plot_taille1():
    plt.plot(log_tailles, precisions, marker="o", linestyle="None")
    plt.xlabel("Log_10 de la taille des morceaux")
    plt.ylabel("Precision de la cross-validation")
    plt.title("Influence de la taille : corpus réalisme")
    plt.savefig("influence_taille1.png")

id_oeuvres2 = [ [("abronte",1)], [("cbronte",1)], [("ebronte",1)] ]
categories2 = ["Anne Brontë", "Charlotte Brontë", "Emily Brontë"]
taille_morceaux2 = 5000

log_tailles2 = list(np.arange(4,4.3,1))
precisions2 = []

def test_taille2():
    global precisions2
    global categories2
    for log_taille_morceaux in log_tailles2:
        taille_morceaux = int(np.power(10,log_taille_morceaux))
        C = CrossValidation(id_oeuvres2, categories2, taille_morceaux, analyseur, createur_classifieur, pourcentage_eval = 0.5, nombre_essais = 10, leave_one_out = False, full_text=False, langue="en")
        C.resoudre()
        precisions2.append(C.prec)

def plot_taille2():
    plt.close()
    plt.plot(log_tailles2, precisions, marker="o", linestyle="None")
    plt.xlabel("Log_10 de la taille des morceaux")
    plt.ylabel("Precision de la cross-validation")
    plt.title("Influence de la taille : corpus Brontë")
    plt.savefig("influence_taille2.png")
    
    
## Classifieurs
    
liste_classifieurs = [SVM,Bayes,Kmeans,KMedoids]
noms_classifieurs = ["SVM", "Bayes", "Kmeans", "Kmedoids"]

taille_morceaux = 10000

def test_classifieurs1(taille_morceaux):
    precisions_classifieurs = []
    for createur in liste_classifieurs:
        C = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, createur, pourcentage_eval = 0.3, nombre_essais = 1, leave_one_out = True, full_text=False)
        C.resoudre()
        precisions_classifieurs.append(C.prec)
    n_groups = len(liste_classifieurs)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = plt.bar(index, precisions_classifieurs, bar_width,
                    alpha=opacity,
                    color='r')
    plt.xlabel('Classifieurs')
    plt.ylabel('Précision de la validation')
    plt.title('Cross-validation, corpus réaliste, ' + str(taille_morceaux)+" mots")
    plt.xticks(index + bar_width / 2, noms_classifieurs)
    #plt.legend(loc="lower right")
    #plt.tight_layout()
    plt.ylim(ymin = 0, ymax = 1)
    plt.savefig("classifieurs1_"+str(taille_morceaux)+"LOO.png")

def test_classifieurs2(taille_morceaux):
    precisions_classifieurs2 = []
    for createur in liste_classifieurs:
        C = CrossValidation(id_oeuvres2, categories2, taille_morceaux, analyseur, createur, pourcentage_eval = 0.3, nombre_essais = 1, leave_one_out = True, full_text=False, langue="en")
        C.resoudre()
        precisions_classifieurs2.append(C.prec)
    n_groups = len(liste_classifieurs)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = plt.bar(index, precisions_classifieurs2, bar_width,
                    alpha=opacity,
                    color='b')
    plt.xlabel('Classifieurs')
    plt.ylabel('Précision de la validation')
    plt.title('Cross-validation, corpus Brontë, ' + str(taille_morceaux)+" mots")
    plt.xticks(index + bar_width / 2, noms_classifieurs)
    #plt.legend(loc="lower right")
    #plt.tight_layout()
    plt.ylim(ymin = 0, ymax=1)
    plt.savefig("classifieurs2_"+str(taille_morceaux)+"LOO.png")
    


## Equilibrage et pourcentage

def test_equilibrage1():
    Ceq1 = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, reseau_neurones, pourcentage_eval = 0.3, nombre_essais = 1, leave_one_out = False, full_text=False)
    Ceq1.creer_textes(equilibrage = True)
    Ceq1.analyser()
    Ceq1.valider()
    reseau_eq = Ceq1.prec
    
    Cneq1 = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, reseau_neurones, pourcentage_eval = 0.3, nombre_essais = 1, leave_one_out = False, full_text=False)
    Cneq1.creer_textes(equilibrage = False)
    Cneq1.analyser()
    Cneq1.valider()
    reseau_neq = Cneq1.prec
    
    Ceq2 = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, Kmeans, pourcentage_eval = 0.3, nombre_essais = 1, leave_one_out = False, full_text=False)
    Ceq2.creer_textes(equilibrage = True)
    Ceq2.analyser()
    Ceq2.valider()
    km_eq = Ceq2.prec
    
    Cneq2 = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, Kmeans, pourcentage_eval = 0.3, nombre_essais = 1, leave_one_out = False, full_text=False)
    Cneq2.creer_textes(equilibrage = False)
    Cneq2.analyser()
    Cneq2.valider()
    km_neq = Cneq2.prec
    
    print(reseau_eq, reseau_neq, km_eq, km_neq)


def test_pourcentage1(taille_morceaux):
    plt.close()
    liste_pourcentages = [0.05, 0.1, 0.15, 0.2, 0.3]
    liste_classifieurs = [SVM,Bayes,Kmeans,KMedoids]
    noms_classifieurs = ["SVM", "Bayes", "Kmeans", "Kmedoids"]
    precisions = [[] for createur in liste_classifieurs]
    for p in liste_pourcentages:
        for k in range(len(liste_classifieurs)):
            createur = liste_classifieurs[k]
            C = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, createur, pourcentage_eval = p, nombre_essais = 1, leave_one_out = False, full_text=False)
            C.resoudre()
            precisions[k].append(C.prec)
    for k in range(len(liste_classifieurs)):   
        plt.plot(liste_pourcentages, precisions[k], label=noms_classifieurs[k], marker="o")
    plt.legend(loc="best")
    plt.xlabel("Pourcentage de textes dans eval_set")
    plt.ylabel("Precision de la validation")
    plt.title("Influence de la répartition entre apprentissage et test")
    plt.savefig("pourcentage_eval1.png")