import numpy as np

lettres = ["a", "z", "e", "r", "t", "y", "u", "i", "o", "p", "q", "s", "d", "f", "g", "h", "j", "k", "l", "m", "w",
           "x", "c", "v", "b", "n"]


def representant_canonique(lettre,langue):
    if lettre in lettres:
        return lettre
    else:
        correspondance_lettres_speciales =[]
        lettres_speciales = []
        if langue == "fr":
            lettres_speciales = ["à", "â", "é", "è", "ê", "ë", "î", "ï", "ô", "ù", "û", "ü"]
            correspondance_lettres_speciales = ["a", "a", "e", "e", "e", "e", "i", "i", "o", "u", "u", "u"]
        elif langue == "en":
            lettres_speciales = []
            correspondance_lettres_speciales = []
        elif langue == "de":
            lettres_speciales = ["ä", "ö", "ü"]
            correspondance_lettres_speciales = ["a", "o", "u"]
        elif langue == "es":
            lettres_speciales = ["ñ", "á", "é", "í", "ó", "ú"]
            correspondance_lettres_speciales = ["n", "a", "e", "i", "o", "u"]
        if lettre in lettres_speciales:
            return correspondance_lettres_speciales[lettres_speciales.index(lettre)]
        else:
            return "-"