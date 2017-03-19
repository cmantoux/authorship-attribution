import pickle
from classes import *
from math import sqrt
from math import pi
from math import e
import numpy as np



#exemples est une liste de vecteurs, chaque vecteurs représentant un texte
#auteurs est une liste de même taille que exemples telle que auteur[i] soit l'auteur de exemples[i]

def f(vecteur_training, categorie_training, categories):
    k = len(vecteur_training) #compte le nombre de vecteurs
    n = len(categories) #compte le nombre de categories
    m = len(vecteur_training[0]) #compte le nombre de coordonnées d'un vecteur
    #on veut convertir training_set en un tableau Classes de numpy où les vecteurs sont rassemblés par catégorie
    Classes = [0]*n #initialisation de Classes
    Test = [True]*n
    for j in range(k): #on parcourt les vecteurs
        texte = np.asarray(vecteur_training[j]) #on convertit le vecteur en numpy
        c = categories.index(categorie_training[j])
        if(Test[c]):
            Classes[c] = [texte]
            Test[c] = False
        else:
            Classes[c] += [texte]
    
    moyenne = np.zeros((n,m)) #Tableau destiné à contenir le vecteur moyen de chaque catégorie
    ecart_type = np.zeros((n,m)) #Tableau destiné à contenir le vecteur écart-type de chaque catégorie
    
    for i in range(n):
       moyenne[i] = np.mean(Classes[i], 0)
       ecart_type[i] = np.sqrt(np.var(Classes[i], 0))       
    return moyenne, ecart_type


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
    
    def classifier(self, training_set, eval_set, categories):
        self.eval_set = eval_set
        self.training_set = training_set
        self.categories = categories
        vecteurs_eval = [t.vecteur for t in eval_set]
        categories_eval = [t.categorie for t in eval_set]
        vecteur_training = [t.vecteur for t in training_set]
        categorie_training = [t.categorie for t in training_set]
        Intermediaires = f(vecteur_training, categorie_training, categories)
        Probabilite = g(Intermediaires[0], Intermediaires[1], vecteurs_eval)
        print(Intermediaires[1])
        self.p = Probabilite
        k = np.shape(Probabilite)[1]
        m = np.shape(Probabilite)[0]
        Reference = np.zeros((m,k))
        vrai = 0
        faux = 0
        clusters = []
        cat = ['none']*len(categories)
        c = -1
        for i in range(m):
            max = Probabilite[i][0]
            categorie = 0
            for j in range(k):
                if(Probabilite[i][j]>max):
                    max = Probabilite[i][j]
                    categorie = j
            if(cat[categorie]=='none'):
                clusters += [[eval_set[i]]]
                c += 1
                cat[categorie] = c
            else:
                clusters[cat[categorie]] += [eval_set[i]]
            ref = categories.index(categories_eval[i])
            if(ref==categorie):
                vrai += 1
            else:
                faux += 1
            Reference[i][ref] = 1
        self.p_ref = Reference
        self.clusters = clusters

                
        
            
            