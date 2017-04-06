from carac_gramm import *
from carac_lettres import *
from carac_ponct import *
from carac_complexite import *
from carac_stopwords import *
from classes import Oeuvre,Texte

a1 = Freq_Gram(langue = "fr")
a2= Markov_Gram(langue = "fr",saut = 1)
a3 = Freq_Ngrammes(langue = "fr",n=2)
a4 = Markov_Lettres(langue = "fr")
a5 = Freq_Ponct(langue = "fr")


aGram = Analyseur("Grammaire",[a1,a2])
aLettres= Analyseur("Lettres",[a3,a4])
aPonct = Analyseur("Ponctuation",[a5])

A = Analyseur("Tout",[aGram,aLettres,aPonct])
A.numeroter()

A.analyser(liste_textes)
print(A.noms_composantes())
for t in liste_textes:
    print(t.vecteur)