from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from carac import *
from classes import Analyseur, Verification
from Verification.similarite import Similarity
from Verification.unmasking import Unmasking

verificateur = Unmasking()

taille_morceaux = 1000
analyseur = Analyseur([freq_gram, freq_stopwords])

liste_id_oeuvres_base = [("corneille",k) for k in range(1,16)]

liste_id_oeuvres_calibrage = [("racine",k) for k in range(1,11)]

liste_id_oeuvres_disputees = [("moliere",k) for k in [1,11]]

V = Verification(liste_id_oeuvres_base, liste_id_oeuvres_calibrage, liste_id_oeuvres_disputees, taille_morceaux, analyseur, verificateur)
V.creer_textes()
V.analyser(normalisation = False)
V.appliquer_verificateur()