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
from Verification.similarite import Similarity
from Interpretation.importance_composantes import importance, gain_information
from Evaluation import evaluation_externe as ee
import matplotlib.pyplot as plt

a1 = Freq_Gram(langue = "fr")
a2 = Markov_Gram(langue = "fr",saut=1)
a3 = Freq_Ngrammes(langue = "fr",n=1)
a4 = Markov_Lettres(langue = "fr")
a5 = Freq_Ponct(langue = "fr")
a6 = Freq_Stopwords(langue = "fr")
a7 = Complexite_Grammaticale(langue = "fr", saut=1)
a8 = Complexite_Vocabulaire()
a9 = Longueur_Phrases()

aGram = Analyseur("Grammaire",[a1])
aLettres= Analyseur("Lettres",[a3,a4])
aPonct = Analyseur("Ponctuation",[a5])

analyseur = Analyseur("Tout",[aGram,aPonct])
analyseur.numeroter()

taille_morceaux = 5000
    
## Probleme

def test_probleme():
    id_training_set = [[("dumas",k) for k in range(1,3)],[("proust",k) for k in range(1,3)]]
    categories = ["dumas","proust"]
    id_eval_set = [[("dumas",k) for k in range(1,3)],[("proust",k) for k in range(3,5)]]
    categories_supposees = ["dumas","proust"]
    classifieur = SVM()
    P = Probleme(id_training_set, categories, id_eval_set, categories_supposees, taille_morceaux, analyseur, classifieur, langue = "fr", full_text = False)
    P.creer_textes()
    P.analyser()
    P.appliquer_classifieur()
    #P.interpreter()
    #P.afficher()
    #P.evaluer()
    P.afficher_graphique()

test_probleme()
    
## Cross-validation

def createur_classifieur():
    return SVM()

def test_cross_validation():
    id_oeuvres = [ [("balzac",k) for k in range(1,4)], [("stendhal",k) for k in range(1,3)], [("flaubert",k) for k in [1,3,4]] ]
    categories = ["balzac","stendhal", "flaubert"]
    C = CrossValidation(id_oeuvres, categories, taille_morceaux, analyseur, createur_classifieur, pourcentage_eval = 0.5, nombre_essais = 10, leave_one_out = True)
    C.resoudre()

## Verification

def test_verif():
    verificateur = Similarity()
    id_oeuvres_base =[[("zola",k) for k in range(1,11)]]
    categories_base = ["zola"]
    id_oeuvres_calibrage = [[("dumas",k) for k in range(1,11)]]
    categories_calibrage = ["dumas"]
    id_oeuvres_disputees = [[("zola",k) for k in range(11,14)] ,[("dumas",k) for k in range(11,14)]]
    categories_disputees = ["zola"] + ["dumas"]
    V = Verification(id_oeuvres_base, categories_base, id_oeuvres_calibrage, categories_calibrage, id_oeuvres_disputees, categories_disputees, taille_morceaux, analyseur, verificateur)
    V.resoudre()