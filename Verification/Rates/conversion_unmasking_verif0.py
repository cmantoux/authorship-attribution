from time import time
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from carac import *
import numpy as np
import numpy.linalg as alg
import random as rd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from Apprentissage.svm import SVM
from classes import Analyseur, Verification
from Utilitaires.equilibrage_et_normalisation import normaliser1, equilibrer1
from matplotlib import cm
from copy import deepcopy


class Unmasking():
    
    def __init__(self):
        print("Creation du verificateur par démasquage")
        self.nb_essais = 5
        self.moyennage = 5
        self.taille_echantillon = 20
        self.pas = 5
    
    def reordonner_composantes(self, textes1, textes2):
        vecteurs1 = np.array([t.vecteur for t in textes2])
        moyennes1 = vecteurs1.mean(axis=0)
        variances1 = vecteurs1.var(axis=0)
        
        vecteurs2 = np.array([t.vecteur for t in textes2])
        moyennes2 = vecteurs2.mean(axis=0)
        variances2 = vecteurs2.var(axis=0)
        
        nb_composantes = len(vecteurs1[0])
        variances = (variances2 + variances1)/2
        importances = np.abs(moyennes2-moyennes1)/np.sqrt(variances)
        
        ordre = sorted(list(range(nb_composantes)), key = lambda i : importances[i])
        importances.sort()
        for t in textes1:
            v = t.vecteur.copy()
            for i in range(nb_composantes):
                t.vecteur[ordre[i]] = v[i]
        for t in textes2: 
            v = t.vecteur.copy()
            for i in range(nb_composantes):
                t.vecteur[ordre[i]] = v[i]
    
    def creer_courbes(self, textes1, textes2):
        self.reordonner_composantes(textes1,textes2)
        nb_composantes = len(textes1[0].vecteur)
        for t in textes1:
            t.auteur = "auteur1"
        for t in textes2:
            t.auteur = "auteur2"
        textes = equilibrer1(textes1+textes2)
        courbes = [[] for e in range(self.nb_essais)]
        for j in self.J:
            print("Nombre de composantes retirées : {}".format(j))
            k = nb_composantes-j
            for t in textes:
                t.vecteur = t.vecteur[:k]
            for e in range(self.nb_essais):
                precision_moyenne = 0
                for m in range(self.moyennage):
                    #print("Essai n°{}".format(e), sep = ' ')
                    classifieur = SVM(pc = False)
                    indices = np.random.choice(len(textes),self.taille_echantillon)
                    non_indices = [i for i in range(len(textes)) if not (i in indices)]
                    eval_set = [textes[i] for i in indices]
                    training_set = [textes[i] for i in non_indices]
                    classifieur.classifier(training_set, eval_set)
                    precision_moyenne += classifieur.precision
                courbes[e].append(precision_moyenne/self.moyennage)
        for c in courbes:
            a = c[0]
            if a > 0:
                for i in range(len(c)):
                    c[i] = c[i]/a
        return courbes
        
    def calibrer(self, textes_base, textes_calibrage):
        
        nb_composantes = len(textes_base[0].vecteur)
        self.J = list(range(0,nb_composantes,self.pas))

        print("Création des courbes auteurs identiques")
        
        nums_base = [t.numero for t in textes_base]
        m = len(nums_base)
        textes_base1 = [copie(t) for t in textes_base if t.numero in nums_base[:int(m/2)]]
        textes_base2 = [copie(t) for t in textes_base if t.numero in nums_base[int(m/2):]]
                
        self.reordonner_composantes(textes_base1, textes_base2)
        self.courbes_id = self.creer_courbes(textes_base1, textes_base2)
        
        print("Création des courbes auteurs differents")
        
        textes_base3 = []
        textes_calibrage1 = []
        for t in textes_base:
            textes_base3.append(copie(t))
        for t in textes_calibrage:
            textes_calibrage1.append(copie(t))
            
        self.reordonner_composantes(textes_base3, textes_calibrage1)
        self.courbes_dif = self.creer_courbes(textes_base3, textes_calibrage1)
    
    def verifier(self, textes_base, textes_disputes):
        
        print("Creation des courbes de verification")
        
        textes_base4 = []
        textes_disputes1 = []
        for t in textes_base:
            textes_base4.append(copie(t))
        for t in textes_disputes:
            textes_disputes1.append(copie(t))
            
        self.reordonner_composantes(textes_base4, textes_disputes1)
        self.courbes_verif = self.creer_courbes(textes_base4, textes_disputes1)
        
        vecteurs_training = []
        labels_training = []
        for c in self.courbes_id:
            vecteurs_training.append(c)
            labels_training.append("id")
        for c in self.courbes_dif:
            vecteurs_training.append(c)
            labels_training.append("dif")
        
        clf = SVC()
        clf.fit(vecteurs_training, labels_training)
        self.labels = []
        for c in self.courbes_verif:
            label = clf.predict([c])[0]
            self.labels.append(label)
    
    def afficher(self):
        print(self.labels)
        CM_id = np.mean(self.courbes_id, axis = 0)
        CM_dif = np.mean(self.courbes_dif, axis = 0)
        CM_verif = np.mean(self.courbes_verif, axis = 0)
        plt.close()
        plt.plot(self.J, CM_id, label = "id")
        plt.plot(self.J, CM_dif, label = "dif")
        plt.plot(self.J, CM_verif, label = "verif")
        plt.legend(loc = "best")
        plt.xlabel("Nombre de composantes retirees")
        plt.ylabel("Precision relative du classifieur")
        plt.show()
    

######################################################################

taille_morceaux = 1000
analyseur = Analyseur([freq_ponct, freq_gram, plus_courants, freq_lettres])
verificateur = Unmasking()

liste_id_oeuvres_base = [("dumas",k) for k in range(1,4)]

liste_id_oeuvres_calibrage = [("zola",k) for k in range(1,4)]

liste_id_oeuvres_disputees = [("dumas",k) for k in range(8,10)]

V = Verification(liste_id_oeuvres_base, liste_id_oeuvres_calibrage, liste_id_oeuvres_disputees, taille_morceaux, analyseur, verificateur)
V.resoudre()