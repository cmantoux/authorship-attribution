from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from carac import *
from classes import Analyseur, Verification
from Verification.similarite import Similarity
from Verification.unmasking import Unmasking

taille_morceaux = 1000
analyseur = Analyseur([freq_ponct, freq_gram, plus_courants])

# verificateur = Unmasking()
verificateur = Similarity()

liste_id_oeuvres_base = [("dumas",k) for k in range(1,11)]

liste_id_oeuvres_calibrage = [("zola",k) for k in range(1,7)]

liste_id_oeuvres_disputees = [("dumas",12), ("zola", 7), ("balzac", 1)]

V = Verification(liste_id_oeuvres_base, liste_id_oeuvres_calibrage, liste_id_oeuvres_disputees, taille_morceaux, analyseur, verificateur)
V.resoudre()