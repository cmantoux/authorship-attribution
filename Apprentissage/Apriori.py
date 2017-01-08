import numpy as np
from classes import Classifieur

from Utilitaires.pca import pca


def Apprentissage(vecteurs, auteurs, seuil=0.5, pas=0.1, composantes=50):
    v = len(vecteurs) #nombre de vecteurs à traiter
    for i in range(v):
        vecteurs[i] = vecteurs[i].tolist()
    m = len(vecteurs[0]) #nombre de composantes d'un vecteur
    if(m>composantes):
        m = composantes #nombre de composantes qui seront effectivement traitées
    Noms = []
    Classes = []
    for i in range(len(auteurs)): #boucle visant à créer un tableau Classes tel que Classes[i] contienne tous les vecteurs de l'auteur Noms[i]
        if not(auteurs[i] in Noms):
            Noms += [auteurs[i]]
            Classes += [[vecteurs[i]]]
        else:
            l = Noms.index(auteurs[i])
            Classes[l] += [vecteurs[i]]
    c = len(Classes) #Nombre de classes donc d'auteurs différents
    Result = [] #Tableau des résultats qui sera renvoyé à la fin
    for i in range(c): #Boucle sur toutes les classes
        Fk = []
        k = 1 #1e étape de l'algo
        for j in range(m): #on parcourt les m 1e composantes des vecteurs de la classe i
            min = Classes[i][0][j]
            max = Classes[i][0][j]
            for l in range(len(Classes[i])): #boucle visant un déterminer la plus petite et la plus grande composante de la classe i
                element = Classes[i][l][j]
                if(element<min):
                    min = element
                if(element>max):
                    max = element
            p = min
            Pas = (max-min)*pas
            while(p<max-Pas):
                f1 = []
                f2 = []
                for t in range(v): 
                    element = vecteurs[t]
                    if(element[j]>=p and element[j]<=p+Pas):
                        f2 += [element] #on regroupe dans f2 les elements dont la j-ème composante est comprise entre p et p+Pas
                        if(element in Classes[i]):
                            f1 += [element] #on regroupe dans f1 les elements de la classe i dont la j-ème composante est comprise entre p et p+Pas
                if(len(f2) != 0 and len(f1)/len(f2) >= seuil): #Si f1 est un sous-ensemble fréquent on le stocke dans F1 accompagné de f2 et d'une liste décrivant le critère d'appartenance à f1 (composante étudiée, bornes de l'intervalle de valeurs)
                    Fk += [[f1, f2, [j, p, p+Pas]]]
                p += Pas
        k += 1
        while(True):
            Ck = []
            for f in range(len(Fk)):
                Ref = Fk[f]
                for j in range(f+1, len(Fk)):
                    L = Fk[j]
                    o = 0
                    for l in range(len(L)):
                        if(not(L[l] in Ref)):
                            o+=1
                            if(o>1):
                                break
                            else:
                                element = L[l]
                    if(o==1):
                        Ck += [Ref + [element]]
            for f in range(len(Ck)):
                f1 = []
                f2 = []
                for t in range(len(vecteurs)):
                    test = True
                    for j in range(len(Ck[f])):
                        if(not(vecteurs[t] in Ck[f][1])):
                            test = False
                            break
                    if(test):
                        f2 += [vecteurs[t]]
                        if(vecteurs[t] in Classes[i]):
                            f1 += [vecteurs[t]]
                if(len(f2)== 0 or len(f1)/len(f2) < seuil):
                    Ck.remove(Ck[f])
            if(len(Ck)==0 or k>15):
                break
            else:
                Fk = list(Ck)
                k +=1
        F_final = []
        for f in range(len(Fk)):
            F_final += [Fk[f][2]]
        Result += [F_final]
    return Noms, Result
    
def Test(Inconnus, Result):
    n = len(Result)
    k = len(Inconnus)
    Probabilites = np.zeros((k,n))
    for i in range(k):
        I = Inconnus[i]
        p = 0
        for r in range(n):
            F = Result[r]
            for f in range(len(F)):
                j = F[f][0]
                p0 = F[f][1]
                p1 = F[f][2]
                if(I[j]>=p0 and I[j]<p1):
                    p+=1
                    Probabilites[i][r] = 1
                    break
        if(p!=0):
            Probabilites[i] = Probabilites[i]/p
        if(p==0):
            for r in range(n):
                Probabilites[i][r] = 1/n
    return Probabilites
    
        
class Apriori(Classifieur):
    
    def __init__(self):
        print("Création du classifieur Apriori")
        self.eval_set = None
        self.training_set = None
        self.p = None
        self.p_ref = None
        self.precision = None
        self.indecis = None
        pass
    
    def classifier(self, training_set, eval_set):
        self.eval_set = eval_set
        self.training_set = training_set
        vecteurs_training = [t.vecteur for t in training_set]
        auteurs_training = [t.auteur for t in training_set]
        t = len(vecteurs_training)
        vecteurs_eval = [t.vecteur for t in eval_set]
        auteurs_eval = [t.auteur for t in eval_set]
        vecteurs = vecteurs_training + vecteurs_eval
        vecteurs = pca(vecteurs)
        vecteurs_training = vecteurs[0:t]
        vecteurs_eval = vecteurs[t:len(vecteurs)]
        Intermediaires = Apprentissage(vecteurs_training, auteurs_training)
        Probabilite = Test(vecteurs_eval, Intermediaires[1])
        self.p = Probabilite
        self.auteurs = Intermediaires[0]
        k = np.shape(Probabilite)[1]
        m = np.shape(Probabilite)[0]
        Reference = np.zeros((m,k))
        vrai = 0
        faux = 0
        indecis = 0
        for i in range(m):
            max = Probabilite[i][0]
            if(max == 1/k):
                indecis += 1
            categorie = 0
            for j in range(k):
                if(Probabilite[i][j]>max):
                    max = Probabilite[i][j]
                    categorie = j
            ref = Intermediaires[0].index(auteurs_eval[i])
            if(ref==categorie):
                vrai += 1
            else:
                faux += 1
            Reference[i][ref] = 1
        self.p_ref = Reference
        self.precision = vrai/(vrai+faux) * 100
        self.indecis = indecis/(vrai+faux) * 100
        
        
    def afficher(self):
        print("Résultats du classificateur Apriori sur le corpus étudié :")
        print("On obtient une précision de : "+str(self.precision)+"%. Parmi les textes qui n'ont pas été attribués correctement, "+str(self.indecis)+"% des textes n'ont pas été attribués à un auteur donné.")