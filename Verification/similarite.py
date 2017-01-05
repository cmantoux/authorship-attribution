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

def qual(fp,fn):
    if fp==0:
        theta = 0
    else:
        theta = np.arctan(fn/fp)
    #q = (1-(fp**2 + fn**2)/2)*np.sin(2*theta)
    #q = (1-2*fn)*(1-fp)*np.sin(2*theta)
    #q = 2 - np.sqrt(fp) - np.sqrt(fn)
    q = (1-fp**2)*(1-fn**2)*min(theta,0.2)*min((np.pi/2 - theta),0.2)*25
    return q

def trace_qual():
    X = np.linspace(0,1,100)
    Y = np.linspace(0,1,100)
    x,y = np.meshgrid(X,Y)
    z = np.zeros((100,100))
    for i in range(100):
        for j in range(100):
            z[i][j] = qual(X[i],Y[j])
    plt.title("Fonction de qualite")
    plt.xlabel("fn")
    plt.ylabel("fp")
    plt.contourf(x, y, z, 100)
    plt.colorbar()
    plt.show()

class Similarity():
    
    def __init__(self):
        print("Creation du vérificateur par similarité")
    
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
        qualite = qual(fp,fn)
        return qualite, fp, fn, q, n, mauvaises_attributions, nb_auteur_different, mauvais_rejets, nb_meme_auteur 
    
    def calibrer(self, textes_base, textes_calibrage):
        self.textes_base = textes_base

        self.M1 = np.zeros((len(textes_base), len(textes_base)))
        for i in range(len(textes_base)):
            for j in range(len(textes_base)):
                self.M1[i,j] = similarity(textes_base[i],textes_base[j])
        self.AS_base = np.mean(self.M1, axis = 0)
        self.AGS_base = np.mean(self.AS_base)
        self.marge_base = np.sqrt(np.var(self.AS_base))
        
        if len(textes_calibrage) > 0:
            
            self.textes_calibrage = rd.sample(textes_calibrage, len(textes_base))
            #self.textes_calibrage = textes_calibrage
            self.textes = self.textes_base + self.textes_calibrage
            
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
            AS_textes = []
            for t in self.textes:
                s = AS(t, self.textes_base)
                AS_textes.append(s)
            Q = []
            FP = []
            FN = []
            A = np.linspace(-1,3,50)
            for a in A:
                verif_calibrage = []
                for s in AS_textes:
                    if s > self.AGS_base - a*self.marge_base:
                        verif_calibrage.append(True)
                    else :
                        verif_calibrage.append(False)
                qualite, fp, fn, q, n, mauvaises_attributions, nb_auteur_different, mauvais_rejets, nb_meme_auteur  = self.qualite(verif_calibrage, vraie_verif_calibrage)
                
                FP.append(fp)
                FN.append(fn)
                Q.append(qualite)
            a_max = A[Q.index(max(Q))]
            print("Qualite optimale : {:f}".format(max(Q)))
            print("Valeur de a correspondante : {:f}".format(a_max))
            self.a = a_max
            plt.figure()
            plt.plot(A,Q)
            plt.title("Réglage du facteur a pour optimiser la qualité ")
            plt.xlabel("a")
            plt.ylabel("qualite de la verification de calibrage")
            plt.plot([a_max], [max(Q)], marker = "o", markersize = 5, label = "a optimal")
            plt.savefig("qualite.png")
            plt.figure()
            plt.plot(FP,FN)
            plt.xlabel("Faux positifs lors du calibrage")
            plt.ylabel("Faux négatifs lors du calibrage")
            plt.plot([FP[Q.index(max(Q))]], [FN[Q.index(max(Q))]], marker = "o", markersize = 5, label = "a optimal")
            plt.title("Compromis entre les faux positifs et négatifs")
            plt.legend(loc = "best")
            plt.savefig("compromis.png")
            plt.show()
        
        else:
            
            self.a = 0
    
    def verifier(self, textes_base, textes_disputes):
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
        qualite, fp, fn, q, n, mauvaises_attributions, nb_auteur_different, mauvais_rejets, nb_meme_auteur   = self.qualite(self.verif, self.vraie_verif)
        print("Mauvaises attributions : {} sur {}".format(mauvaises_attributions, nb_auteur_different))
        print("Mauvais rejets : {} sur {}".format(mauvais_rejets, nb_meme_auteur))
        print("Nombre de vérifications correctes : {} sur {}".format(q,n))
        print("Pourcentage d'efficacité : {} %".format(int(100*(1-(fp+fn)/2))))
    
    def afficher(self):
        print("")
        print("Résultats de la vérification")
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
                    print("L'oeuvre " + aut + str(num) + " n'a pas été écrite par " + aut_base + " : " + str(nb_vrai) + " textes contre " + str(nb_faux))
                nb_vrai = 0
                nb_faux = 0
                aut = self.textes_disputes[i+1].auteur
                num = self.textes_disputes[i+1].numero
            i+=1
        if nb_vrai>nb_faux:
            print("L'oeuvre " + aut + str(num) + " a été écrite par " + aut_base + " : " + str(nb_vrai) + " textes contre " + str(nb_faux))
        else:
            print("L'oeuvre " + aut + str(num) + " n'a pas été écrite par " + aut_base + " : " + str(nb_vrai) + " textes contre " + str(nb_faux))


def scale(courbe):
    a = courbe[0]
    if a==0:
        return courbes
    for i in range(len(courbe)):
        courbe[i]/=a

def copie(t):
    tbis = deepcopy(t)
    tbis.vecteur = np.array(deepcopy(t.vecteur))
    return tbis
    
    
###################################################################################

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
verificateur = Similarity()

liste_id_oeuvres_base = [("dumas",k) for k in range(1,4)]

liste_id_oeuvres_calibrage = [("zola",k) for k in range(1,4)]

liste_id_oeuvres_disputees = [("dumas",k) for k in range(8,10)]

V = Verification(liste_id_oeuvres_base, liste_id_oeuvres_calibrage, liste_id_oeuvres_disputees, taille_morceaux, analyseur, verificateur)
V.resoudre()