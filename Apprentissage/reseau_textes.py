# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pickle

#Adresse du fichier contenant les données de l'ensemble d'apprentisage
cheminApprentissage = "C:/Users/Clement/Downloads/donnees5"
#Adresse du fichier contenant les données de l'ensemble de test
cheminTest = "C:/Users/Clement/Downloads/donnees6"

# La plupart des paramètres sont déclarés juste avant la fonction go() (vers le bas du code)

# Crée les poids (W), les biais (b), et les fonctions d'activation de chaque couche (f)
# Le format d'entrée de la structure est par exemple, pour un réseau à 5 entrées,
# 2 couches de neurones dont une de 3 neurones et une de 10 neurones : [5,4,3]
def initialise_reseau(structure_reseau):
    W = [0]*(len(structure_reseau)-1) #Tableau des matrices de poids
    b = [0]*(len(structure_reseau)-1) #Tableau des seuils/biais
    f = [0]*(len(structure_reseau)-1) #Tableau des fonctions d'activation
    for k in range(0, len(structure_reseau)-1): #On prend des valeurs aléatoires uniformément distribuées dans [-1;1]
        W[k] = 2*np.random.rand(structure_reseau[k+1],structure_reseau[k])-1 #idem
        b[k] = 2*np.random.rand(structure_reseau[k+1],1)-1
        f[k] = logsig #Par défaut on initialise toutes les fonctions d'activation à sigmoïde
    return W,b,f

# Renvoie les sorties de chaque couche du réseau pour une entrée donnée sous forme de vecteur colonne
def propage_entree(entree, W, b):
    a = [] #Sortie des couches
    n = [] #Sortie des couches avant activation (ie. application de f[k])
    a.append(entree)
    for k in range(len(W)):
        n.append(np.dot(W[k],a[len(a)-1])-b[k])
        a.append(f[k](n[k]))
    return n,a

# FONCTIONS DE SEUILLAGE : varient en fonction des neurones, ici pour le moment c'est logsig qui est utilisée
# Ces fonctions prennent un tableau et s'appliquent à chacun de ses éléments.
def hardlim(x):
    res = []
    for y in x.transpose().tolist()[0]:
        if y>0:
            res.append(1)
        else:
            res.append(0)
    res = np.array(res).reshape(x.shape)
    return res

def logsig(x):
    res = []
    for y in x.transpose().tolist()[0]:
        res.append(1/(1+np.exp(-y)))
    res = np.array(res).reshape(x.shape)
    return res

def satlin(x):
    res = []
    for y in x.transpose().tolist()[0]:
        if y>-0.5:
            if y<0.5:
                res.append(y)
            else:
                res.append(y)
        else:
            res.append(y)
    res = np.array(res).reshape(x.shape)
    return res

def derivee_satlin(x):
    res = []
    for y in x.transpose().tolist()[0]:
        if y>-0.5:
            if y<0.5:
                res.append(1)
            else:
                res.append(1)
        else:
            res.append(1)
    res = np.array(res).reshape(x.shape)
    return res

def derive(f):
    if f==hardlim:
        return (lambda x: 0)
    if f==logsig:
        return (lambda x: np.exp(-x)/np.power(1+np.exp(-x), 2))
    if f==satlin:
        return derivee_satlin
    return (lambda x: 0)
# Fin de la partie fonctions d'activation

# A partir des sorties de chaque couche du réseau (a,n) (données par propage_entrees),
# on calcule les sensibilités (s) de chaque neurone (dérivée de l'erreur quadratique) par rétropropagation
def retropropage_sensibilites(W, f, a, n, d): #d = sortie théorique
    s = [] #Sensibilité de l'erreur de chaque couche par rapport à n
    k = len(W)-1
    sM = -2*np.dot(np.diag(derive(f[len(W)-1])(n[len(W)-1])), d-a[len(W)])
    s.append(sM)
    k -= 1
    while k>=0:
        j = np.dot(np.diag(np.transpose(derive(f[k])(n[k])).tolist()[0]),np.transpose(W[k+1])) #Un peu sale parce qu'il faut transformer n de vecteur colonne en liste python
        s0 = np.dot(j, s[len(s)-1])
        s.append(s0)
        k-=1
    s.reverse()
    for k in range(len(s)):
        s[k] = np.transpose([s[k]])
    return s

