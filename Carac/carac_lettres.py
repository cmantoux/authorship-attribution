from classes import Texte,Analyseur,FonctionAnalyse
from Utilitaires.stats import *
from Utilitaires.lettres import *
from Utilitaires.product import *

class Freq_Ngrammes(FonctionAnalyse):

    def __init__(self, langue, n):
        self.natures = []
        self.langue = langue
        self.n = n
        self.lettres = ["a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "q", "s", "d", "f", "g", "h", "j", "k", "l", "m", "w",
           "x", "c", "v", "b", "n"]


        nom = "Frequences des {}-grammes".format(self.n)
        composantes = []
        for l in product([self.lettres]*self.n):
            composantes.append("Fréquence du {}-gramme {}".format(self.n,"".join(l)))
        super(Freq_Ngrammes,self).__init__(nom,composantes)

    def analyser(self, liste_textes):

        for t in liste_textes:
            X = t.texte_brut.lower()
            X = [representant_canonique(x,self.langue) for x in X]
            real_X = []
            for k in range(0, len(X) - self.n, self.n):
                real_X.append("".join(X[k:k + self.n]))

            grammes = ["".join(l) for l in product([self.lettres]*self.n)]
            v = freqs(real_X, grammes)
            t.vecteur += v

class Markov_Lettres(FonctionAnalyse):

    def __init__(self, langue):
        self.langue = langue
        self.lettres = ["a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "q", "s", "d", "f", "g", "h", "j", "k", "l", "m", "w",
           "x", "c", "v", "b", "n"]

        nom = "Transitions entre lettres "
        composantes = []
        for i in lettres:
            for j in lettres:
                composantes.append("Transitions {} -> {} ".format(i,j))
        super(Markov_Lettres,self).__init__(nom,composantes)

    def analyser(self, liste_textes):

        for t in liste_textes:
            X = t.texte_brut.lower()
            X = [representant_canonique(x, self.langue) for x in X]

            v = markov(1,X,self.lettres)
            t.vecteur += v

