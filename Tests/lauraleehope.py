import sys

from Verification.unmasking import Unmasking
from Verification.similarite import Similarity
from carac_gramm import *
from carac_lettres import *
from carac_ponct import *
from carac_complexite import *
from carac_stopwords import *
from classes import *
from Apprentissage.svm import SVM
from Apprentissage.reseau_textes import reseau_neurones
from Clustering.kmeans import Kmeans
from Clustering.kmedoids import KMedoids
sys.path.append("/Users/maximegodin/Documents/Documents/Ecole polytechnique/2A/PSC/psc")


oeuvres_training_set = [("lgaris",k) for k in range(1,4)] + [("hgaris",k) for k in range(1,4)]
oeuvres_eval_set = [("lgaris",k) for k in range(11,13)] + [("hgaris",k) for k in range(11,24)]
taille_morceaux = 5000


a1 = Longueur_Phrases()
a2 = Complexite_Grammaticale(langue = "en", saut= 1)
a3 = Freq_Stopwords(langue = "en")

analyseur = Analyseur([a1,a2,a3])


id_training_set, categories, id_eval_set, categories_supposees, taille_morceaux, analyseur, classifieur, langue = "fr"

classifieur = SVM()
P = Probleme(oeuvres_training_set,["lgaris","hgaris"] oeuvres_eval_set, taille_morceaux, analyseur, classifieur, langue = "en")
P.creer_textes(equilibrage = False,equilibrage_eval=False)
P.analyser(normalisation = False)
P.appliquer_classifieur()
P.afficher()
P.evaluer()
P.interpreter(utiliser_textes_training=True)
P.afficher_graphique(poids_composantes=importance)

# taille_morceaux = 1000
# analyseur = Analyseur([freq_ponct, freq_gram,freq_stopwords])
#
# verificateur = Similarity()
#
# liste_id_oeuvres_base = [("hgaris",k) for k in range(1,4)]
#
# liste_id_oeuvres_calibrage = [("lgaris",k) for k in range(1,4)] + [("adams",k) for k in range(1,4)] + [("stratemeyer",k) for k in range(1,4)]
#
# liste_id_oeuvres_disputees = [("hgaris",k) for k in range(41,53)]
#
# V = Verification(liste_id_oeuvres_base, liste_id_oeuvres_calibrage, liste_id_oeuvres_disputees, taille_morceaux, analyseur, verificateur, langue = "en")
# V.resoudre()