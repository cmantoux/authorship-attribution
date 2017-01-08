#!/usr/bin/env python
# coding: utf-8

import codecs

def importer(auteur,numero,emplacement_corpus):
    """permet d'ouvrir le fichier txt situé à l'adresse ci-dessous et nommé par exemple dumas1.txt => pour utiliser sur votre ordinateur, changez juste le chemin d'accès au corpus"""
    file = codecs.open(emplacement_corpus + auteur + str(numero) + '.txt', encoding = 'utf-8')
    raw = file.read()
    
    debut = 0
    fin = raw.find("End")
    raw = raw[debut:fin]

    return raw
    

import re

def formater(raw_text):
    # Remplace les tirets doubles par des tirets simples et un espace
    raw_text = re.sub("--"," - ", raw_text)
    # Remplace les mots de la forme "_mot_" par "mot"
    raw_text = re.sub("_","b", raw_text)
    # standardise les espaces et les sauts de ligne
    raw_text = re.sub(r'\s+', ' ', raw_text)
    return raw_text