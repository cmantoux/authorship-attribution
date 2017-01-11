import sys

from Verification.unmasking import Unmasking
from carac import *
from classes import Analyseur, Verification

sys.path.append("/Users/maximegodin/Documents/Documents/Ecole polytechnique/2A/PSC/psc")


# oeuvres_training_set = [("lgaris",k) for k in range(1,4)] + [("hgaris",k) for k in range(1,4)]
# oeuvres_eval_set = [("lgaris",k) for k in range(11,13)] + [("hgaris",k) for k in range(11,24)]
# taille_morceaux = 5000
# analyseur = Analyseur([freq_gram, plus_courants, freq_ponct])
# classifieur = SVM()
# P = Probleme(oeuvres_training_set, oeuvres_eval_set, taille_morceaux, analyseur, classifieur, langue = "en")
# P.creer_textes(equilibrage = True,equilibrage_eval=True)
# P.analyser(normalisation = True)
# P.appliquer_classifieur()
# P.afficher()
# P.evaluer()
# P.afficher_graphique()

taille_morceaux = 1000
analyseur = Analyseur([freq_ponct, freq_gram, plus_courants])

verificateur = Unmasking(langue = "en")

liste_id_oeuvres_base = [("hgaris",k) for k in range(1,4)]

liste_id_oeuvres_calibrage = [("lgaris",k) for k in range(1,4)] + [("adams",k) for k in range(1,4)] + [("stratemeyer",k) for k in range(1,4)]

liste_id_oeuvres_disputees = [("hgaris",k) for k in range(41,53)]

V = Verification(liste_id_oeuvres_base, liste_id_oeuvres_calibrage, liste_id_oeuvres_disputees, taille_morceaux, analyseur, verificateur, langue = "en")
V.resoudre()