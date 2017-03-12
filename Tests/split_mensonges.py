#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.append("/Users/Guillaume/Documents/Informatique/psc")
from classes import *


with open("/Users/Guillaume/Google Drive/Cours X/PSC/Groupe PSC/Corpus/Francais/Fichiers txt/mensonge0.txt","rb") as fichier:
    T = fichier.read().decode("utf-8")
    TS = T.split("\n")

for k in range(len(TS)):
    if k%2==0:
        t = TS[k].encode("utf-8")
        with open("/Users/Guillaume/Google Drive/Cours X/PSC/Groupe PSC/Corpus/Francais/Fichiers txt/mensonge"+str(k//2 + 1)+".txt", "wb") as fichier:
            fichier.write(t)
            