import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/psc")
import numpy as np
import numpy.linalg as alg
import random as rd
import matplotlib.pyplot as plt
from time import time

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
    alpha = 0.4
    q = (1-fp**2)*(1-fn**2)*min(theta,alpha)*min((np.pi/2 - theta),alpha)*(1/alpha**2)
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
    plt.savefig("graphe_qualite.png")
    plt.show()

def eval_qualite(verif, vraie_verif):
    n = len(verif)
    nb_meme_categorie = 0
    nb_categorie_different = 0
    mauvaises_attributions = 0
    mauvais_rejets = 0
    q = 0
    for i in range(n):
        if verif[i] == vraie_verif[i]:
            q += 1
        if vraie_verif[i]:
            nb_meme_categorie += 1
            if not verif[i]:
                mauvais_rejets += 1
        if not vraie_verif[i]:
            nb_categorie_different += 1
            if verif[i]:
                mauvaises_attributions += 1
    if nb_categorie_different == 0:
        fp = 0
    else:
        fp = mauvaises_attributions / nb_categorie_different
    if nb_meme_categorie == 0:
        fn = 0
    else:
        fn = mauvais_rejets / nb_meme_categorie
    qualite = qual(fp, fn)
    return qualite, fp, fn, q, n, mauvaises_attributions, nb_categorie_different, mauvais_rejets, nb_meme_categorie


def evaluer(verif, vraie_verif):
    qualite, fp, fn, q, n, mauvaises_attributions, nb_categorie_different, mauvais_rejets, nb_meme_categorie = eval_qualite(
        verif, vraie_verif)
    print("Mauvaises attributions : {} sur {}, soit {} %".format(mauvaises_attributions, nb_categorie_different,
                                                                 int(100 * fp)))
    print("Mauvais rejets : {} sur {}, soit {} %".format(mauvais_rejets, nb_meme_categorie, int(100 * fn)))
    # print("Nombre de vérifications correctes : {} sur {}".format(q,n))
    print("Efficacité moyenne : {} %".format(int(100 * (1 - (fp + fn) / 2))))

