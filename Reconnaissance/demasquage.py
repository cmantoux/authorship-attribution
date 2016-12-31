from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from carac import *
import numpy as np
import numpy.linalg as alg
import random as rd
import matplotlib.pyplot as plt
from Apprentissage.svm import SVM
from classes import Analyseur, Verification
from Utilitaires.equilibrage_et_normalisation import normaliser1, equilibrer1

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
        print("Creation du demasqueur par similarité")
    
    def qualite(self, verif, vraie_verif):
        n = len(verif)
        nb_meme_auteur = 0
        nb_auteur_different = 0
        mauvaises_attributions = 0
        mauvais_rejets = 0
        q = 0
        for i in range(n):
            if verif[i] == vraie_verif[i]:
                q += 1
            if vraie_verif[i]:
                nb_meme_auteur += 1
                if not verif[i]:
                    mauvais_rejets += 1
            if not vraie_verif[i]:
                nb_auteur_different += 1
                if verif[i]:
                    mauvaises_attributions += 1
        fp = mauvaises_attributions/nb_auteur_different
        fn = mauvais_rejets/nb_meme_auteur
        qualite = (2-(np.sqrt(fn)+np.sqrt(fp)))
        return qualite, q, n, mauvaises_attributions, nb_auteur_different, mauvais_rejets, nb_meme_auteur 
    
    def calibrer(self, textes_base, textes_calibrage):
        self.textes_base = textes_base
        self.textes_calibrage = rd.sample(textes_calibrage, len(textes_base))
        self.textes = self.textes_base + self.textes_calibrage

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
        
        print("Largeur de la base : {:3f} +- {:3f}".format(self.AGS_base, self.marge_base))
        print("Largeur du corpus de calibrage : {:3f} +- {:3f}".format(self.ADGS_calibrage, self.marge_calibrage))
        
        vraie_verif_calibrage = []
        auteur_base = self.textes_base[0].auteur
        for t in self.textes:
            auteur_theorique = t.auteur
            if auteur_theorique == auteur_base:
                vraie_verif_calibrage.append(True)
            else:
                vraie_verif_calibrage.append(False)
        Q = []
        A = np.linspace(-1,2,31)
        for a in A:
            verif_calibrage = []
            for t in self.textes:
                s = AS(t, self.textes_base)
                if s > self.AGS_base - a*self.marge_base:
                    verif_calibrage.append(True)
                else :
                    verif_calibrage.append(False)
            q = self.qualite(verif_calibrage, vraie_verif_calibrage)[0]
            Q.append(q)
        a_max = A[Q.index(max(Q))]
        print("Qualite optimale : {}".format(max(Q)))
        print("Valeur de a : {}".format(a_max))
        self.a = a_max
    
    def demasquer(self, textes_base, textes_disputes):
        self.textes_disputes = textes_disputes
        self.verif = []
        self.vraie_verif = []
        auteur_base = self.textes_base[0].auteur
        for t in textes_disputes:
            s = AS(t, self.textes_base)
            if s > self.AGS_base - self.a*self.marge_base:
                # il est suffisamment proche de la base
                self.verif.append(True)
            else :
                self.verif.append(False)
            auteur_theorique = t.auteur
            if auteur_theorique == auteur_base:
                self.vraie_verif.append(True)
            else:
                self.vraie_verif.append(False)
        
    def evaluer(self):
        qualite, q, n, mauvaises_attributions, nb_auteur_different, mauvais_rejets, nb_meme_auteur  = self.qualite(self.verif, self.vraie_verif)
        print("Mauvaises attributions : {} sur {}".format(mauvaises_attributions, nb_auteur_different))
        print("Mauvais rejets : {} sur {}".format(mauvais_rejets, nb_meme_auteur))
        print("Nombre de vérifications correctes : {} sur {}".format(q,n))
        print("Pourcentage d'efficacité : {} %".format(int(100*q/n)))
    
    def afficher(self):
        print("")
        self.evaluer()
        aut_base = self.textes_base[0].auteur
        aut = self.textes_disputes[0].auteur
        num = self.textes_disputes[0].numero
        nb_vrai = 0
        nb_faux = 0
        i = 0
        while i < len(self.textes_disputes)-1:
            if self.textes_disputes[i+1].auteur == aut and self.textes_disputes[i+1].numero == num:
                if self.verif[i]:
                    nb_vrai += 1
                else :
                    nb_faux += 1
            else:
                if nb_vrai>nb_faux:
                    print("L'oeuvre " + aut + str(num) + " a été écrite par " + aut_base + " : " + str(nb_vrai) + " textes contre " + str(nb_faux))
                else:
                    print("L'oeuvre " + aut + str(num) + " n'a pas été écrite par " + aut_base + " : " + str(nb_faux) + " textes contre " + str(nb_vrai))
                nb_vrai = 0
                nb_faux = 0
                aut = self.textes_disputes[i+1].auteur
                num = self.textes_disputes[i+1].numero
            i+=1
        if nb_vrai>nb_faux:
            print("L'oeuvre " + aut + str(num) + " a été écrite par " + aut_base + " : " + str(nb_vrai) + " textes contre " + str(nb_faux))
        else:
            print("L'oeuvre " + aut + str(num) + " n'a pas été écrite par " + aut_base + " : " + str(nb_faux) + " textes contre " + str(nb_vrai))


########################

taille_morceaux = 2000
analyseur = Analyseur([freq_gram, freq_ponct, plus_courants, freq_lettres])
demasqueur = Similarity()

liste_id_oeuvres_base = [("zola",k) for k in range(1,3)]

liste_id_oeuvres_calibrage = [("balzac",k) for k in range(1,3)] + [("maupassant",k) for k in range(1,3)] + [("flaubert",k) for k in range(1,3)] + [("proust",k) for k in range(1,4)]

liste_id_oeuvres_disputees = [("zola",11), ("zola", 13),("balzac",7), ("proust", 9)]

V = Verification(liste_id_oeuvres_base, liste_id_oeuvres_calibrage, liste_id_oeuvres_disputees, taille_morceaux, analyseur, demasqueur)
V.resoudre()