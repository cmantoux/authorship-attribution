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

analyseur = Markov_Gram(langue="fr", saut=1, emondage = True)
analyseur.numeroter()

taille_morceaux = 5000


## Probleme

def test_probleme():
    id_training_set = [[("dumas", k) for k in range(1, 3)], [("proust", k) for k in range(1, 3)]]
    categories = ["dumas", "proust"]
    id_eval_set = [[("dumas", k) for k in range(3, 5)], [("proust", k) for k in range(3, 5)]]
    categories_supposees = ["dumas", "proust"]
    classifieur = SVM()
    P = Probleme(id_training_set, categories, id_eval_set, categories_supposees, taille_morceaux, analyseur,
                 classifieur, langue="fr", full_text=False)
    P.creer_textes()
    P.analyser()
    P.appliquer_classifieur()
    P.interpreter()
    P.afficher()
    # P.evaluer()
    P.afficher_graphique()

test_probleme()