# Met à jour les poids et les biais en fonction des sensibilités (s), des sorties des neurones (a),
# du coefficient d'apprentissage (qui détermine la taille du pas qu'on fait vers la direction donnée par le gradient),
# l'inertie (momentum), qui détermine la mesure dans laquelle on continue à aller dans la direction de l'étape précédente
# (pour ne pas prendre de virages trop brusques, et pour sortie des minimas locaux)
# Les tableaux oldDeltaW et oldDeltaB servent à stocker ces directions pour l'étape suivante
def nouveaux_poids_et_biais(W, b, a, s, coeffApprentissage, oldDeltaW = 0, oldDeltaB = 0, momentum = 0):
    deltaW = [np.dot(0,w) for w in W]
    deltaB = [np.dot(0,b0) for b0 in b]
    for k in range(len(W)):
        if momentum==0:
            deltaW[k] = -2*coeffApprentissage*np.dot(s[k], np.transpose(a[k]))
            deltaB[k] = coeffApprentissage*s[k]
        else:
            deltaW[k] = momentum*oldDeltaW[k]-(1-momentum)*2*coeffApprentissage*np.dot(s[k], np.transpose(a[k]))
            deltaB[k] = momentum*oldDeltaB[k]+(1-momentum)*coeffApprentissage*s[k]
        W[k] += deltaW[k]
        b[k] += deltaB[k]
    return deltaW, deltaB

# Fonction "finale" : prend les poids et les biais, une entrée et une sortie (e) et les paramètres du réseau,
# calcule la mise à jour des poids et des biais et les renvoie
def apprend(W, b, f, coeffApprentissage, e, oldDeltaW = 0, oldDeltaB = 0, momentum = 0): #e = [entrée, sortie]
    n, a = propage_entree(e[0], W, b) #L'entrée est un vecteur colonne
    s = retropropage_sensibilites(W, f, a, n, e[1]) #s est un vecteur colonne
    return nouveaux_poids_et_biais(W, b, a, s, coeffApprentissage, oldDeltaW, oldDeltaB, momentum)

#Ensemble d'apprentissage
with open(cheminApprentissage,  "rb" ) as mon_fichier:
    mon_depickler = pickle.Unpickler(mon_fichier) 
    oeuvres_vecteurs = mon_depickler.load()

#Ensemble de test
with open(cheminTest,  "rb" ) as mon_fichier:
    mon_depickler = pickle.Unpickler(mon_fichier) 
    oeuvres_vecteurs_test = mon_depickler.load()

#Calcule la sortie du réseau pour une entrée donnée sous forme de vecteur colonne
def sortie(entree):
    global W,b
    n,a = propage_entree(entree, W, b)
    return a[len(a)-1]

#Dit si un élément de l'ensemble d'apprentissage est censé être reconnu par le réseau
def is_ok(k):
    return k<10 #Par exemple, ici, les 10 premiers textes seulement sont de Dumas

#Transforme une liste python en vecteur colonne
def col(l):
    return [[x] for x in l]
    
#Renvoie la norme de v
def norme(v):
    res = 0
    for x in v:
        res+= np.power(x,2)
    return np.sqrt(res)

#Initialise les poids et biais à leur valeur optimale
def setMin():
    W,b = Wmin, bmin

#Calcule l'erreur du réseau sur une valeur
def erreur_quadratique_valeur(k):
    global oeuvres_vecteurs
    if is_ok(k):
        b=1
    else:
        b=0
    return np.power(abs(b-sortie(oeuvres_vecteurs[k][0])[0][0]),2)

#Calcule l'erreur totale du réseau sur l'ensemble donné en argument
def erreur_quadratique_ensemble(st):
    e = 0
    for k in range(len(st)):
        e += erreur_quadratique_valeur(k)
    return e

