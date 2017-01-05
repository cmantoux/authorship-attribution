from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from carac import *
from classes import Analyseur, Verification
from Verification.similarite import Similarity
from Verification.unmasking import Unmasking

taille_morceaux = 1000
analyseur = Analyseur([freq_ponct, freq_gram, plus_courants, freq_lettres])

verificateur = Unmasking()
# verificateur = Similarity()

liste_id_oeuvres_base = [("dumas",k) for k in range(1,15)]

liste_id_oeuvres_calibrage = [("zola",k) for k in range(1,6)]

liste_id_oeuvres_disputees = [("dumas",k) for k in range(15,18)]

V = Verification(liste_id_oeuvres_base, liste_id_oeuvres_calibrage, liste_id_oeuvres_disputees, taille_morceaux, analyseur, verificateur)
V.resoudre()