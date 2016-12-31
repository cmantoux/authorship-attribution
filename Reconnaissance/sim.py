from time import time

import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from carac import *
import numpy as np
import numpy.linalg as alg
import numpy.random as rd
import matplotlib.pyplot as plt
from classes import Analyseur,Classifieur,Probleme
from Interpretation.importance_composantes import importance, gain_information
import Evaluation.evaluation_interne as ei
import Evaluation.evaluation_externe as ee
import Evaluation.evaluation_relative as er

def norm(v):
    n = len(v)
    return alg.norm(v)/np.sqrt(n) # dimension-independent 2-norm

def similarity(texte1, texte2):
    v1 = texte1.vecteur
    v2 = texte2.vecteur
    # s = -norm(v1-v2) # scaled euclidean norm
    # s = np.vdot(v1,v2)/(alg.norm(v1)*alg.norm(v2)) # cosine similarity
    gamma = 1
    s = np.exp(-gamma*norm(v1-v2)**2) # RBF kernel
    return s
    
def AS(texte, liste_textes):
    sim = [similarity(texte, texte2) for texte2 in liste_textes]
    return np.mean(sim)

def AGS(liste_textes):
    group_sim = [AS(texte,liste_textes) for texte in liste_textes]
    return np.mean(group_sim)
    
def ADS(liste_textes1, liste_textes2):
    sim1 = [AS(texte1,liste_textes2) for texte1 in liste_textes1]
    sim2 = [AS(texte2, liste_textes1) for texte2 in liste_textes2]
    sim1.extend(sim2)
    return np.mean(sim1)

class AVS(Classifieur):
    
    def __init__(self,a=0.77):
        print("Création du classifieur AVS")
        self.a = a
        
    def classifier(self, training_set, eval_set):
        self.training_set = training_set
        self.eval_set = eval_set
        
        m = len(training_set)
        n = len(eval_set)
        
        self.M1 = np.zeros((m,m))
        self.M2 = np.zeros((n,n))
        self.M3 = np.zeros((m,n))
        
        for i in range(m):
            for j in range(m):
                self.M1[i,j] = similarity(training_set[i],training_set[j])
        for i in range(n):
            for j in range(n):
                self.M2[i,j] = similarity(eval_set[i],eval_set[j])
        for i in range(m):
            for j in range(n):
                self.M3[i,j] = similarity(training_set[i],eval_set[j])
        
        AGS1 = np.mean(self.M1)
        AGS2 = np.mean(self.M2)
        ADS1 = np.mean(self.M3)
        self.b = 0.5*((ADS1/AGS1)+(ADS1/AGS2))
        print(AGS1,AGS2)
        print(ADS1)
        
        if (ADS1>self.a*AGS1 and ADS1>self.a*AGS2):
            print("AUTEURS IDENTIQUES")
            self.same = True
        else:
            print("AUTEURS DIFFERENTS")
            self.same = False

        
def main_test():
    plt.close()
    taille_morceaux = 1000
    analyseur = Analyseur([plus_courants])
    normalisation = True
    equilibrage = True
    B1=[]
    B2=[]
    nb_exp1 = 0
    nb_exp2 = 0
    nb_exp1_suc = 0
    nb_exp2_suc = 0
    
    # auteurs différents
    
    auteurs = ["dumas","hugo", "proust", "zola", "maupassant"]
    for i in range(len(auteurs)):
        for j in range(i+1,len(auteurs)):
            for k in range(1,5):
                oeuvres_training_set = [(auteurs[i],k)]
                oeuvres_eval_set = [(auteurs[j],k)]
                classifieur = AVS()
                P = Probleme(oeuvres_training_set, oeuvres_eval_set, taille_morceaux, analyseur, classifieur, langue = "fr")
                P.creer_textes(equilibrage)
                P.analyser(normalisation)
                P.appliquer_classifieur()
                nb_exp1 += 1
                B1.append(classifieur.b)
                if classifieur.same == False:
                    nb_exp1_suc += 1
    
    # même auteur
    
    auteurs = ["dumas","hugo", "proust", "zola", "maupassant"]
    for i in range(len(auteurs)):
        for k in range(1,8):
            oeuvres_training_set = [(auteurs[i],k)]
            oeuvres_eval_set = [(auteurs[i],k+1)]
            classifieur = AVS()
            P = Probleme(oeuvres_training_set, oeuvres_eval_set, taille_morceaux, analyseur, classifieur, langue = "fr")
            P.creer_textes(equilibrage)
            P.analyser(normalisation)
            P.appliquer_classifieur()
            nb_exp2 += 1
            B2.append(classifieur.b)
            if classifieur.same == True:
                nb_exp2_suc += 1
    
    print()
    print("Succès pour des auteurs différents : {}".format(nb_exp1_suc/nb_exp1))
    print("a moyen : {}".format(np.mean(B1)))
    print("Ecart-type : {}".format(np.sqrt(np.var(B1))))
    print()
    print("Succès pour des auteurs identiques : {}".format(nb_exp2_suc/nb_exp2))
    print("a moyen : {}".format(np.mean(B2)))
    print("Ecart-type : {}".format(np.sqrt(np.var(B2))))