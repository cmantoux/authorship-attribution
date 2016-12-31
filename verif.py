from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from carac import *
from classes import Analyseur, Verification
from Reconnaissance.demasquage import Similarity

taille_morceaux = 1000
analyseur = Analyseur([freq_gram, freq_ponct, plus_courants, freq_lettres])
demasqueur = Similarity()

liste_id_oeuvres_base = [("zola",k) for k in range(1,5)]

liste_id_oeuvres_calibrage = [("balzac",k) for k in range(1,5)] + [("maupassant",k) for k in range(1,5)] + [("flaubert",k) for k in range(1,5)]

liste_id_oeuvres_disputees = [("zola",11), ("zola", 13),("balzac",7), ("dumas",1), ("proust", 9)]

V = Verification(liste_id_oeuvres_base, liste_id_oeuvres_calibrage, liste_id_oeuvres_disputees, taille_morceaux, analyseur, demasqueur)
V.resoudre()