from classes import Texte,Analyseur,FonctionAnalyse
from Utilitaires.stats import *
from Utilitaires.lettres import *
from Utilitaires.product import *

class Freq_Ponct(FonctionAnalyse):

    def __init__(self, langue):
        self.langue = langue
        self.signes =     signes = [".", ",",";", ":", "?", "!", "(", ")", "-", "'"]
        if self.langue == "zh":
            self.signes = ["。", "，", "：", "！", "？", "“", "”", "；"]


        nom = "Frequences de la ponctuation"
        composantes = []
        for x in self.signes:
            composantes.append("Fréquence de {}".format(x))
        super(Freq_Ponct,self).__init__(nom,composantes)

    def analyser(self, liste_textes):

        for t in liste_textes:
            X = t.texte_brut.lower()
            X = [representant_canonique(x,self.langue) for x in X]
            v = freqs(t.texte_brut, self.signes)
            t.vecteur += v

class Longueur_Phrases(FonctionAnalyse):

    def __init__(self):

        composantes = ["Moyenne log longueur phrase", "Ecart-type log longueur phrase", "Assymétrie log longueur phrase",
         "Kurtosis log longueur phrase", "Moyenne longueur phrase","Ecart-type longueur phrase","Minimum longueur phrase",
                       "Maximum longueur phrase","Q1 longueur phrase","Médiane longueur phrase","Q3 longueur phrase"]

        super(Longueur_Phrases, self).__init__("Longueur des phrases", composantes)

    def analyser(self,liste_textes):
        for t in liste_textes:
            v =  log_serie_temporelle(np.array(t.racines), ".") + serie_temporelle(np.array(t.racines),".")
            t.vecteur += v


