from classes import Texte,Analyseur,FonctionAnalyse
from Carac.carac_gramm import Markov_Gram
from Utilitaires.stats import *
from Utilitaires.lettres import *
from Utilitaires.product import *
import nltk
import numpy as np


class Complexite_Grammaticale(FonctionAnalyse):

    def __init__(self, langue, saut):
        self.langue = langue
        self.saut = saut
        nom = "Complexité grammaticale ordre {}".format(self.saut)
        composantes = ["Ecart au style canonique Linfini ordre {} ".format(self.saut),"Ecart au style canonique Frobenius ordre {} ".format(self.saut)]
        super(Complexite_Grammaticale,self).__init__(nom,composantes)

    def analyser(self, liste_textes):

        markov_gram = Markov_Gram(self.langue,self.saut)

        N = len(markov_gram.natures)
        M = np.zeros((N,N))

        P = []

        for t in liste_textes:
            p = markov_gram.estimer(t)
            P.append(markov_gram.estimer(t))
            M+=p

        M = M/ (len(liste_textes))

        for i in range(len(liste_textes)):
            t = liste_textes[i]
            p = P[i]
            v = [np.max(np.abs(p-M)),np.trace((p-M).dot((p-M).transpose()))]
            t.vecteur += v


class Complexite_Vocabulaire(FonctionAnalyse):

    def __init__(self):

        nom = "Complexité du vocabulaire"
        composantes = ["vocabulaire / mots", "sqrt(vocabulaire)/ ots", "log(vocabulaire)/log(mots)"]
        super(Complexite_Vocabulaire,self).__init__(nom,composantes)

    def analyser(self, liste_textes):

        n = 200
        for t in liste_textes:
            N = len(t.racines)
            V = len(set(t.racines))
            fdist = nltk.FreqDist(t.racines)
            p = [x[1] for x in fdist.most_common(n)]
            v = [V / N, np.sqrt(V) / N, np.log(V) / np.log(N)]
            t.vecteur+= v

