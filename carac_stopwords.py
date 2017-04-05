from classes import Texte,Analyseur,FonctionAnalyse
from Utilitaires.stats import *
from Utilitaires.stopwords import stopwords_en, stopwords_fr, stopwords_zh

class Freq_Stopwords(FonctionAnalyse):

    def __init__(self, langue):
        self.langue = langue
        stopwords = []
        if langue == "en":
            stopwords = stopwords_en()
        elif langue == "fr":
            stopwords = stopwords_fr()
        elif langue == "zh":
            stopwords = stopwords_zh()

        self.stopwords = stopwords

        nom = "Frequences des stopwords"
        composantes = []
        for x in self.stopwords:
            composantes.append("Fréquence de {}".format(x))
        super(Freq_Stopwords,self).__init__(nom,composantes)

    def analyser(self, liste_textes):

        for t in liste_textes:
            v = freqs(t.racines, self.stopwords)
            t.vecteur += v
