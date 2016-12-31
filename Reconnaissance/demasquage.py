from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from carac import *
import numpy as np
import numpy.linalg as alg
import numpy.random as rd
import matplotlib.pyplot as plt
from Apprentissage.svm import SVM

def norm(v):
    n = len(v)
    return alg.norm(v)/np.sqrt(n) # dimension-independent 2-norm

def similarity(texte1, texte2):
    v1 = texte1.vecteur
    v2 = texte2.vecteur
    gamma = 1
    s = np.exp(-gamma*norm(v1-v2)**2) # RBF kernel
    return s
    
def AS(texte, liste_textes):
    sim = [similarity(texte, texte2) for texte2 in liste_textes]
    return np.mean(sim)

def AGS(liste_textes):
    group_sim = [AS(texte,liste_textes) for texte in liste_textes]
    return np.mean(group_sim)

class Similarity():
    
    def __init__(self):
        #print("Creation du demasqueur par similarité")
        self.a = 1
        self.AGS_base = 0
    
    def qualite(self, verif, vraie_verif):
        n = len(verif)
        q = 0
        for i in range(n):
            if verif[i] == vraie_verif[i]:
                q += 1
        return q/n
    
    def calibrer(self, textes_base, textes_calibrage):
        self.textes_base = textes_base
        self.textes_calibrage = textes_calibrage
        self.textes = textes_base + textes_calibrage

        self.M1 = np.zeros((len(textes_base), len(textes_base)))
        for i in range(len(textes_base)):
            for j in range(len(textes_base)):
                self.M1[i,j] = similarity(textes_base[i],textes_base[j])
        self.AS_base = np.mean(self.M1, axis = 0)
        self.AGS_base = np.mean(self.AS_base)
        self.marge_base = np.sqrt(np.var(self.AS_base))
        self.AS_calibrage = []
        for t in self.textes_calibrage:
            self.AS_calibrage.append(AS(t,self.textes_base))
        self.ADGS_calibrage = np.mean(self.AS_calibrage)
        self.marge_calibrage = np.sqrt(np.var(self.AS_calibrage))
        B = np.linspace(0.5, 1.5, 20)
        Q = []
        for b in B:
            verif_calibrage = []
            for s in list(self.AS_base) + list(self.AS_calibrage):
                verif_calibrage.append(s>b*self.AGS_base)
            vraie_verif_calibrage = [True]*len(textes_base) + [False]*len(textes_calibrage)
            Q.append(self.qualite(verif_calibrage, vraie_verif_calibrage))
        print("Qualite maximale : {}".format(max(Q)))
        self.a = B[Q.index(max(Q))]
        print("Valeur optimale de a : {}".format(self.a))
        
    
    def demasquer(self, textes_base, textes_disputes):
        self.textes_disputes = textes_disputes
        self.verif = []
        for t in textes_disputes:
            s = AS(t, textes_base)
            if s > self.a*self.AGS_base:
                # il est suffisamment proche de la base
                self.verif.append(True)
            else :
                self.verif.append(False)
    
    def afficher(self):
        self.vraie_verif = []
        auteur_base = self.textes_base[0].auteur
        for i in range(len(self.textes_disputes)):
            t = self.textes_disputes[i]
            auteur_theorique = t.auteur
            if auteur_theorique == auteur_base:
                self.vraie_verif.append(True)
            else:
                self.vraie_verif.append(False)
        self.succes = 0
        for i in range(len(self.verif)):
            if self.vraie_verif[i] == self.verif[i]:
                self.succes += 1
        print("Nombre de verifications correctes : {} sur {}".format(self.succes, len(self.verif)))
        print("Pourcentage : {} %".format(int(100*self.succes / len(self.verif))))



########################

taille_morceaux = 1000
analyseur = Analyseur([freq_gram, freq_ponct, plus_courants, freq_lettres])
demasqueur = Similarity()

liste_id_oeuvres_base = [("zola",k) for k in range(1,3)]

liste_id_oeuvres_calibrage = [("balzac",k) for k in range(1,3)] + [("maupassant",k) for k in range(1,3)] + [("flaubert",k) for k in range(1,3)]

liste_id_oeuvres_disputees = [("zola",11), ("zola", 13),("balzac",7), ("dumas",1), ("proust", 9)]

V = Verification(liste_id_oeuvres_base, liste_id_oeuvres_calibrage, liste_id_oeuvres_disputees, taille_morceaux, analyseur, demasqueur)
V.resoudre()