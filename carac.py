import nltk
import math
from classes import emplacement_dossier_groupe

# Fonctions basées sur les caractères

def freq_lettres(texte):
    texte1 = texte.texte_brut.lower()
    lettres = ["a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "q", "s", "d", "f", "g", "h", "j", "k", "l", "m", "w",
               "x", "c", "v", "b", "n"]
    if texte.langue == "fr":
        lettres_speciales = ["à", "â", "é", "è", "ê", "ë", "î", "ï", "ô", "ù", "û", "ü"]
        correspondance_lettres_speciales = ["a", "a", "e", "e", "e", "e", "i", "i", "o", "u", "u", "u"]
    elif texte.langue == "en":
        lettres_speciales = []
        correspondance_lettres_speciales = []
    elif texte.langue == "de":
        lettres_speciales = ["ä", "ö", "ü"]
        correspondance_lettres_speciales = ["a", "o", "u"]
    elif texte.langue == "es":
        lettres_speciales = ["ñ", "á", "é", "í", "ó", "ú"]
        correspondance_lettres_speciales = ["n", "a", "e", "i", "o", "u"]
    l = len(texte1)
    n = len(lettres)
    frequences = [0 for k in range(n)]
    for k in range(l):
        x = texte1[k]
        if x in lettres:
            i = lettres.index(x)
            frequences[i] += 1
        elif x in lettres_speciales:
            i = lettres.index(correspondance_lettres_speciales[lettres_speciales.index(x)])
            frequences[i] += 1
    S = sum(frequences)
    if S == 0:
        raise ValueError("Ca va pas du tout")
    frequences = [f / S for f in frequences]
    return frequences, ["Fréquence de la lettre {}".format(lettres[k]) for k in range(len(lettres))]


def freq_ponct(texte):
    signes = [".", ",", ":", "!", "?", "-"]
    dico_freq = {}
    for s in signes:
        dico_freq[s] = 0
    for m in texte.mots:
        if m in signes:
            dico_freq[m] += 1
    frequences = dico_freq.values()
    S = len(texte.mots)
    if S == 0:
        A = [0] * len(frequences)
    else:
        A = [f / S for f in frequences]
    return A, ["Fréquence relative du signe de ponctuation {}".format(signes[k]) for k in
               range(len(signes))]


# Analyse grammaticale et POS

def freq_gram(texte):
    pos = texte.POS
    if texte.langue == "fr":
        natures = ["ADJ", "ADV", "DET:ART", "DET:POS", "KON", "NAM", "NOM", "PRO", "PRO:DEM", "PRO:IND", "PRO:PER",
                   "PRO:POS", "PRO:REL", "PRP", "PRP:det", "PUN", "SENT", "VER:pres", "VER:ppre", "VER:pper",
                   "VER:simple", "VER:subp", "VER:subi", "VER:impf", "VER:cond", "VER:futu"]
    elif texte.langue == "en":
        natures = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'IN/that', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NP',
                   'NPS', 'PDT', 'POS', 'PP', 'PP$', 'RB', 'RBR', 'RBS', 'RP', 'SENT', 'SYM TO', 'UH', 'VB', 'VBD',
                   'VBG', 'VBN', 'VBZ', 'VBP', 'VD', 'VDD', 'VDG', 'VDN', 'VDZ', 'VDP', 'VH', 'VHD VHG', 'VHN', 'VHZ',
                   'VHP', 'VV', 'VVD', 'VVG', 'VVN', 'VVP', 'VVZ', 'WDT', 'WP', 'WP$', 'WRB']
    dico_freq = {}
    for p in natures:
        dico_freq[p] = 0
    for p in pos:
        if p in natures:
            dico_freq[p] += 1
    frequences = dico_freq.values()
    S = len(pos)
    if S==0:
        raise ValueError("Ca va pas du tout")
    return [f / S for f in frequences], ["Fréquence relative de la catégorie grammaticale {}".format(natures[k]) for k
                                         in range(len(frequences))]


# Fonctions basées sur les mots

def plus_courants(texte, n=10):
    nltk_racines = nltk.Text(texte.racines)
    L = len(nltk_racines)
    fdist = nltk.FreqDist(nltk_racines)
    M = fdist.most_common(n)
    return [m[1] / L for m in M], ["Fréquence du {}-ème mot le plus courant".format(k+1) for k in range(len(M))]


def dif_plus_courants(texte, n=10):
    P = plus_courants(texte, n)[0]
    D = [(P[k] - P[k + 1]) / P[k] for k in range(n - 1)]
    return D, ["Chute de fréquence entre le {}-ème token le plus courant et le {}+1-ème".format(k, k) for k in
               range(1, n)]


def freq_stopwords(texte):
    with open(
            emplacement_dossier_groupe + "Bibliographie et ressources/Littérature/Stopwords/stopwords_" + texte.langue + ".txt",
            "r") as fichier:
        stopwords = fichier.read()
    liste_stopwords = stopwords.split()
    fdist = nltk.FreqDist([m.lower() for m in texte.mots])
    frequences = [fdist.freq(sw) for sw in liste_stopwords]
    S = sum(frequences)
    return [f/S for f in frequences], ["Fréquence du stopword {}".format(liste_stopwords[k]) for k in range(len(liste_stopwords))]


# Fonctions naives


def richesse_voc(texte):
    n = 200
    N = len(texte.racines)
    V = len(set(texte.racines))
    fdist = nltk.FreqDist(texte.racines)
    p = [x[1] for x in fdist.most_common(n)]
    A = [V/N, math.sqrt(V)/N, math.log(V)/math.log(N)]
    return A, ["Richesse du vocabulaire (divers indicateurs)"]*len(A)

def longueur_mots(texte):
    longueurs = [0 for k in range(20)]
    for m in [texte.mots[k] for k in texte.mots if texte.mot[k] not in string.punctuation]:
        longueurs[len(m)] +=1
    S = sum(longueurs)
    return [l/S for l in longueurs], ["Fréquence des mots de longueur {}" for k in range(len(longueurs))]