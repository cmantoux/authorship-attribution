from classes import Texte,Analyseur,FonctionAnalyse
from Utilitaires.stats import *
import numpy as np

class Freq_Gram(FonctionAnalyse):

    def __init__(self, langue):
        self.natures = []
        self.langue = langue
        if self.langue == "fr":
            self.natures = ["ABR", "ADJ", "ADV", "DET:ART", "DET:POS", "INT", "KON", "NAM", "NOM", "NUM", "PRO", "PRO:DEM",
                       "PRO:IND",
                       "PRO:PER", "PRO:POS", "PRO:REL", "PRP", "PRP:det", "PUN", "PUN:cit", "SENT", "SYM", "VER:cond",
                       "VER:futu",
                       "VER:impe", "VER:impf", "VER:infi", "VER:pper", "VER:ppre", "VER:pres", "VER:simp", "VER:subi",
                       "VER:subp"]
        elif self.langue == "en":
            self.natures = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'IN/that', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NP',
                       'NPS', 'PDT', 'POS', 'PP', 'PP$', 'RB', 'RBR', 'RBS', 'RP', 'SENT', 'SYM TO', 'UH', 'VB', 'VBD',
                       'VBG', 'VBN', 'VBZ', 'VBP', 'VD', 'VDD', 'VDG', 'VDN', 'VDZ', 'VDP', 'VH', 'VHD VHG', 'VHN',
                       'VHZ',
                       'VHP', 'VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ', 'WDT', 'WP', 'WP$', 'WRB']
        elif self.langue == "zh":
            self.natures = ["a", "ad", "ag", "an", "b", "bg", "c", "cg", "d", "dg", "e", "ew", "f", "fg", "g", "h", "i",
                       "j", "k", "l", "m", "mg", "n", "ng", "nr", "ns", "nt", "nx", "nz", "o", "p", "pg", "q", "qg",
                       "r", "rg", "s", "t", "tg", "u", "v", "vd", "vg", "vn", "w", "x", "y", "yg", "z", "zg"]


        nom = "Frequences grammaticales"
        composantes = []
        for n in self.natures:
            composantes.append("Fréquence de la catégorie grammaticale {}".format(n))
        super(Freq_Gram,self).__init__(nom,composantes)

    def analyser(self, liste_textes):

        for t in liste_textes:
            v = freqs(t.POS, self.natures)
            t.vecteur+= v

class Markov_Gram(FonctionAnalyse):

    def __init__(self, langue, saut):
        self.natures = []
        self.langue = langue
        self.saut = saut
        if self.langue == "fr":
            self.natures = ["ABR", "ADJ", "ADV", "DET:ART", "DET:POS", "INT", "KON", "NAM", "NOM", "NUM", "PRO", "PRO:DEM",
                       "PRO:IND",
                       "PRO:PER", "PRO:POS", "PRO:REL", "PRP", "PRP:det", "PUN", "PUN:cit", "SENT", "SYM", "VER:cond",
                       "VER:futu",
                       "VER:impe", "VER:impf", "VER:infi", "VER:pper", "VER:ppre", "VER:pres", "VER:simp", "VER:subi",
                       "VER:subp"]
        elif self.langue == "en":
            self.natures = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'IN/that', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NP',
                       'NPS', 'PDT', 'POS', 'PP', 'PP$', 'RB', 'RBR', 'RBS', 'RP', 'SENT', 'SYM TO', 'UH', 'VB', 'VBD',
                       'VBG', 'VBN', 'VBZ', 'VBP', 'VD', 'VDD', 'VDG', 'VDN', 'VDZ', 'VDP', 'VH', 'VHD VHG', 'VHN',
                       'VHZ',
                       'VHP', 'VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ', 'WDT', 'WP', 'WP$', 'WRB']
        elif self.langue == "zh":
            self.natures = ["a", "ad", "ag", "an", "b", "bg", "c", "cg", "d", "dg", "e", "ew", "f", "fg", "g", "h", "i",
                       "j", "k", "l", "m", "mg", "n", "ng", "nr", "ns", "nt", "nx", "nz", "o", "p", "pg", "q", "qg",
                       "r", "rg", "s", "t", "tg", "u", "v", "vd", "vg", "vn", "w", "x", "y", "yg", "z", "zg"]


        nom = "{}-transitions grammaticales".format(self.saut)
        composantes = []
        for i in self.natures:
            for j in self.natures:
                composantes.append("Fréquence {}-transition {} -> {}".format(saut,i,j))
        super(Markov_Gram,self).__init__(nom,composantes)

    def analyser(self, liste_textes):

        for t in liste_textes:
            v = markov(self.saut,t.POS, self.natures)
            t.vecteur += v

    def estimer(self,texte):
        v =  markov(self.saut,texte.POS, self.natures)
        N = len(self.natures)
        m = np.zeros((N,N))
        for idx in range(len(v)):
            i = idx // N
            j = idx % N
            m[i,j] = v[idx]
        return m