# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 15:31:26 2017

@author: wang
"""

import jieba
import codecs

def importer(auteur, numero, emplacement_corpus):
    """pour le texte en chinois"""
    file = codecs.open(emplacement_corpus + auteur + str(numero) + ".txt", encoding='utf-8')
    raw = file.read()
    """On peut choisir le type de cut ici"""    
    raw_list = jieba.cut_for_search(raw)
    """Ajouter l'espace entre chaque deux mots"""    
    new_raw = " ".join(raw_list)
    
    return new_raw
    



#"""for test"""
#from treetaggerwrapper import TreeTagger, make_tags
#
#emplacement_corpus = "/home/wang/Documents/PSC/GitDePSC/Corpus/chinois/"
#auteur = "HanHanx"
#numero = 3
#texte_brut = importer(auteur, numero, emplacement_corpus)   
#tagger = TreeTagger(TAGLANG = "zh")
#tags = make_tags(tagger.tag_text(texte_brut))
#for tag in tags:
#    print(tag)

