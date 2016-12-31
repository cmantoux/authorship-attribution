from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from carac import *
import numpy as np
from numpy.linalg import norm
import numpy.random as rd
import matplotlib.pyplot as plt
from classes import Analyseur,Classifieur,Probleme
from Interpretation.importance_composantes import importance, gain_information
from Apprentissage.svm import SVM
from Clustering.kmeans import Kmeans


class Unmasking2(Classifieur):

    def __init__(self):
        print("Création du classifieur Unmasking2")
        self.nb_essais = 50
        self.taille_echantillon = 40
        self.pas = 4

    def classifier(self, training_set, eval_set):
        self.training_set = training_set
        self.eval_set = eval_set

        # Calcul de l'importance et réordonnement des composantes
        
        vecteurs_training = np.array([t.vecteur for t in training_set])
        moyennes_training = vecteurs_training.mean(axis=0)
        variances_training = vecteurs_training.var(axis=0)
        vecteurs_eval = np.array([t.vecteur for t in eval_set])
        moyennes_eval = vecteurs_eval.mean(axis=0)
        variances_eval = vecteurs_eval.var(axis=0)
        nb_composantes = len(vecteurs_training[0])
        variances = (variances_eval + variances_training)/2
        importances = np.abs(moyennes_eval-moyennes_training)/np.sqrt(variances)
        #importances = gain_information([training_set, eval_set])
        #for i in range(nb_composantes):
        #    if not np.isfinite(importances[i]):
        #        importances[i] = 0
        ordre = sorted(list(range(nb_composantes)), key = lambda i : importances[i])
        importances.sort()
        for t in training_set:
            t.auteur = t.auteur + "1" 
            v = t.vecteur.copy()
            for i in range(nb_composantes):
                t.vecteur[ordre[i]] = v[i]
        for t in eval_set: 
            t.auteur = t.auteur + "2"
            v = t.vecteur.copy()
            for i in range(nb_composantes):
                t.vecteur[ordre[i]] = v[i]

        textes = training_set
        textes.extend(eval_set)
        rd.shuffle(textes)
        self.J = list(range(0,nb_composantes,self.pas))
        self.precision = []
        for j in self.J:
            print("Nombre de composantes retirées : {}".format(j))
            precision_moyenne = 0
            k = nb_composantes-j
            for t in textes:
                t.vecteur = t.vecteur[:k]
            for e in range(self.nb_essais):
                print("Essai n°{}".format(e))
                classifieur = SVM(pc = False)
                indices = rd.choice(len(textes),self.taille_echantillon)
                non_indices = [i for i in range(len(textes)) if not (i in indices)]
                eval_set_bis = [textes[i] for i in indices]
                training_set_bis = [textes[i] for i in non_indices]

                classifieur.classifier(training_set_bis, eval_set_bis)
                precision_moyenne += classifieur.precision
            precision_moyenne /= self.nb_essais
            self.precision.append(precision_moyenne)

        return

    def afficher(self):
        print("Voilà c'est bon quoi")
        print("")

d = time()

plt.close()

l = 8
oeuvres_training_set =[("dumas",k) for k in range(1,1+l)]
oeuvres_eval_set1 = [("dumas",k) for k in range(1+l,1+2*l)]
oeuvres_eval_set2 = [("zola",k) for k in range(1,1+l)]


taille_morceaux = 500
analyseur = Analyseur([freq_gram, freq_ponct, plus_courants, freq_lettres])
nb_oeuvres = 1

PM1 = []
PM2 = []
K = 8

for k in range(K):

    print("Paire de courbes n°{}".format(k))
    
    a = rd.choice(len(oeuvres_training_set),nb_oeuvres) 
    ot = [oeuvres_training_set[i] for i in a]
    oe1 = [oeuvres_eval_set1[i] for i in a]
    oe2 = [oeuvres_eval_set2[i] for i in a]
    
    classifieur_id = Unmasking2()
    P_id = Probleme(ot, oe1, taille_morceaux, analyseur, classifieur_id, "fr")
    P_id.creer_textes(equilibrage = True)
    P_id.analyser(normalisation = True)
    P_id.appliquer_classifieur()
    J = P_id.classifieur.J
    precision1 = P_id.classifieur.precision
    a = precision1[0]
    precision1 = [p/a for p in precision1]
    plt.plot(J,precision1, linestyle = "--", color = "b")
    
    classifieur_dif = Unmasking2()
    P_dif = Probleme(ot, oe2, taille_morceaux, analyseur, classifieur_id, "fr")
    P_dif.creer_textes(equilibrage = True)
    P_dif.analyser(normalisation = True)
    P_dif.appliquer_classifieur()
    J = P_dif.classifieur.J
    precision2 = P_dif.classifieur.precision
    a = precision2[0]
    precision2 = [p/a for p in precision2]
    plt.plot(J,precision2, linestyle = "--", color = "r")
    
    if k==0:
        PM1 = np.zeros((len(precision1)))
        PM2 = np.zeros((len(precision2)))
    PM1 += precision1
    PM2 += precision2

PM1 /= K
PM2 /= K

def pente(P,J):
    p = 0
    for i in range(len(P)-1):
        p += (P[i+1]-P[i])/(J[i+1]-J[i])
    x = p/(len(P)-1)
    return int(10000*p)/10000

plt.close()
plt.plot(J,PM1, linewidth = 2, color = "b", label = "auteurs identiques")
plt.plot(J, PM2, linewidth = 2, color = "r", label = "auteurs differents")

plt.xlabel("Nombre de composantes stylistiques retirées")
plt.ylabel("Precision relative du classifieur")
plt.legend(loc="best")
plt.title("Unmasking : Dumas VS Zola")
plt.savefig("unmasking_graph"+ str(int(time())) + ".png")

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")
