
import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/Projets-git/psc")
from time import time
from Carac.carac_ponct import *
from Carac.carac_complexite import *
from Carac.carac_stopwords import *
from classes import *
import numpy as np
from numpy.linalg import norm
import numpy.random as rd
import matplotlib.pyplot as plt
from classes import Classifieur,Probleme,Analyseur
from Interpretation.importance_composantes import importance, gain_information
from Apprentissage.svm import SVM
from Clustering.kmeans import Kmeans
from Utilitaires.defuzze import defuzze
import Evaluation.evaluation_externe as ee
from Utilitaires.equilibrage_et_normalisation import equilibrer1

def surete(d_id, d_dif):
    s = np.abs(d_id-d_dif)/np.max(d_id,d_dif) 
    return s
    
def lissage(courbe, k = 1):
    if k==0:
        return courbe
    c = lissage(courbe,k-1)
    c2 = np.zeros((len(c)))
    for i in range(len(c)-1):
        c2[i] = (c[i] + c[i+1])/2
    return c2
    

class UnmaskingCourbes(Classifieur):

    def __init__(self, nb_essais, pas, taille_echantillon, facteur):
        self.training_set = None
        self.eval_set = None
        self.nb_essais = nb_essais
        self.pas = pas
        self.taille_echantillon = taille_echantillon
        self.facteur = facteur
        self.equi = False

    def classifier(self, training_set, eval_set, categories):
        self.training_set = training_set
        self.eval_set = eval_set
        self.categories = categories

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
        
        ordre = sorted(list(range(nb_composantes)), key = lambda x : importances[x])
        importances.sort()
        nouvelles_categories = ["categorie 1", "categorie 2"]
        for t in training_set:
            t.auteur = t.auteur + "1" 
            t.categorie = "categorie 1" 
            v = t.vecteur.copy()
            for i in range(nb_composantes):
                t.vecteur[ordre[i]] = v[i]
        for t in eval_set: 
            t.auteur = t.auteur + "2"
            t.categorie = "categorie 2" 
            v = t.vecteur.copy()
            for i in range(nb_composantes):
                t.vecteur[ordre[i]] = v[i]

        textes = training_set
        textes.extend(eval_set)
        if self.equi:
            textes = equilibrer1(textes)
        self.J = list(range(0,nb_composantes-self.pas,self.pas))
        self.precision = []
        for j in self.J:
            print("Nombre de composantes retirées : {}".format(j))
            precision_moyenne = 0
            k = nb_composantes-j
            for t in textes:
                t.vecteur = t.vecteur[:k]
            for e in range(self.nb_essais):
                nb_loupes = 0
                #print("Essai n°{}".format(e))
                classifieur = SVM(pc = False)
                indices = rd.choice(len(textes),min(self.taille_echantillon, len(textes)//self.facteur))
                #non_indices = [i for i in range(len(textes)) if not (i in indices)]
                non_indices = rd.choice(len(textes),min((self.facteur-1)*self.taille_echantillon, len(textes)*(self.facteur-1)//self.facteur))
                eval_set_bis = [textes[i] for i in indices]
                training_set_bis = [textes[i] for i in non_indices]
                m = 0
                while len(list(set([t.auteur for t in training_set_bis])))<=1 and m < 20:
                    m+=1
                    indices = rd.choice(len(textes),min(self.taille_echantillon, len(textes)//self.facteur))
                    #non_indices = [i for i in range(len(textes)) if not (i in indices)]
                    non_indices = rd.choice(len(textes),min((self.facteur-1)*self.taille_echantillon, len(textes)*(self.facteur-1)//self.facteur))
                if len(list(set([t.auteur for t in training_set_bis])))<=1 or len(training_set)<4 or len(eval_set_bis)<4:
                    nb_loupes += 1
                else:
                    classifieur.classifier(training_set_bis, eval_set_bis, nouvelles_categories)
                    precision_moyenne+= ee.precision(classifieur.eval_set,defuzze(classifieur.p),classifieur.p_ref)
            if nb_loupes >= self.nb_essais - 4 :
                raise ValueError("Les corpus sont trop petits")
            precision_moyenne /= (self.nb_essais-nb_loupes)
            self.precision.append(precision_moyenne)
        return

    def afficher(self):
        return

class Unmasking:
    
    def __init__(self, nb_selections = 1, nb_oeuvres = 2, taille_echantillon = 10, facteur = 3, lissage = 0, nb_essais = 10, pas = 3,langue = "fr"):
        self.taille_morceaux = 1000
        self.analyseur = None
        self.J = None
        self.auteur_base = "?"
        self.cat_base = "?"
        self.nb_selections = nb_selections
        self.nb_oeuvres = nb_oeuvres
        self.taille_echantillon = taille_echantillon
        self.facteur = facteur
        self.lissage = lissage
        self.nb_essais = nb_essais
        self.pas = pas
        self.verif = []
        self.PM_verif = []
        self.PM_id = None
        self.PM_dif = None
        self.taux = []
        self.langue = langue
    
    def calibrer(self, textes_base, textes_calibrage):
        self.auteur_base = textes_base[0].auteur
        self.cat_base = textes_base[0].categorie
        for k in range(self.nb_selections):
            print("")
            print("Paire de courbes de calibrage n°{}".format(k+1))
            print("")
            lb = min(self.nb_oeuvres, len(self.liste_id_oeuvres_base))
            lc = min(self.nb_oeuvres, len(self.liste_id_oeuvres_calibrage))
            ob1_ind = np.random.choice(len(self.liste_id_oeuvres_base), lb)
            ob2_ind = np.random.choice(len(self.liste_id_oeuvres_base), lb)
            oc1_ind = np.random.choice(len(self.liste_id_oeuvres_calibrage), lc)
            #while len(set(ob2_ind).intersection(set(ob1_ind))) > 0:
                #print("blabla")
                #ob2_ind = np.random.choice(len(self.liste_id_oeuvres_base), lb)
            ob1 = [[self.liste_id_oeuvres_base[i] for i in ob1_ind]]
            ob2 = [[self.liste_id_oeuvres_base[i] for i in ob2_ind]]
            oc1 = [[self.liste_id_oeuvres_calibrage[i] for i in oc1_ind]]
            
            classifieur_id = UnmaskingCourbes(self.nb_essais, self.pas, self.taille_echantillon, self.facteur)
            P_id = Probleme(ob1, self.categories_base, ob2, self.categories_base, self.taille_morceaux, self.analyseur, classifieur_id, self.langue)
            P_id.creer_textes(equilibrage = True, equilibrage_eval = False)
            P_id.analyser(normalisation = True)
            P_id.appliquer_classifieur()
            J = P_id.classifieur.J
            precision1 = P_id.classifieur.precision
            a = precision1[0]
            precision1 = [p/a for p in precision1]
            #plt.plot(J,precision1, linestyle = "--", color = "b")

            classifieur_dif = UnmaskingCourbes(self.nb_essais, self.pas, self.taille_echantillon, self.facteur)
            P_dif = Probleme(ob1, self.categories_base, oc1, self.categories_calibrage, self.taille_morceaux, self.analyseur, classifieur_dif, self.langue)
            P_dif.creer_textes(equilibrage = True, equilibrage_eval = False)
            P_dif.analyser(normalisation = True)
            P_dif.appliquer_classifieur()
            J = P_dif.classifieur.J
            precision2 = P_dif.classifieur.precision
            a = precision2[0]
            precision2 = [p/a for p in precision2]
            #plt.plot(J,precision2, linestyle = "--", color = "r")
            
            if k==0:
                self.PM_id = np.zeros((len(precision1)))
                self.PM_dif = np.zeros((len(precision2)))
            self.PM_id += precision1
            self.PM_dif += precision2
        
        self.J = J
        self.PM_id /= self.nb_selections
        self.PM_dif /= self.nb_selections
        
        self.PM_id = lissage(self.PM_id, self.lissage)
        self.PM_dif = lissage(self.PM_dif, self.lissage)
    
    def verifier(self, textes_base, textes_disputes):
        for i in range(len(self.liste_id_oeuvres_disputees)):
            for k in range(self.nb_selections):
                print("")
                print("Courbe de vérification n°{} pour l'oeuvre disputee {}".format(k+1, i+1))
                print("")
                lb = min(self.nb_oeuvres, len(self.liste_id_oeuvres_base))
                ob1_ind = np.random.choice(len(self.liste_id_oeuvres_base), lb)
                ob1 = [[self.liste_id_oeuvres_base[i] for i in ob1_ind]]
                od1 = [[self.liste_id_oeuvres_disputees[i]]]
 
                classifieur_verif = UnmaskingCourbes(self.nb_essais, self.pas, self.taille_echantillon, self.facteur)
                P_verif = Probleme(ob1, self.categories_base, od1, self.categories_disputees, self.taille_morceaux, self.analyseur, classifieur_verif, self.langue)
                P_verif.creer_textes(equilibrage = True, equilibrage_eval = False)
                P_verif.analyser(normalisation = True)
                P_verif.classifieur.equi = True
                P_verif.appliquer_classifieur()
                J = P_verif.classifieur.J
                precision3 = P_verif.classifieur.precision
                a = precision3[0]
                precision3 = [p/a for p in precision3]
                #plt.plot(J,precision3, linestyle = "--", color = "b")
                
                if k==0:
                    self.PM_verif.append(np.zeros((len(precision3))))
                self.PM_verif[i] += precision3
            
            self.PM_verif[i] /= self.nb_selections
            self.PM_verif[i] = lissage(self.PM_verif[i], self.lissage)
            d_id = norm(self.PM_verif[i] - self.PM_id)
            d_dif = norm(self.PM_verif[i] - self.PM_dif)
            if d_id < d_dif:
                self.verif.append(True)
            else:
                self.verif.append(False)
            self.taux.append([d_id,d_dif])
    
    def afficher(self):
        print("")
        for i in range(len(self.liste_id_oeuvres_disputees)):
            aut = self.liste_id_oeuvres_disputees[i][0]
            num = self.liste_id_oeuvres_disputees[i][1]
            t = self.taux[i]
            if self.verif[i]:
                print("L'oeuvre disputée " + aut + str(num) + " est attribuée à la categorie de base " + self.cat_base + ". \nDistances aux courbes de référence : id {:f} / dif {:f}".format(t[0],t[1]))  
            else:
                print("L'oeuvre disputée " + aut + str(num) + " n'est pas attribuée à la categorie de base " + self.cat_base + ". \nDistances aux courbes de référence : id {:f} / dif {:f}".format(t[0],t[1])) 
            print("")
            plt.figure()
            plt.plot(self.J,self.PM_id, linewidth = 2, color = "g", label = self.auteur_base + " / " + self.auteur_base)
            plt.plot(self.J,self.PM_dif, linewidth = 2, color = "r", label = self.auteur_base + " / auteur different")
            plt.plot(self.J,self.PM_verif[i], linewidth = 2, color = "b", label = self.auteur_base + " / auteur inconnu")
            
            plt.xlabel("Nombre de composantes stylistiques retirées")
            plt.ylabel("Precision relative du classifieur")
            plt.legend(loc="best")
            plt.title("Unmasking")
            plt.savefig("unmasking_graph"+ str(int(time())) + ".png")
            #plt.show()
            plt.close()



