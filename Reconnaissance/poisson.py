from classes import *
from carac import *
import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rd
import math

def fonc_repart_poisson(lam,x):
    p = np.exp(-lam)
    Px = 0
    for n in range(math.floor(x) + 1):
        Px += p
        p *= (lam/(n+1))
    return Px

def fonc_repart(lam,N,x):
    return fonc_repart_poisson(lam*N,N*x)

def prob_int(lam,N,x,y):
    return fonc_repart(lam,N,y) - fonc_repart(lam,N,x)

def int_conf(lam,N,alpha = 0.1):
    pas = 1/(2*N)
    x,y = lam,lam
    #print(x,y)
    while prob_int(lam,N,x,y) < 1-alpha:
        P = prob_int(lam,N,x,y)
        y += pas
        x -= pas
        #print(x,y, P)
    #print(prob_int(lam,N,x,y))
    return (max(0,x),y)


taille_morceaux = 5000

textes = []
textes2 = []

for k in range(1,19):
    o = Oeuvre("dumas",k)
    textes.extend(o.split(taille_morceaux))


for k in range(1,6)
    o = Oeuvre("hugo",k)
    textes2.extend(o.split(taille_morceaux))

N = len(textes)
nb_col = int(np.sqrt(N)/2)

a = Analyseur([freq_lettres])

for t in textes:
    a.analyser(t)
for t2 in textes2:
    a.analyser(t2)

plt.close()
    
j = 2
values = np.array([t.vecteur[j] for t in textes])

lam = np.mean(values)
inf, sup = int_conf(lam,N)
plt.plot(np.linspace(inf,sup,10),np.linspace(0,0,10), linewidth = 10)
P = rd.poisson(N*lam, N)/N
plt.hist([values,P], nb_col, normed = 1, alpha = 0.5)
plt.xlabel(a.noms_composantes[j])
plt.ylabel("Effectifs")
plt.savefig(a.noms_composantes[j])
plt.show()


vecteurs = np.array([t.vecteur for t in textes])
lams = np.mean(vecteurs, axis = 0)
infs, sups = [],[]
for lam in lams:
    i,s = int_conf(lam,N,0.5)
    infs.append(i)
    sups.append(s)

def pourcentage_contraintes(t,infs,sups):
    k = 0
    for j in range(len(t.vecteur)):
        x = t.vecteur[j]
        if (x > infs[j] and x < sups[j]):
            k += 1
    return k/len(t.vecteur)

pourcentages_identiques = []
for t in textes:
    pourcentages_identiques.append(pourcentage_contraintes(t,infs,sups))
pourcentages_differents = []
for t2 in textes2:
    pourcentages_differents.append(pourcentage_contraintes(t2,infs,sups))

m = np.mean(pourcentages_identiques)
m2 = np.mean(pourcentages_differents)