class Similarity:
    
    def __init__(self):
        print("Creation du vérificateur par similarité")
        self.plot = False
        self.textes_base = None
        self.textes_calibrage = None
        self.textes_disputes = None
        self.textes = None
        self.M1 = None
        self.AS_base = None
        self.AGS_base = None
        self.marge_base = None
        self.AS_calibrage = None
        self.ADGS_calibrage = None
        self.marge_calibrage = None
        self.verif_calibrage = None
        self.vraie_verif_calibrage = None
        self.a = None
        self.verif = None
        self.vraie_verif = None
    
    def calibrer(self, textes_base, textes_calibrage):
        m = min(len(textes_base), len(textes_calibrage))
        self.textes_base = rd.sample(textes_base, m)
        self.textes_calibrage = rd.sample(textes_calibrage, m)

        self.M1 = np.zeros((len(textes_base), len(textes_base)))
        for i in range(len(textes_base)):
            for j in range(len(textes_base)):
                self.M1[i,j] = similarity(textes_base[i],textes_base[j])
        self.AS_base = np.mean(self.M1, axis = 0)
        self.AGS_base = np.mean(self.AS_base)
        self.marge_base = np.sqrt(np.var(self.AS_base))
        
        if len(self.textes_calibrage) > 0:
            self.textes = self.textes_base + self.textes_calibrage
            
            self.AS_calibrage = []
            for t in self.textes_calibrage:
                self.AS_calibrage.append(AS(t,self.textes_base))
            self.ADGS_calibrage = np.mean(self.AS_calibrage)
            self.marge_calibrage = np.sqrt(np.var(self.AS_calibrage))
            
            print("Largeur de la base : {:3f} +- {:3f}".format(self.AGS_base, self.marge_base))
            print("Largeur du corpus de calibrage : {:3f} +- {:3f}".format(self.ADGS_calibrage, self.marge_calibrage))
            
            vraie_verif_calibrage = []
            categorie_base = self.textes_base[0].categorie
            for t in self.textes:
                categorie_theorique = t.categorie
                if categorie_theorique == categorie_base:
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
                qualite, fp, fn, q, n, mauvaises_attributions, nb_categorie_different, mauvais_rejets, nb_meme_categorie  = eval_qualite(verif_calibrage, vraie_verif_calibrage)
                
                FP.append(fp)
                FN.append(fn)
                Q.append(qualite)
            a_max = A[Q.index(max(Q))]
            print("Qualite optimale : {:f}".format(max(Q)))
            print("Valeur de a correspondante : {:f}".format(a_max))
            self.a = a_max
            
            self.verif_calibrage = []
            for s in AS_textes:
                if s > self.AGS_base - self.a*self.marge_base:
                    self.verif_calibrage.append(True)
                else :
                    self.verif_calibrage.append(False)
            self.vraie_verif_calibrage = vraie_verif_calibrage
            
            if self.plot:
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
        w = len(textes_base)
        w += 1
        self.textes_disputes = textes_disputes
        self.verif = []
        self.vraie_verif = []
        categorie_base = self.textes_base[0].categorie
        for t in textes_disputes:
            s = AS(t, self.textes_base)
            if s > self.AGS_base - self.a*self.marge_base:
                # il est suffisamment proche de la base
                self.verif.append(True)
            else :
                self.verif.append(False)
            categorie_theorique = t.categorie
            if categorie_theorique == categorie_base:
                self.vraie_verif.append(True)
            else:
                self.vraie_verif.append(False)
        

    
    def afficher(self):
        self.oeuvres = []
        self.vrais = []
        self.faux = []
        print("")
        print("Performance sur le calibrage")
        print("")
        evaluer(self.verif_calibrage, self.vraie_verif_calibrage)
        print("")
        print("Performance sur la verification")
        print("")
        evaluer(self.verif, self.vraie_verif)
        print("")
        aut_base = self.textes_base[0].categorie
        self.cat_base = aut_base
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
                    print("L'oeuvre " + aut + str(num) + " est dans la catégorie " + aut_base + " : " + str(nb_vrai) + " textes acceptés contre contre " + str(nb_faux) + " rejetés.")
                else:
                    print("L'oeuvre " + aut + str(num) + " n'est pas dans la catégorie " + aut_base + " : " + str(nb_vrai) + " textes acceptés contre " + str(nb_faux) + " rejetés.")
                self.oeuvres.append((aut,num))
                self.vrais.append(nb_vrai)
                self.faux.append(nb_faux)
                nb_vrai = 0
                nb_faux = 0
                aut = self.textes_disputes[i+1].auteur
                num = self.textes_disputes[i+1].numero
            i+=1
        if nb_vrai>nb_faux:
            print("L'oeuvre " + aut + str(num) + " est dans la catégorie " + aut_base + " : " + str(nb_vrai) + " textes acceptés contre contre " + str(nb_faux) + " rejetés.")
        else:
            print("L'oeuvre " + aut + str(num) + " n'est pas dans la catégorie " + aut_base + " : " + str(nb_vrai) + " textes acceptés contre " + str(nb_faux) + " rejetés.")
        self.oeuvres.append((aut,num))
        self.vrais.append(nb_vrai)
        self.faux.append(nb_faux)
        self.tracer()
        print("")
        print("Graphique enregistré dans le dossier source")
        
    def tracer(self):
        n_groups = len(self.oeuvres)
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.4
        error_config = {'ecolor': '0.3'}
        rects1 = plt.bar(index, self.vrais, bar_width,
                        alpha=opacity,
                        color='g',
                        label='Attributions dans {}'.format(self.cat_base))
        rects2 = plt.bar(index + bar_width, self.faux, bar_width,
                        alpha=opacity,
                        color='r',
                        label='Rejets')
        plt.xlabel('Oeuvres')
        plt.ylabel('Nombre de textes')
        plt.title('Vérification par Average Similarity')
        noms_oeuvres = [self.oeuvres[i][0] + str(self.oeuvres[i][1]) for i in range(len(self.oeuvres))]
        plt.xticks(index + bar_width / 2, noms_oeuvres)
        plt.legend(loc="best")
        #plt.tight_layout()
        plt.savefig("similarity_graph"+ str(int(time())) + ".png")