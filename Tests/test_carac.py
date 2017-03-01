from carac_gramm import *
from carac_lettres import *
from carac_ponct import *
from carac_complexite import *
from carac_stopwords import *
from classes import Oeuvre,Texte

# a = Freq_Gram(langue = "fr")
# a = Markov_Gram(langue = "fr",saut = 1)
# a = Freq_Ngrammes(langue = "fr",n=2)
# a = Markov_Lettres(langue = "fr")
# a = Freq_Ponct(langue = "fr")
a1 = Longueur_Phrases()
a2 = Complexite_Grammaticale(langue = "fr", saut= 1)
a3 = Freq_Stopwords(langue = "fr")

a = Analyseur([a1,a2,a3])

a.analyser(liste_textes)
print(a.noms_composantes())
for t in liste_textes:
    print(t.vecteur)