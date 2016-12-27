from time import time

from carac import *
import numpy as np
from numpy.linalg import norm
import numpy.random as rd
import matplotlib.pyplot as plt
from classes import Analyseur,Classifieur,Probleme
from Interpretation.importance_composantes import importance, gain_information
import Evaluation.evaluation_interne as ei
import Evaluation.evaluation_externe as ee
import Evaluation.evaluation_relative as er


def norm(a):
    return np.mean(np.abs(a))
    
def matos_evaluation(training_set, eval_set, k):
    textes = training_set + eval_set
    for t in textes:
        t.vecteur = t.vecteur[:k]
    n = len(textes)
    p = np.zeros((n,2))
    p_ref = np.zeros((n,2))
    T = len(training_set)
    E = len(eval_set)
    for i in range(T):
        p[i][0] = 1
        p_ref[i][0] = 1
    for i in range(E):
        p[T+i][1] = 1
        p_ref[T+i][1] = 1
    return textes, p, p_ref
    
def indice_precision(training_set, eval_set, k):
    textes, p, p_ref = matos_evaluation(training_set, eval_set, k)
    return er.davies_bouldin(textes, p)

class Unmasking(Classifieur):

    def __init__(self):
        print("Création du classifieur Unmasking")

    def classifier(self, training_set, eval_set):
        self.training_set = training_set
        self.eval_set = eval_set

        vecteurs_training = np.array([t.vecteur for t in training_set])
        moyennes_training = vecteurs_training.mean(axis=0)
        variances_training = vecteurs_training.var(axis=0)

        vecteurs_eval = np.array([t.vecteur for t in eval_set])
        moyennes_eval = vecteurs_eval.mean(axis=0)
        variances_eval = vecteurs_eval.var(axis=0)

        nb_composantes = len(vecteurs_training[0])
        variances = (variances_eval + variances_training)/2
        #importances = np.abs(moyennes_eval-moyennes_training)/np.sqrt(variances)
        importances = gain_information([training_set, eval_set])
        
        for i in range(nb_composantes):
            if not np.isfinite(importances[i]):
                importances[i] = 0
        ordre = sorted(list(range(nb_composantes)), key = lambda i : importances[i])
        importances.sort()
        #print(importances)
        #print(ordre)

        for t in training_set: 
            v = t.vecteur.copy()
            for i in range(nb_composantes):
                t.vecteur[ordre[i]] = v[i]
        for t in eval_set: 
            v = t.vecteur.copy()
            for i in range(nb_composantes):
                t.vecteur[ordre[i]] = v[i]
        
        t0 = training_set[0]
        t1 = eval_set[0]
        if t0.auteur == t1.auteur:
            label = "auteurs identiques"
        else:
            label = "auteurs differents"

        J = list(range(0,nb_composantes,2))
        self.dist = []
        for j in J:
            k = nb_composantes-j
            self.dist.append(indice_precision(training_set, eval_set, k))
        a = self.dist[0]
        for l in range(len(self.dist)):
            self.dist[l]/=a
        self.J = J
        return
        

    def afficher(self):
        print("Voilà c'est bon quoi")
        print("")

d = time()

plt.close()

oeuvres_training_set =[("hugo",k) for k in range(1,8)]
oeuvres_eval_set = [("proust",1)]
oeuvres_eval_set_bis = [("hugo",8)]

taille_morceaux = 500
analyseur = Analyseur([freq_gram, freq_ponct, plus_courants, freq_lettres])
classifieur = Unmasking()

nb_essais = 3
nb_oeuvres_base = 1

for k in range(nb_essais):
    oeuvres_training_set_sample = [oeuvres_training_set[i] for i in rd.choice(len(oeuvres_training_set),nb_oeuvres_base)]
    P = Probleme(oeuvres_training_set_sample, oeuvres_eval_set, taille_morceaux, analyseur, classifieur, langue = "fr")
    P.creer_textes(equilibrage = False)
    P.analyser(normalisation = False)
    P.appliquer_classifieur()
    J = P.classifieur.J
    dist = P.classifieur.dist
    plt.plot(J,dist,label = "test" + str(k) +" diff")

for k in range(nb_essais):
    oeuvres_training_set_sample = [oeuvres_training_set[i] for i in rd.choice(len(oeuvres_training_set),nb_oeuvres_base)]
    P = Probleme(oeuvres_training_set_sample, oeuvres_eval_set_bis, taille_morceaux, analyseur, classifieur, langue = "fr")
    P.creer_textes(equilibrage = False)
    P.analyser(normalisation = False)
    P.appliquer_classifieur()
    J = P.classifieur.J
    dist = P.classifieur.dist
    plt.plot(J,dist, linestyle = "--", label = "test" + str(k) +" id")

plt.xlabel("Nombre de composantes retirées")
plt.ylabel("Séparation relative entre les paquets de textes")
plt.legend(loc="best")
plt.title("Unmasking")
plt.savefig("unmasking_graph"+ str(int(time())) + ".png")

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")
