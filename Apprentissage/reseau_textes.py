# -*- coding: utf-8 -*-
import numpy as np
import classes
from Representation.fenetre import FenetreAffichage
from Interpretation.importance_composantes import importance, gain_information

class reseau_neurones(classes.Classifieur):
    def __init__(self):
        self.setApprentissage = []  # /!\ différent de training_set (pas le même format)
        self.clusters = []
        self.liste_textes = None
        self.precision = None
        self.clusters = None
        self.p = self.p_ref = None
        self.eval_set = self.training_set = None
        self.Wmin = self.bmin = None

    # Crée les poids (W), les biais (b), et les fonctions d'activation de chaque couche (f)
    # Le format d'entrée de la structure est par exemple, pour un réseau à 5 entrées,
    # 2 couches de neurones dont une de 3 neurones et une de 10 neurones : [5,4,3]
    def initialise_reseau(self, structure_reseau):
        W = [0]*(len(structure_reseau)-1)  # Tableau des matrices de poids
        b = [0]*(len(structure_reseau)-1)  # Tableau des seuils/biais
        f = [0]*(len(structure_reseau)-1)  # Tableau des fonctions d'activation
        for k in range(0, len(structure_reseau)-1):  # On prend des valeurs aléatoires uniformément distribuées dans [-1;1]
            W[k] = 2*np.random.rand(structure_reseau[k+1],structure_reseau[k])-1 #idem
            b[k] = 2*np.random.rand(structure_reseau[k+1],1)-1
            f[k] = self.logsig  # Par défaut on initialise toutes les fonctions d'activation à sigmoïde
        return W,b,f

    # Renvoie les sorties de chaque couche du réseau pour une entrée donnée sous forme de vecteur colonne
    def propage_entree(self, entree, W, b, f):
        a = []  # Sortie des couches
        n = []  # Sortie des couches avant activation (ie. application de f[k])
        a.append(entree)
        for k in range(len(W)):
            n.append(np.dot(W[k], a[len(a)-1]) - b[k])
            a.append(f[k](n[k]))
        return n,a

    # FONCTIONS DE SEUILLAGE : varient en fonction des neurones, ici pour le moment c'est logsig qui est utilisée
    # Ces fonctions prennent un tableau et s'appliquent à chacun de ses éléments.
    def hardlim(self, x):
        res = []
        for y in x.transpose().tolist()[0]:
            if y > 0:
                res.append(1)
            else:
                res.append(0)
        res = np.array(res).reshape(x.shape)
        return res

    def logsig(self, x):
        res = []
        for y in x.transpose().tolist()[0]:
            res.append(1/(1+np.exp(-y)))
        res = np.array(res).reshape(x.shape)
        return res

    def satlin(self, x):
        res = []
        for y in x.transpose().tolist()[0]:
            if y > -0.5:
                if y < 0.5:
                    res.append(y)
                else:
                    res.append(y)
            else:
                res.append(y)
        res = np.array(res).reshape(x.shape)
        return res

    def derivee_satlin(self, x):
        res = []
        for y in x.transpose().tolist()[0]:
            if y > -0.5:
                if y < 0.5:
                    res.append(1)
                else:
                    res.append(1)
            else:
                res.append(1)
        res = np.array(res).reshape(x.shape)
        return res

    def derive(self, f):
        if f == self.hardlim:
            return (lambda x: 0)
        if f == self.logsig:
            return (lambda x: np.exp(-x)/np.power(1+np.exp(-x), 2))
        if f == self.satlin:
            return self.derivee_satlin
        return lambda x: 0
    # Fin de la partie fonctions d'activation

    # A partir des sorties de chaque couche du réseau (a,n) (données par propage_entrees),
    # on calcule les sensibilités (s) de chaque neurone (dérivée de l'erreur quadratique) par rétropropagation
    def retropropage_sensibilites(self, W, f, a, n, d): #d = sortie théorique
        s = []  # Sensibilité de l'erreur de chaque couche par rapport à n
        k = len(W)-1
        sM = -2*np.dot(np.diag(np.transpose(self.derive(f[len(W)-1])(n[len(W)-1])).tolist()[0]), d-a[len(W)])
        s.append(sM)
        k -= 1
        while k >= 0:
            j = np.dot(np.diag(np.transpose(self.derive(f[k])(n[k])).tolist()[0]), np.transpose(W[k+1])) #Un peu sale parce qu'il faut transformer n de vecteur colonne en liste python
            s0 = np.dot(j, s[len(s)-1])
            s.append(s0)
            k -= 1
        s.reverse()
        return s

    # Met à jour les poids et les biais en fonction des sensibilités (s), des sorties des neurones (a),
    # du coefficient d'apprentissage (qui détermine la taille du pas qu'on fait vers la direction donnée par le gradient),
    # l'inertie (momentum), qui détermine la mesure dans laquelle on continue à aller dans la direction de l'étape précédente
    # (pour ne pas prendre de virages trop brusques, et pour sortie des minimas locaux)
    # Les tableaux oldDeltaW et oldDeltaB servent à stocker ces directions pour l'étape suivante
    def nouveaux_poids_et_biais(self, W, b, a, s, coeffApprentissage, oldDeltaW = 0, oldDeltaB = 0, momentum = 0):
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
    # Calcule la mise à jour des poids et des biais et les renvoie
    def apprend(self, W, b, f, coeffApprentissage, e, oldDeltaW = 0, oldDeltaB = 0, momentum = 0): #e = [entrée, sortie]
        n, a = self.propage_entree(e[0], W, b, f) #L'entrée est un vecteur colonne
        s = self.retropropage_sensibilites(W, f, a, n, e[1]) #s est un vecteur colonne
        return self.nouveaux_poids_et_biais(W, b, a, s, coeffApprentissage, oldDeltaW, oldDeltaB, momentum)

    # Calcule la sortie du réseau pour une entrée donnée sous forme de vecteur colonne
    def sortie(self, entree):
        n,a = self.propage_entree(entree, self.W, self.b, self.f)
        return a[len(a)-1]

    # Transforme une liste python en vecteur colonne
    def col(self, l):
        return [[x] for x in l]

    # Renvoie la norme de v
    def norme(self, v):
        res = 0
        for x in v:
            res+= np.power(x,2)
        return np.sqrt(res)

    # Calcule l'erreur du réseau sur une valeur
    def erreur_quadratique_valeur(self, k):
        s_concret = self.sortie(self.setApprentissage[k][0])
        s_theorique = self.setApprentissage[k][1]
        return np.power(self.norme([s_theorique[i][0]-s_concret[i][0] for i in range(len(s_concret))]),2)

    # Calcule l'erreur totale du réseau sur l'ensemble donné en argument
    def erreur_quadratique_ensemble(self, st):
        e = 0
        for k in range(len(st)):
            e += self.erreur_quadratique_valeur(k)
        return e

    def composante_dominante(self, vecteur):
        i = 0
        for j in range(len(vecteur)):
            if(vecteur[j]>vecteur[i]):
                i = j
        return i

    def classifier(self, training_set, eval_set):
        #On constitue la liste des auteurs
        self.auteurs = []
        self.auteurs_inverses = {}
        for texte in training_set:
            if texte.auteur not in self.auteurs:
                self.auteurs.append(texte.auteur)
                self.auteurs_inverses[texte.auteur] = len(self.auteurs)-1


        # [nombre_entrees, taille des couches]
        structure_reseau = np.array([len(eval_set[0].vecteur), 10, len(self.auteurs)])  # Le premier terme est la dimension de l'espace de départ

        self.W, self.b, self.f = self.initialise_reseau(structure_reseau)
        coeffApprentissage = 0.1
        momentum = 0.  # Pas de momentum (le réseau de textes converge sans pour le moment)

        # On initialise ces variables (qui servent dans la mise à jour des poids
        oldDeltaW = [np.dot(0, w) for w in self.W]
        oldDeltaB = [np.dot(0, b0) for b0 in self.b]

        # Plusieurs variables qui servent dans la boucle :
        renormage = False  # Si activé, conserve la norme des poids à  (mais fait perdre en précision)
        verbose = False  # Si activé, affiche les poids dans la console
        erreur = 10  # On initialise l'erreur (pour ne pas s'arrêter au début de la boucle)
        cpt = 0  # Compteur d'étapes
        self.Wmin, self.bmin = self.W, self.b  # Valeurs des poids et des biais pour lesquelles le réseau a atteint sa meilleure performance
        erreur_min = 10  # On initialise l'erreur minimale à 10, elle sera mise à jour dès qu'on tombera sur plus petit
        borne_arret = 0.01  # si erreur<borneArret, la boucle s'arrête
        etape_max = 2000

        self.setApprentissage = []
        for i in range(len(training_set)):
            vecteur_sortie = [0]*len(self.auteurs)
            vecteur_sortie[self.auteurs_inverses[training_set[i].auteur]] = 1
            self.setApprentissage.append([self.col(training_set[i].vecteur), self.col(vecteur_sortie)])

        print("Classification par réseau de neurones")
        print("Début de l'apprentissage (borne d'arrêt : erreur = {0} ou étape = {1})".format(borne_arret, etape_max))

        while erreur > borne_arret and cpt < etape_max:  # Tant que l'erreur quadratique totale est trop élevée, on continue
            cpt += 1
            cpt2 = 0
            for i in range(len(self.setApprentissage)-1):  # On parcourt l'ensemble d'apprentissage
                cpt2 += 1
                if cpt2 == 1 and renormage:  # Si activé, régule les normes des poids à 1 (mais perte de précision)
                    cpt2 = 0
                    # On renorme les poids
                    print("Normage des poids à 1")
                    for k in range(len(self.W)):
                        for j in range(len(self.W[k])):
                            self.W[k][j] = self.W[k][j]/self.norme(self.W[k][j])
                    if verbose:
                        print(self.W)
                # On fait apprendre au réseau l'élément de l'ensemble d'apprentissage
                oldDeltaW, oldDeltaB = self.apprend(self.W, self.b, self.f, coeffApprentissage, self.setApprentissage[i], oldDeltaW, oldDeltaB, momentum)
            erreur = self.erreur_quadratique_ensemble(self.setApprentissage)
            if erreur<erreur_min:  # Si on bat notre record, on met à jour Wmin et bmin
                erreur_min = erreur
                self.Wmin, self.bmin = self.W, self.b
            if cpt%100 == 0:  # Changer 100 en n>1 pour régler la fréquence d'affichage
                print(erreur, cpt.__str__()+"/"+etape_max.__str__())
        print("Apprentissage terminé en {0} étapes".format(cpt))
        self.W, self.b = self.Wmin, self.bmin

        # Création de self.clusters, p et p_ref : ne concerne que eval_set
        self.p = np.zeros([len(eval_set), len(self.auteurs)])
        self.p_ref = np.zeros([len(eval_set), len(self.auteurs)])
        self.clusters = [[] for i in range(len(self.auteurs))]
        for i in range(len(eval_set)):
            s = self.sortie(self.col(eval_set[i].vecteur))
            self.p[i] = [x[0] for x in s]
            self.p_ref[i] = [0]*len(self.auteurs)
            self.p_ref[i][self.auteurs_inverses[eval_set[i].auteur]] = 1
            comp = self.composante_dominante(s)
            self.clusters[comp].append(eval_set[i])

        # Création de self.précision : ne concerne que training_set
        self.precision = 0
        for i in range(len(training_set)):
            s = self.sortie(self.col(training_set[i].vecteur))
            comp = self.composante_dominante(s)
            if(comp == self.auteurs_inverses[training_set[i].auteur]):
                self.precision += 1.
        self.precision /= len(training_set)

    def poids_composantes(self, clusters=None):
        tab = [0]*len(self.W[0][0])
        for i in range(len(self.W[0])):
            for j in range(len(self.W[0][i])):
                tab[j] += abs(self.W[0][i][j])
        return tab