#VALIDATION DU RESEAU

#On indique si chaque oeuvre doit être reconnue
for k in range(10):
    oeuvres_vecteurs[k] = [col(oeuvres_vecteurs[k]), 1] #oeuvres de Dumas
for k in range(10, len(oeuvres_vecteurs)):
    oeuvres_vecteurs[k] = [col(oeuvres_vecteurs[k]), 0] #oeuvres de Maquet et Hugo

setApprentissage = oeuvres_vecteurs

#STRUCTURE DU RESEAU
#[nombre_entrees, taille des couches]
structure_reseau = np.array([20,4,1])

W,b,f = initialise_reseau(structure_reseau)
coeffApprentissage = 0.1
momentum = 0. #Pas de momentum (le réseau de textes converge sans pour le moment)

#On initialise ces variables (qui servent dans la mise à jour des poids
oldDeltaW = [np.dot(0,w) for w in W]
oldDeltaB = [np.dot(0,b0) for b0 in b]

# Plusieurs variables qui servent dans la boucle :
renormage = False #Si activé, conserve la norme des poids à  (mais fais perdre en précision)
verbose = False #Si activé, affiche les poids dans la console
erreur = 10 #On initialise l'erreur (pour ne pas s'arrêter au début de la boucle)
cpt = 0 #Compteur d'étapes
Wmin, bmin = W, b #Valeurs des poids et des biais pour lesquelles le réseau a atteint sa meilleure performance
erreurMin = 10 #On initialise l'erreur minimale à 10, elle sera mise à jour dès qu'on tombera sur plus petit
borneArret = 0.005 #si erreur<borneArret, la boucle s'arrête

# Boucle d'apprentissage du réseau :
# A chaque tour de boucle, on fait apprendre au réseau tout l'ensemble d'apprentissage
# Tant que le résultat de sortie n'est pas assez proche de celui qu'on veut
def go():
    global cpt, erreur, oldDeltaW, oldDeltaB, renormage, verbose, Wmin, bmin, erreurMin
    while erreur>borneArret : #Tant que l'erreur quadratique totale est trop élevée, on continue
        cpt+=1
        cpt2 = 0
        for i in range(len(setApprentissage)): #On parcourt l'ensemble d'apprentissage
            cpt2+=1
            if cpt2==1 and renormage: #Si activé, régule les normes des poids à 1 (mais perte de précision)
                cpt2=0
                #On renorme les poids
                print "Normage des poids à 1"
                for k in range(len(W)):
                    for i in range(len(W[k])):
                        W[k][i] = W[k][i]/norme(W[k][i])
                if verbose: print W
            #On fait apprendre au réseau l'élément de l'ensemble d'apprentissage
            oldDeltaW, oldDeltaB = apprend(W, b, f, coeffApprentissage, setApprentissage[i], oldDeltaW, oldDeltaB, momentum)
        erreur = erreur_quadratique_ensemble(setApprentissage)
        if erreur<erreurMin: #Si on bat notre record, on met à jour Wmin et bmin
            erreurMin = erreur
            Wmin, bmin = W, b
        if cpt%1 == 0: #Changer 1 en n>1 pour régler la fréquence d'affichage
            print erreur, cpt

go()

#Affiche la sortie du réseau sur l'ensemble d'apprentissage
def aff1():
    for i in range(len(oeuvres_vecteurs)):
        print sortie(oeuvres_vecteurs[i][0])

#Affiche la sortie du réseau sur les textes à tester
def aff2():
    for i in range(len(oeuvres_vecteurs_test)):
        print sortie(col(oeuvres_vecteurs_test[i]))

def poids_composantes():
    global W
    tab = [0]*len(W[0][0])
    for i in range(len(W[0])):
        for j in range(len(W[0][i])):
            tab[j]+=abs(W[0][i][j])
    for poids in tab:
        print poids

print "===="
print "apprentissage terminé en {0} étapes".format(cpt)
