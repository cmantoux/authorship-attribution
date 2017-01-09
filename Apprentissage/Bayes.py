import pickle
from classes import *
from math import sqrt
from math import pi
from math import e
import numpy as np



#exemples est une liste de vecteurs, chaque vecteurs représentant un texte
#auteurs est une liste de même taille que exemples telle que auteur[i] soit l'auteur de exemples[i]

def f(exemples, auteurs):
    k = len(exemples) #compte le nombre d'exemples
    m = len(exemples[0]) #compte le nombre de coordonnées d'un vecteur
    Noms = [] #Liste destinée à contenir le nom de chaque auteur de manière unique
    Classes = []
    for i in range(k):#boucle pour remplir les listes
        if not(auteurs[i] in Noms):
            Noms += [auteurs[i]]
            texte = np.asarray(exemples[i])
            Classes += [texte]
        else:
            l = Noms.index(auteurs[i])
            texte = np.asarray(exemples[i])
            Classes[l] = np.concatenate((Classes[l], texte), axis=0)
    
    n = len(Noms) #Nombre de catégories différentes
    moyenne = np.zeros((n,m)) #Tableau destiné à contenir le vecteur moyen de chaque catégorie
    ecart_type = np.zeros((n,m)) #Tableau destiné à contenir le vecteur écart-type de chaque catégorie
    
    for i in range(n):
       moyenne[i] = np.mean(Classes[i], 0)
       ecart_type[i] = np.sqrt(np.var(Classes[i], 0))       
    
    return moyenne, ecart_type, Noms


def g(moyenne, ecart_type, inconnus):
    m = len(inconnus) #nombre de vecteurs de texte inconnus
    n = moyenne.shape[1] #nombre de coordonnées d'un vecteur
    k = moyenne.shape[0] #nombre de catégories

    Probabilite  = np.ones((m,k)) #Création de la matrice stochastique de résultats

    #Remplissage de la matrice
    for i in range (m): 
        for l in range(k):
            for j in range(n):
                Probabilite[i][l] *= 1/(sqrt(2*pi)*ecart_type[l][j]) * e**(-1/2*((inconnus[i][j]-moyenne[l][j])/ecart_type[l][j])**2)
    
    return Probabilite

class Bayes(Classifieur):
    
    def __init__(self):
        print("Création du classifieur Bayes")
        self.eval_set = None
        self.training_set = None
        self.p = None
        self.p_ref = None
        self.precision = None
        pass
    
    def classifier(self, training_set, eval_set):
        self.eval_set = eval_set
        self.training_set = training_set
        vecteurs_training = [t.vecteur for t in training_set]
        auteurs_training = [t.auteur for t in training_set]
        vecteurs_eval = [t.vecteur for t in eval_set]
        auteurs_eval = [t.auteur for t in eval_set]
        Intermediaires = f(vecteurs_training, auteurs_training)
        Probabilite = g(Intermediaires[0], Intermediaires[1], vecteurs_eval)
        self.auteurs = Intermediaires[2]
        self.p = Probabilite
        k = np.shape(Probabilite)[1]
        m = np.shape(Probabilite)[0]
        Reference = np.zeros((m,k))
        for i in range(m):
            max = Probabilite[i][0]
            categorie = 0
            for j in range(k):
                if(Probabilite[i][j]>max):
                    max = Probabilite[i][j]
                    categorie = j
            ref = Intermediaires[2].index(auteurs_eval[i])
            if(ref==categorie):
                vrai += 1
            else:
                faux += 1
            Reference[i][ref] = 1
        self.p_ref = Reference

                
        
            
            