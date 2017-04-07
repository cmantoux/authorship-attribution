# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 16:27:33 2016

@author: wang
"""

from tkinter import *
from tkinter import ttk
#from tkinter import filedialog
from tkinter import messagebox
#import os
#from tkinter import filedialog as fd

from time import time

from Carac.carac_gramm import *
from Carac.carac_lettres import *
from Carac.carac_ponct import *
from Carac.carac_complexite import *
from Carac.carac_stopwords import *
from classes import Analyseur, Probleme, Verification
from Clustering.kmeans import Kmeans
from Clustering.kmedoids import Kmedoids
from Apprentissage.reseau_textes import reseau_neurones
from Apprentissage.Bayes import Bayes
from Apprentissage.Apriori import Apriori
from Apprentissage.svm import SVM
from Interpretation.importance_composantes import importance, gain_information
from Verification.similarite import Similarity
from Verification.unmasking import Unmasking



    
root = Tk()
root.title("choose the parameters")

#mainframe
mainframe = ttk.Frame(root, padding='10 10 10 10', borderwidth='3', relief='flat')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


#notebook
notebook = ttk.Notebook(mainframe, width=1500, height=950)
frame1 = ttk.Frame(notebook, padding='40 40 40 40')
frame2 = ttk.Frame(notebook, padding='40 20 40 40')
frame3 = ttk.Frame(notebook, padding='40 40 40 40')
notebook.add(frame1, text='  Classification  ')
notebook.add(frame2, text='  Verification  ')
notebook.add(frame3, text='  About the database  ')
notebook.pack()





"""notebook Classification"""

"""vertical before horizontal, otherwise false, I don't know why"""
ttk.Separator(frame1, orient=VERTICAL).grid(column=3, rowspan=7, sticky="sn", padx=0, pady=10)
ttk.Separator(frame1, orient=HORIZONTAL).grid(columnspan=7, row=7, sticky="ew", padx=20, pady=20)


langue="fr"
def setLangue(self):
    global langue
    if forLangue.get()=='Anglais':
        langue="en"
    elif forLangue.get()=='Francais':
        langue="fr"
    elif forLangue.get()=='Allemand':
        langue="de"
    elif forLangue.get()=='Espagnol':
        langue="es"
    elif forLangue.get()=='Chinois':
        langue="zh"
ttk.Label(frame1, text="Langue").grid(column=0, row=0, padx=10, pady=10)
Languevar = StringVar()
forLangue = ttk.Combobox(frame1, textvariable=Languevar)
forLangue['values'] = ('Anglais', 'Francais', 'Allemand', 'Espagnol', 'Chinois')
forLangue.bind('<<ComboboxSelected>>', setLangue)
forLangue.grid(column=1, row=0)


classifieur=reseau_neurones()
def setClassifieur(self):
    global classifieur
    if forClassifieur.get()=='SVM':
        classifieur=SVM()
    elif forClassifieur.get()=='reseau_neurones':
        classifieur=reseau_neurones()
    elif forClassifieur.get()=='Bayes':
        classifieur=Bayes()
    elif forClassifieur.get()=='Apriori':
        classifieur=Apriori()
    elif forClassifieur.get()=='Kmeans':
        classifieur=Kmeans()
    elif forClassifieur.get()=='KMedoids':
        classifieur=KMedoids()
    elif forClassifieur.get()=='kPPV':
        classifieur=kPPV()
    elif forClassifieur.get()=='OPTICS':
        classifieur=OPTICS()
ttk.Label(frame1, text="Classifieur").grid(column=0, row=1, padx=10, pady=10)
Classifieurvar = StringVar()
forClassifieur = ttk.Combobox(frame1, textvariable=Classifieurvar)
forClassifieur['values'] = ('SVM', 'reseau_neurones', 'Bayes', 'Apriori', 'Kmeans', 'KMedoids', 'kPPV', 'OPTICS')
forClassifieur.bind('<<ComboboxSelected>>', setClassifieur)
forClassifieur.grid(column=1, row=1)


ttk.Label(frame1, text='taille_morceaux').grid(column=0, row=2, padx=10, pady=10)
taillevar = IntVar()
ttk.Entry(frame1, textvariable=taillevar).grid(column=1, row=2)


ttk.Label(frame1, text="Full Text").grid(column=0, row=3, padx=10, pady=10)
full_textvar = StringVar()
"""ttk.Radiobutton is not round, but Radiobutton is."""
true = Radiobutton(frame1, text='True', variable=full_textvar, value='True')
true.grid(column=1, row=3)      
false = Radiobutton(frame1, text='False', variable=full_textvar, value='False')
false.grid(column=2, row=3)


ttk.Label(frame1, text="Equilibrage").grid(column=0, row=4, padx=10, pady=10)
equilibragevar = StringVar()
"""ttk.Radiobutton is not round, but Radiobutton is."""
true = Radiobutton(frame1, text='True', variable=equilibragevar, value='True')
true.grid(column=1, row=4)      
false = Radiobutton(frame1, text='False', variable=equilibragevar, value='False')
false.grid(column=2, row=4)


ttk.Label(frame1, text="Equilibrage Eval").grid(column=0, row=5, padx=10, pady=10)
equilibrage_evalvar = StringVar()
"""ttk.Radiobutton is not round, but Radiobutton is."""
true = Radiobutton(frame1, text='True', variable=equilibrage_evalvar, value='True')
true.grid(column=1, row=5)      
false = Radiobutton(frame1, text='False', variable=equilibrage_evalvar, value='False')
false.grid(column=2, row=5)


ttk.Label(frame1, text="Normalisation").grid(column=0, row=6, padx=10, pady=10)
normalisationvar = StringVar()
"""ttk.Radiobutton is not round, but Radiobutton is."""
true = Radiobutton(frame1, text='True', variable=normalisationvar, value='True')
true.grid(column=1, row=6)
false = Radiobutton(frame1, text='False', variable=normalisationvar, value='False')
false.grid(column=2, row=6)


ttk.Label(frame1, text="Utiliser Textes Training").grid(column=4, row=0, padx=10, pady=10)
utiliser_textes_trainingvar = StringVar()
"""ttk.Radiobutton is not round, but Radiobutton is."""
true = Radiobutton(frame1, text='True', variable=utiliser_textes_trainingvar, value='True')
true.grid(column=5, row=0)
false = Radiobutton(frame1, text='False', variable=utiliser_textes_trainingvar, value='False')
false.grid(column=6, row=0)





ttk.Label(frame1, text='Analyseur').grid(column=4, row=1, padx=10, pady=10)

A=[]
Freq_Gramvar=StringVar()
def callFreq_Gram():
    if Freq_Gramvar.get()=='oui':
        if A.count(Freq_Gram)==0:
            A.append(Freq_Gram)
            print ('add Freq_Gram')
    else:
        A.remove(Freq_Gram)
        print ('remove Freq_Gram')
Checkbutton(frame1, text='Freq_Gram', variable=Freq_Gramvar, command=callFreq_Gram, onvalue='oui', offvalue='non').grid(column=5, row=2, padx=10, pady=10)

Markov_Gramvar=StringVar()
def callMarkov_Gram():
    if Markov_Gramvar.get()=='oui':
        if A.count(Markov_Gram)==0:
            A.append(Markov_Gram)
            print ('add Markov_Gram')
    else:
        A.remove(Markov_Gram)
        print ('remove Markov_Gram')
Checkbutton(frame1, text='Markov_Gram', variable=Markov_Gramvar, command=callMarkov_Gram, onvalue='oui', offvalue='non').grid(column=5, row=3, padx=10, pady=10)

Freq_Ngrammesvar=StringVar()
def callFreq_Ngrammes():
    if Freq_Ngrammesvar.get()=='oui':
        if A.count(Freq_Ngrammes)==0:
            A.append(Freq_Ngrammes)
            print ('add Freq_Ngrammes')
    else:
        A.remove(Freq_Ngrammes)
        print ('remove Freq_Ngrammes')
Checkbutton(frame1, text='Freq_Ngrammes', variable=Freq_Ngrammesvar, command=callFreq_Ngrammes, onvalue='oui', offvalue='non').grid(column=5, row=4, padx=10, pady=10)

Markov_Lettresvar=StringVar()
def callMarkov_Lettres():
    if Markov_Lettresvar.get()=='oui':
        if A.count(Markov_Lettres)==0:
            A.append(Markov_Lettres)
            print ('add Markov_Lettres')
    else:
        A.remove(Markov_Lettres)
        print ('remove Markov_Lettres')
Checkbutton(frame1, text='Markov_Lettres', variable=Markov_Lettresvar, command=callMarkov_Lettres, onvalue='oui', offvalue='non').grid(column=5, row=5, padx=10, pady=10)

Freq_Ponctvar=StringVar()
def callFreq_Ponct():
    if Freq_Ponctvar.get()=='oui':
        if A.count(Freq_Ponct)==0:
            A.append(Freq_Ponct)
            print ('add Freq_Ponct')
    else:
        A.remove(Freq_Ponct)
        print ('remove Freq_Ponct')
Checkbutton(frame1, text='Freq_Ponct', variable=Freq_Ponctvar, command=callFreq_Ponct, onvalue='oui', offvalue='non').grid(column=5, row=6, padx=10, pady=10)

Longueur_Phrasesvar=StringVar()
def callLongueur_Phrases():
    if Longueur_Phrasesvar.get()=='oui':
        if A.count(Longueur_Phrases)==0:
            A.append(Longueur_Phrases)
            print ('add Longueur_Phrases')
    else:
        A.remove(Longueur_Phrases)
        print ('remove Longueur_Phrases')
Checkbutton(frame1, text='Longueur_Phrases', variable=Longueur_Phrasesvar, command=callLongueur_Phrases, onvalue='oui', offvalue='non').grid(column=6, row=2, padx=10, pady=10)

Complexite_Grammaticalevar=StringVar()
def callComplexite_Grammaticale():
    if Complexite_Grammaticalevar.get()=='oui':
        if A.count(Complexite_Grammaticale)==0:
            A.append(Complexite_Grammaticale)
            print ('add Complexite_Grammaticale')
    else:
        A.remove(Complexite_Grammaticale)
        print ('remove Complexite_Grammaticale')
Checkbutton(frame1, text='Complexite_Grammaticale', variable=Complexite_Grammaticalevar, command=callComplexite_Grammaticale, onvalue='oui', offvalue='non').grid(column=6, row=3, padx=10, pady=10)

Complexite_Vocabulairevar=StringVar()
def callComplexite_Vocabulaire():
    if Complexite_Vocabulairevar.get()=='oui':
        if A.count(Complexite_Vocabulaire)==0:
            A.append(Complexite_Vocabulaire)
            print ('add Complexite_Vocabulaire')
    else:
        A.remove(Complexite_Vocabulaire)
        print ('remove Complexite_Vocabulaire')
Checkbutton(frame1, text='Complexite_Vocabulaire', variable=Complexite_Vocabulairevar, command=callComplexite_Vocabulaire, onvalue='oui', offvalue='non').grid(column=6, row=4, padx=10, pady=10)

Freq_Stopwordsvar=StringVar()
def callFreq_Stopwords():
    if Freq_Stopwordsvar.get()=='oui':
        if A.count(Freq_Stopwords)==0:
            A.append(Freq_Stopwords)
            print ('add Freq_Stopwords')            
    else:
        A.remove(Freq_Stopwords)
        print ('remove Freq_Stopwords')
Checkbutton(frame1, text='Freq_Stopwords', variable=Freq_Stopwordsvar, command=callFreq_Stopwords, onvalue='oui', offvalue='non').grid(column=6, row=5, padx=10, pady=10)





#"""here can only for one text, so do not use it"""
#ttk.Label(mainframe, text='Training Set').grid(column=0, row=5, padx=10, pady=10)
#def browsefunc():
#    global trainingvar
#    filename = fd.askopenfilename()
#    trainingvar = os.path.dirname(filename)
#    training.delete(0, END)
#    training.insert(0, trainingvar)
#trainingvar = StringVar()
#training = Entry(mainframe, textvariable=trainingvar)
#training.grid(column=1, row=5, padx=2, pady=2, sticky='we')
#buttonBrowse = Button(mainframe, text='Browse', command=browsefunc)
#buttonBrowse.grid(column=2, row=5)
#
#
#"""here can only for one text, so not use it"""
#ttk.Label(mainframe, text='Evaluation Set').grid(column=0, row=6, padx=10, pady=10)
#def browsefunc():
#    #global content
#    global evaluationvar
#    filename = fd.askopenfilename()
#    #infile = open(filename, 'r')
#    #content = infile.read()
#    evaluationvar = os.path.dirname(filename)
#    evaluation.delete(0, END)
#    evaluation.insert(0, evaluationvar)
#    #return content
#evaluationvar = StringVar()
#evaluation = Entry(mainframe, textvariable=evaluationvar)
#evaluation.grid(column=1, row=6, padx=2, pady=2, sticky='we')
#buttonBrowse = Button(mainframe, text='Browse', command=browsefunc)
#buttonBrowse.grid(column=2, row=6)

ttk.Label(frame1, text='Training Set').grid(column=0, row=8, padx=10, pady=10)
ttk.Label(frame1, text='Auteur').grid(column=1, row=8, padx=10, pady=10)
auteur1var = StringVar()
ttk.Entry(frame1, textvariable=auteur1var).grid(column=2, row=8)
ttk.Label(frame1, text='from').grid(column=3, row=8, padx=10, pady=10)
from1var = IntVar()
ttk.Entry(frame1, textvariable=from1var).grid(column=4, row=8)
ttk.Label(frame1, text='to').grid(column=5, row=8, padx=10, pady=10)
to1var = IntVar()
ttk.Entry(frame1, textvariable=to1var).grid(column=6, row=8)
ttk.Label(frame1, text='Auteur').grid(column=1, row=9, padx=10, pady=10)
auteur2var = StringVar()
ttk.Entry(frame1, textvariable=auteur2var).grid(column=2, row=9)
ttk.Label(frame1, text='from').grid(column=3, row=9, padx=10, pady=10)
from2var = IntVar()
ttk.Entry(frame1, textvariable=from2var).grid(column=4, row=9)
ttk.Label(frame1, text='to').grid(column=5, row=9, padx=10, pady=10)
to2var = IntVar()
ttk.Entry(frame1, textvariable=to2var).grid(column=6, row=9)


a1=0
auteurvar1=['']
fromvar1=[0]
tovar1=[0]
def Ajouter1():
    global a1
    global auteurvar1
    global fromvar1
    global tovar1  
    if a1<2:
        temp1=a1+1
        a1=temp1
        labelauteur = ttk.Label(frame1, text='Auteur')
        labelauteur.grid(column=1, row=9+a1, padx=10, pady=10)
        auteurvar1.append('')
        auteurvar1[a1] = StringVar()
        entryauteur = ttk.Entry(frame1, textvariable=auteurvar1[a1])
        entryauteur.grid(column=2, row=9+a1)
        labelfrom = ttk.Label(frame1, text='from')
        labelfrom.grid(column=3, row=9+a1, padx=10, pady=10)
        fromvar1.append(0)    
        fromvar1[a1] = IntVar()
        entryfrom = ttk.Entry(frame1, textvariable=fromvar1[a1])
        entryfrom.grid(column=4, row=9+a1)
        labelto = ttk.Label(frame1, text='to')
        labelto.grid(column=5, row=9+a1, padx=10, pady=10)
        tovar1.append(0)
        tovar1[a1] = IntVar()
        entryto = ttk.Entry(frame1, textvariable=tovar1[a1])
        entryto.grid(column=6, row=9+a1)
        auteurofcategories = ttk.Entry(frame1, textvariable=auteurvar1[a1])
        auteurofcategories.grid(column=3+a1, row=14)
        def Supprimer1():
            global a1
            global auteurvar1
            global fromvar1
            global tovar1
            labelauteur.destroy()
            entryauteur.destroy()
            labelfrom.destroy()
            entryfrom.destroy()
            labelto.destroy()
            entryto.destroy()
            auteurofcategories.destroy()
            buttonsupprimer1.destroy()
            del auteurvar1[a1]
            del fromvar1[a1]
            del tovar1[a1]
            temp1=a1-1
            a1=temp1
        buttonsupprimer1 = ttk.Button(frame1, text='Supprimer', command=Supprimer1)
        buttonsupprimer1.grid(column=0, row=9+a1)
    else:
        messagebox.showerror('ERROR!', 'Trop d\'auteurs à training!')
ttk.Button(frame1, text='Ajouter', command=Ajouter1).grid(column=0, row=9)


ttk.Label(frame1, text='Categories').grid(column=1, row=14, padx=10, pady=10)
ttk.Entry(frame1, textvariable=auteur1var).grid(column=2, row=14)
ttk.Entry(frame1, textvariable=auteur2var).grid(column=3, row=14)


ttk.Label(frame1, text='Evaluation Set').grid(column=0, row=15, padx=10, pady=10)
ttk.Label(frame1, text='Auteur').grid(column=1, row=15, padx=10, pady=10)
evalauteur1var = StringVar()
ttk.Entry(frame1, textvariable=evalauteur1var).grid(column=2, row=15)
ttk.Label(frame1, text='from').grid(column=3, row=15, padx=60, pady=10)
evalfrom1var = IntVar()
ttk.Entry(frame1, textvariable=evalfrom1var).grid(column=4, row=15)
ttk.Label(frame1, text='to').grid(column=5, row=15, padx=60, pady=10)
evalto1var = IntVar()
ttk.Entry(frame1, textvariable=evalto1var).grid(column=6, row=15)
ttk.Label(frame1, text='Auteur').grid(column=1, row=16, padx=10, pady=10)
evalauteur2var = StringVar()
ttk.Entry(frame1, textvariable=evalauteur2var).grid(column=2, row=16)
ttk.Label(frame1, text='from').grid(column=3, row=16, padx=60, pady=10)
evalfrom2var = IntVar()
ttk.Entry(frame1, textvariable=evalfrom2var).grid(column=4, row=16)
ttk.Label(frame1, text='to').grid(column=5, row=16, padx=60, pady=10)
evalto2var = IntVar()
ttk.Entry(frame1, textvariable=evalto2var).grid(column=6, row=16)


a2=0
auteurvar2=['']
fromvar2=[0]
tovar2=[0]
supposees=['']
def Ajouter2():
    global a2
    global auteurvar2
    global fromvar2
    global tovar2  
    if a2<2:
        temp2=a2+1
        a2=temp2
        labelauteur = ttk.Label(frame1, text='Auteur')
        labelauteur.grid(column=1, row=16+a2, padx=10, pady=10)
        auteurvar2.append('')
        auteurvar2[a2] = StringVar()
        entryauteur = ttk.Entry(frame1, textvariable=auteurvar2[a2])
        entryauteur.grid(column=2, row=16+a2)
        labelfrom = ttk.Label(frame1, text='from')
        labelfrom.grid(column=3, row=16+a2, padx=10, pady=10)
        fromvar2.append(0)    
        fromvar2[a2] = IntVar()
        entryfrom = ttk.Entry(frame1, textvariable=fromvar2[a2])
        entryfrom.grid(column=4, row=16+a2)
        labelto = ttk.Label(frame1, text='to')
        labelto.grid(column=5, row=16+a2, padx=10, pady=10)
        tovar2.append(0)
        tovar2[a2] = IntVar()
        entryto = ttk.Entry(frame1, textvariable=tovar2[a2])
        entryto.grid(column=6, row=16+a2)
        supposees.append('')
        supposees[a2] = StringVar()
        auteurofcategories = ttk.Entry(frame1, textvariable=supposees[a2])
        auteurofcategories.grid(column=3+a2, row=21)
        def Supprimer2():
            global a2
            global auteurvar2
            global fromvar2
            global tovar2
            labelauteur.destroy()
            entryauteur.destroy()
            labelfrom.destroy()
            entryfrom.destroy()
            labelto.destroy()
            entryto.destroy()
            auteurofcategories.destroy()
            buttonsupprimer2.destroy()
            del auteurvar2[a2]
            del fromvar2[a2]
            del tovar2[a2]
            temp2=a2-1
            a2=temp2
        buttonsupprimer2 = ttk.Button(frame1, text='Supprimer', command=Supprimer2)
        buttonsupprimer2.grid(column=0, row=16+a2)
    else:
        messagebox.showerror('ERROR!', 'Trop d\'auteurs à evaluer!')
ttk.Button(frame1, text='Ajouter', command=Ajouter2).grid(column=0, row=16)


ttk.Label(frame1, text='Categories Supposees').grid(column=1, row=21, padx=10, pady=10)
supposee1 = StringVar()
ttk.Entry(frame1, textvariable=supposee1).grid(column=2, row=21)
supposee2 = StringVar()
ttk.Entry(frame1, textvariable=supposee2).grid(column=3, row=21)





"""cette fonction reset n'inclut pas la fonction supprimer. Donc il faut supprimer ce qu'on a ajouté manuellemnt et puis reset."""
def reset_classification():
    if messagebox.askyesno('Confirmation!', 'Are you sure to reset all? You will lose all your choices.'):
        global langue
        global classifieur
        Languevar.set('')
        langue=''
        Classifieurvar.set('')
        classifieur=''
        taillevar.set(0)
        full_textvar.set('')
        equilibragevar.set('')
        equilibrage_evalvar.set('')
        normalisationvar.set('')
        utiliser_textes_trainingvar.set('')
        Freq_Gramvar.set('')
        Markov_Gramvar.set('')
        Freq_Ngrammesvar.set('')
        Markov_Lettresvar.set('')
        Freq_Ponctvar.set('')
        Longueur_Phrasesvar.set('')
        Complexite_Grammaticalevar.set('')
        Complexite_Vocabulairevar.set('')
        Freq_Stopwordsvar.set('')
        A.clear()
        auteur1var.set('')
        from1var.set(0)
        to1var.set(0)
        auteur2var.set('')
        from2var.set(0)
        to2var.set(0)
        evalauteur1var.set('')
        evalfrom1var.set(0)
        evalto1var.set(0)
        evalauteur2var.set('')
        evalfrom2var.set(0)
        evalto2var.set(0)
        supposee1.set('')
        supposee2.set('')
ttk.Button(frame1, text='Reset', command=reset_classification).grid(column=6, row=30, sticky=(E, S), padx=5, pady=30)


def run_classification():
    if messagebox.askyesno('Confirmation!', 'Are you sure to run it?'):
        d = time()
        liste_fonctions=[]
        if A.count(Freq_Gram):
            liste_fonctions.append(Freq_Gram(langue))
        if A.count(Markov_Gram):
            liste_fonctions.append(Markov_Gram(langue,saut=1))
        if A.count(Freq_Ngrammes):
            liste_fonctions.append(Freq_Ngrammes(langue,n=1))
        if A.count(Markov_Lettres):
            liste_fonctions.append(Markov_Lettres(langue))
        if A.count(Freq_Ponct):
            liste_fonctions.append(Freq_Ponct(langue))
        if A.count(Longueur_Phrases):
            liste_fonctions.append(Longueur_Phrases())
        if A.count(Complexite_Grammaticale):
            liste_fonctions.append(Complexite_Grammaticale(langue,saut=1))
        if A.count(Complexite_Vocabulaire):
            liste_fonctions.append(Complexite_Vocabulaire())
        if A.count(Freq_Stopwords):
            liste_fonctions.append(Freq_Stopwords(langue))
        analyseur=Analyseur(liste_fonctions)
        
        categories=[auteur1var.get()]+[auteur2var.get()]
        id_training_set=[[(auteur1var.get(),k) for k in range(from1var.get(),to1var.get())], [(auteur2var.get(),k) for k in range(from2var.get(),to2var.get())]]
        for i in range(1,len(auteurvar1)):
            print (auteurvar1[i].get())
            print (fromvar1[i].get())
            print (tovar1[i].get())
            categories.append(auteurvar1[i].get())
            id_training_set.append([(auteurvar1[i].get(),k) for k in range(fromvar1[i].get(),tovar1[i].get())])
        
        categories_supposees=[supposee1.get()]+[supposee2.get()]
        id_eval_set=[[(evalauteur1var.get(),k) for k in range(evalfrom1var.get(),evalto1var.get())], [(evalauteur2var.get(),k) for k in range(evalfrom2var.get(),evalto2var.get())]]
        for i in range(1,len(auteurvar2)):
            print (auteurvar2[i].get())
            print (fromvar2[i].get())
            print (tovar2[i].get())
            print (supposees[i].get())
            categories_supposees.append(supposees[i].get())
            id_eval_set.append([(auteurvar2[i].get(),k) for k in range(fromvar2[i].get(),tovar2[i].get())])
        
        if full_textvar.get()=='True':
            P = Probleme(id_training_set, categories, id_eval_set, categories_supposees, taillevar.get(), analyseur, classifieur, langue, full_text = True)
        else:
            P = Probleme(id_training_set, categories, id_eval_set, categories_supposees, taillevar.get(), analyseur, classifieur, langue, full_text = False)
        
        if equilibragevar.get()=='True':
            if equilibrage_evalvar.get()=='True':
                P.creer_textes(equilibrage = True, equilibrage_eval = True)
            else:
                P.creer_textes(equilibrage = True, equilibrage_eval = False)
        else:
            if equilibrage_evalvar.get()=='True':
                P.creer_textes(equilibrage = False, equilibrage_eval = True)
            else:
                P.creer_textes(equilibrage = False, equilibrage_eval = False)
        
        if normalisationvar.get()=='True':
            P.analyser(normalisation = True)
        else:
            P.analyser(normalisation = False)
        
        P.appliquer_classifieur()
        P.afficher()
        if utiliser_textes_trainingvar.get()=='True':
            P.interpreter(utiliser_textes_training=True)
        else:
            P.interpreter(utiliser_textes_training=False)
        
        P.afficher_graphique()
        f = time()
        print()
        print("Temps d'exécution : " + str(f-d) + "s")           
ttk.Button(frame1, text='Okay', command=run_classification).grid(column=7, row=30, sticky=(E, S), padx=5, pady=30)


def close_classification():
    if messagebox.askyesno('QUIT', 'Are you sure to close it?'):
        root.destroy()
ttk.Button(frame1, text='Cancel', command=close_classification).grid(column=8, row=30, sticky=(E, S), padx=5, pady=30)










"""notebook Verification"""

"""vertical before horizontal, otherwise false, I don't know why"""
ttk.Separator(frame2, orient=VERTICAL).grid(column=3, rowspan=6, sticky="sn", padx=0, pady=10)
ttk.Separator(frame2, orient=HORIZONTAL).grid(columnspan=7, row=6, sticky="ew", padx=20, pady=20)


Vlangue="fr"
def VsetLangue(self):
    global Vlangue
    if VforLangue.get()=='Anglais':
        Vlangue="en"
    elif VforLangue.get()=='Francais':
        Vlangue="fr"
    elif VforLangue.get()=='Allemand':
        Vlangue="de"
    elif VforLangue.get()=='Espagnol':
        Vlangue="es"
    elif VforLangue.get()=='Chinois':
        Vlangue="zh"
ttk.Label(frame2, text="Langue").grid(column=0, row=0, padx=10, pady=10)
VLanguevar = StringVar()
VforLangue = ttk.Combobox(frame2, textvariable=VLanguevar)
VforLangue['values'] = ('Anglais', 'Francais', 'Allemand', 'Espagnol', 'Chinois')
VforLangue.bind('<<ComboboxSelected>>', VsetLangue)
VforLangue.grid(column=1, row=0)


verificateur=Similarity()
def setVerificateur(self):
    global verificateur
    if forVerificateur.get()=='Unmasking':
        verificateur=Unmasking()
    elif forVerificateur.get()=='Similarity':
        verificateur=Similarity()
ttk.Label(frame2, text="Verificateur").grid(column=0, row=1, padx=10, pady=10)
Verificateurvar = StringVar()
forVerificateur = ttk.Combobox(frame2, textvariable=Verificateurvar)
forVerificateur['values'] = ('Similarity', 'Unmasking')
forVerificateur.bind('<<ComboboxSelected>>', setVerificateur)
forVerificateur.grid(column=1, row=1)


ttk.Label(frame2, text='taille_morceaux').grid(column=0, row=2, padx=10, pady=10)
Vtaillevar = IntVar()
ttk.Entry(frame2, textvariable=Vtaillevar).grid(column=1, row=2)


ttk.Label(frame2, text="Full_texte").grid(column=0, row=3, padx=10, pady=10)
Vfull_textvar = StringVar()
"""ttk.Radiobutton is not round, but Radiobutton is."""
true = Radiobutton(frame2, text='True', variable=Vfull_textvar, value='True')
true.grid(column=1, row=3)      
false = Radiobutton(frame2, text='False', variable=Vfull_textvar, value='False')
false.grid(column=2, row=3)


ttk.Label(frame2, text="Normalisation").grid(column=0, row=4, padx=10, pady=10)
Vnormalisationvar = StringVar()
"""ttk.Radiobutton is not round, but Radiobutton is."""
true = Radiobutton(frame2, text='True', variable=Vnormalisationvar, value='True')
true.grid(column=1, row=4)
false = Radiobutton(frame2, text='False', variable=Vnormalisationvar, value='False')
false.grid(column=2, row=4)





ttk.Label(frame2, text='Analyseur').grid(column=4, row=0, padx=10, pady=10)

VA=[]
VFreq_Gramvar=StringVar()
def VcallFreq_Gram():
    if VFreq_Gramvar.get()=='oui':
        if VA.count(Freq_Gram)==0:
            VA.append(Freq_Gram)
            print ('add Freq_Gram')
    else:
        VA.remove(Freq_Gram)
        print ('remove Freq_Gram')
Checkbutton(frame2, text='Freq_Gram', variable=VFreq_Gramvar, command=VcallFreq_Gram, onvalue='oui', offvalue='non').grid(column=5, row=1, padx=10, pady=10)

VMarkov_Gramvar=StringVar()
def VcallMarkov_Gram():
    if VMarkov_Gramvar.get()=='oui':
        if VA.count(Markov_Gram)==0:
            VA.append(Markov_Gram)
            print ('add Markov_Gram')
    else:
        VA.remove(Markov_Gram)
        print ('remove Markov_Gram')
Checkbutton(frame2, text='Markov_Gram', variable=VMarkov_Gramvar, command=VcallMarkov_Gram, onvalue='oui', offvalue='non').grid(column=5, row=2, padx=10, pady=10)

VFreq_Ngrammesvar=StringVar()
def VcallFreq_Ngrammes():
    if VFreq_Ngrammesvar.get()=='oui':
        if VA.count(Freq_Ngrammes)==0:
            VA.append(Freq_Ngrammes)
            print ('add Freq_Ngrammes')
    else:
        VA.remove(Freq_Ngrammes)
        print ('remove Freq_Ngrammes')
Checkbutton(frame2, text='Freq_Ngrammes', variable=VFreq_Ngrammesvar, command=VcallFreq_Ngrammes, onvalue='oui', offvalue='non').grid(column=5, row=3, padx=10, pady=10)

VMarkov_Lettresvar=StringVar()
def VcallMarkov_Lettres():
    if VMarkov_Lettresvar.get()=='oui':
        if VA.count(Markov_Lettres)==0:
            VA.append(Markov_Lettres)
            print ('add Markov_Lettres')
    else:
        VA.remove(Markov_Lettres)
        print ('remove Markov_Lettres')
Checkbutton(frame2, text='Markov_Lettres', variable=VMarkov_Lettresvar, command=VcallMarkov_Lettres, onvalue='oui', offvalue='non').grid(column=5, row=4, padx=10, pady=10)

VFreq_Ponctvar=StringVar()
def VcallFreq_Ponct():
    if VFreq_Ponctvar.get()=='oui':
        if VA.count(Freq_Ponct)==0:
            VA.append(Freq_Ponct)
            print ('add Freq_Ponct')
    else:
        VA.remove(Freq_Ponct)
        print ('remove Freq_Ponct')
Checkbutton(frame2, text='Freq_Ponct', variable=VFreq_Ponctvar, command=VcallFreq_Ponct, onvalue='oui', offvalue='non').grid(column=5, row=5, padx=10, pady=10)

VLongueur_Phrasesvar=StringVar()
def VcallLongueur_Phrases():
    if VLongueur_Phrasesvar.get()=='oui':
        if VA.count(Longueur_Phrases)==0:
            VA.append(Longueur_Phrases)
            print ('add Longueur_Phrases')
    else:
        VA.remove(Longueur_Phrases)
        print ('remove Longueur_Phrases')
Checkbutton(frame2, text='Longueur_Phrases', variable=VLongueur_Phrasesvar, command=VcallLongueur_Phrases, onvalue='oui', offvalue='non').grid(column=6, row=1, padx=10, pady=10)

VComplexite_Grammaticalevar=StringVar()
def VcallComplexite_Grammaticale():
    if VComplexite_Grammaticalevar.get()=='oui':
        if VA.count(Complexite_Grammaticale)==0:
            VA.append(Complexite_Grammaticale)
            print ('add Complexite_Grammaticale')
    else:
        VA.remove(Complexite_Grammaticale)
        print ('remove Complexite_Grammaticale')
Checkbutton(frame2, text='Complexite_Grammaticale', variable=VComplexite_Grammaticalevar, command=VcallComplexite_Grammaticale, onvalue='oui', offvalue='non').grid(column=6, row=2, padx=10, pady=10)

VComplexite_Vocabulairevar=StringVar()
def VcallComplexite_Vocabulaire():
    if VComplexite_Vocabulairevar.get()=='oui':
        if VA.count(Complexite_Vocabulaire)==0:
            VA.append(Complexite_Vocabulaire)
            print ('add Complexite_Vocabulaire')
    else:
        VA.remove(Complexite_Vocabulaire)
        print ('remove Complexite_Vocabulaire')
Checkbutton(frame2, text='Complexite_Vocabulaire', variable=VComplexite_Vocabulairevar, command=VcallComplexite_Vocabulaire, onvalue='oui', offvalue='non').grid(column=6, row=3, padx=10, pady=10)

VFreq_Stopwordsvar=StringVar()
def VcallFreq_Stopwords():
    if VFreq_Stopwordsvar.get()=='oui':
        if VA.count(Freq_Stopwords)==0:
            VA.append(Freq_Stopwords)
            print ('add Freq_Stopwords')            
    else:
        VA.remove(Freq_Stopwords)
        print ('remove Freq_Stopwords')
Checkbutton(frame2, text='Freq_Stopwords', variable=VFreq_Stopwordsvar, command=VcallFreq_Stopwords, onvalue='oui', offvalue='non').grid(column=6, row=4, padx=10, pady=10)





ttk.Label(frame2, text='id_oeuvres_base').grid(column=0, row=8, padx=10, pady=10)
ttk.Label(frame2, text='Auteur').grid(column=1, row=8, padx=10, pady=10)
Vbase_auteur1var = StringVar()
ttk.Entry(frame2, textvariable=Vbase_auteur1var).grid(column=2, row=8)
ttk.Label(frame2, text='from').grid(column=3, row=8, padx=60, pady=10)
Vbase_from1var = IntVar()
ttk.Entry(frame2, textvariable=Vbase_from1var).grid(column=4, row=8)
ttk.Label(frame2, text='to').grid(column=5, row=8, padx=60, pady=10)
Vbase_to1var = IntVar()
ttk.Entry(frame2, textvariable=Vbase_to1var).grid(column=6, row=8)
ttk.Label(frame2, text='Auteur').grid(column=1, row=9, padx=10, pady=10)
Vbase_auteur2var = StringVar()
ttk.Entry(frame2, textvariable=Vbase_auteur2var).grid(column=2, row=9)
ttk.Label(frame2, text='from').grid(column=3, row=9, padx=60, pady=10)
Vbase_from2var = IntVar()
ttk.Entry(frame2, textvariable=Vbase_from2var).grid(column=4, row=9)
ttk.Label(frame2, text='to').grid(column=5, row=9, padx=60, pady=10)
Vbase_to2var = IntVar()
ttk.Entry(frame2, textvariable=Vbase_to2var).grid(column=6, row=9)

Va1=0
Vauteurvar1=['']
Vfromvar1=[0]
Vtovar1=[0]
def VAjouter1():
    global Va1
    global Vauteurvar1
    global Vfromvar1
    global Vtovar1  
    if Va1<2:
        temp1=Va1+1
        Va1=temp1
        labelauteur = ttk.Label(frame2, text='Auteur')
        labelauteur.grid(column=1, row=9+Va1, padx=10, pady=10)
        Vauteurvar1.append('')
        Vauteurvar1[Va1] = StringVar()
        entryauteur = ttk.Entry(frame2, textvariable=Vauteurvar1[Va1])
        entryauteur.grid(column=2, row=9+Va1)
        labelfrom = ttk.Label(frame2, text='from')
        labelfrom.grid(column=3, row=9+Va1, padx=10, pady=10)
        Vfromvar1.append(0)    
        Vfromvar1[Va1] = IntVar()
        entryfrom = ttk.Entry(frame2, textvariable=Vfromvar1[Va1])
        entryfrom.grid(column=4, row=9+Va1)
        labelto = ttk.Label(frame2, text='to')
        labelto.grid(column=5, row=9+Va1, padx=10, pady=10)
        Vtovar1.append(0)
        Vtovar1[Va1] = IntVar()
        entryto = ttk.Entry(frame2, textvariable=Vtovar1[Va1])
        entryto.grid(column=6, row=9+Va1)
        auteurofcategories = ttk.Entry(frame2, textvariable=Vauteurvar1[Va1])
        auteurofcategories.grid(column=3+Va1, row=14)
        def VSupprimer1():
            global Va1
            global Vauteurvar1
            global Vfromvar1
            global Vtovar1
            labelauteur.destroy()
            entryauteur.destroy()
            labelfrom.destroy()
            entryfrom.destroy()
            labelto.destroy()
            entryto.destroy()
            auteurofcategories.destroy()
            Vbuttonsupprimer1.destroy()
            del Vauteurvar1[Va1]
            del Vfromvar1[Va1]
            del Vtovar1[Va1]
            temp1=Va1-1
            Va1=temp1
        Vbuttonsupprimer1 = ttk.Button(frame2, text='Supprimer', command=VSupprimer1)
        Vbuttonsupprimer1.grid(column=0, row=9+Va1)
    else:
        messagebox.showerror('ERROR!', 'Trop d\'auteurs à training!')
ttk.Button(frame2, text='Ajouter', command=VAjouter1).grid(column=0, row=9)

ttk.Label(frame2, text='categories_base').grid(column=1, row=14, padx=10, pady=10)
ttk.Entry(frame2, textvariable=Vbase_auteur1var).grid(column=2, row=14)
ttk.Entry(frame2, textvariable=Vbase_auteur2var).grid(column=3, row=14)


ttk.Label(frame2, text='id_oeuvres_calibrage').grid(column=0, row=15, padx=10, pady=10)
ttk.Label(frame2, text='Auteur').grid(column=1, row=15, padx=10, pady=10)
Vcalibrage_auteur1var = StringVar()
ttk.Entry(frame2, textvariable=Vcalibrage_auteur1var).grid(column=2, row=15)
ttk.Label(frame2, text='from').grid(column=3, row=15, padx=60, pady=10)
Vcalibrage_from1var = IntVar()
ttk.Entry(frame2, textvariable=Vcalibrage_from1var).grid(column=4, row=15)
ttk.Label(frame2, text='to').grid(column=5, row=15, padx=60, pady=10)
Vcalibrage_to1var = IntVar()
ttk.Entry(frame2, textvariable=Vcalibrage_to1var).grid(column=6, row=15)
ttk.Label(frame2, text='Auteur').grid(column=1, row=16, padx=10, pady=10)
Vcalibrage_auteur2var = StringVar()
ttk.Entry(frame2, textvariable=Vcalibrage_auteur2var).grid(column=2, row=16)
ttk.Label(frame2, text='from').grid(column=3, row=16, padx=60, pady=10)
Vcalibrage_from2var = IntVar()
ttk.Entry(frame2, textvariable=Vcalibrage_from2var).grid(column=4, row=16)
ttk.Label(frame2, text='to').grid(column=5, row=16, padx=60, pady=10)
Vcalibrage_to2var = IntVar()
ttk.Entry(frame2, textvariable=Vcalibrage_to2var).grid(column=6, row=16)

Va2=0
Vauteurvar2=['']
Vfromvar2=[0]
Vtovar2=[0]
def VAjouter2():
    global Va2
    global Vauteurvar2
    global Vfromvar2
    global Vtovar2  
    if Va2<2:
        temp2=Va2+1
        Va2=temp2
        labelauteur = ttk.Label(frame2, text='Auteur')
        labelauteur.grid(column=1, row=16+Va2, padx=10, pady=10)
        Vauteurvar2.append('')
        Vauteurvar2[Va2] = StringVar()
        entryauteur = ttk.Entry(frame2, textvariable=Vauteurvar2[Va2])
        entryauteur.grid(column=2, row=16+Va2)
        labelfrom = ttk.Label(frame2, text='from')
        labelfrom.grid(column=3, row=16+Va2, padx=10, pady=10)
        Vfromvar2.append(0)    
        Vfromvar2[Va2] = IntVar()
        entryfrom = ttk.Entry(frame2, textvariable=Vfromvar2[Va2])
        entryfrom.grid(column=4, row=16+Va2)
        labelto = ttk.Label(frame2, text='to')
        labelto.grid(column=5, row=16+Va2, padx=10, pady=10)
        Vtovar2.append(0)
        Vtovar2[Va2] = IntVar()
        entryto = ttk.Entry(frame2, textvariable=Vtovar2[Va2])
        entryto.grid(column=6, row=16+Va2)
        auteurofcategories = ttk.Entry(frame2, textvariable=Vauteurvar2[Va2])
        auteurofcategories.grid(column=3+Va2, row=21)
        def VSupprimer2():
            global Va2
            global Vauteurvar2
            global Vfromvar2
            global Vtovar2
            labelauteur.destroy()
            entryauteur.destroy()
            labelfrom.destroy()
            entryfrom.destroy()
            labelto.destroy()
            entryto.destroy()
            auteurofcategories.destroy()
            Vbuttonsupprimer2.destroy()
            del Vauteurvar2[Va2]
            del Vfromvar2[Va2]
            del Vtovar2[Va2]
            temp2=Va2-1
            Va2=temp2
        Vbuttonsupprimer2 = ttk.Button(frame2, text='Supprimer', command=VSupprimer2)
        Vbuttonsupprimer2.grid(column=0, row=16+Va2)
    else:
        messagebox.showerror('ERROR!', 'Trop d\'auteurs à evaluer!')
ttk.Button(frame2, text='Ajouter', command=VAjouter2).grid(column=0, row=16)

ttk.Label(frame2, text='categories_calibrage').grid(column=1, row=21, padx=10, pady=10)
ttk.Entry(frame2, textvariable=Vcalibrage_auteur1var).grid(column=2, row=21)
ttk.Entry(frame2, textvariable=Vcalibrage_auteur2var).grid(column=3, row=21)


ttk.Label(frame2, text='id_oeuvres_disputees').grid(column=0, row=22, padx=10, pady=10)
ttk.Label(frame2, text='Auteur').grid(column=1, row=22, padx=10, pady=10)
Vdisputees_auteur1var = StringVar()
ttk.Entry(frame2, textvariable=Vdisputees_auteur1var).grid(column=2, row=22)
ttk.Label(frame2, text='from').grid(column=3, row=22, padx=60, pady=10)
Vdisputees_from1var = IntVar()
ttk.Entry(frame2, textvariable=Vdisputees_from1var).grid(column=4, row=22)
ttk.Label(frame2, text='to').grid(column=5, row=22, padx=60, pady=10)
Vdisputees_to1var = IntVar()
ttk.Entry(frame2, textvariable=Vdisputees_to1var).grid(column=6, row=22)
ttk.Label(frame2, text='Auteur').grid(column=1, row=23, padx=10, pady=10)
Vdisputees_auteur2var = StringVar()
ttk.Entry(frame2, textvariable=Vdisputees_auteur2var).grid(column=2, row=23)
ttk.Label(frame2, text='from').grid(column=3, row=23, padx=60, pady=10)
Vdisputees_from2var = IntVar()
ttk.Entry(frame2, textvariable=Vdisputees_from2var).grid(column=4, row=23)
ttk.Label(frame2, text='to').grid(column=5, row=23, padx=60, pady=10)
Vdisputees_to2var = IntVar()
ttk.Entry(frame2, textvariable=Vdisputees_to2var).grid(column=6, row=23)

Va3=0
Vauteurvar3=['']
Vfromvar3=[0]
Vtovar3=[0]
def VAjouter3():
    global Va3
    global Vauteurvar3
    global Vfromvar3
    global Vtovar3  
    if Va3<2:
        temp3=Va3+1
        Va3=temp3
        labelauteur = ttk.Label(frame2, text='Auteur')
        labelauteur.grid(column=1, row=23+Va3, padx=10, pady=10)
        Vauteurvar3.append('')
        Vauteurvar3[Va3] = StringVar()
        entryauteur = ttk.Entry(frame2, textvariable=Vauteurvar3[Va3])
        entryauteur.grid(column=2, row=23+Va3)
        labelfrom = ttk.Label(frame2, text='from')
        labelfrom.grid(column=3, row=23+Va3, padx=10, pady=10)
        Vfromvar3.append(0)    
        Vfromvar3[Va3] = IntVar()
        entryfrom = ttk.Entry(frame2, textvariable=Vfromvar3[Va3])
        entryfrom.grid(column=4, row=23+Va3)
        labelto = ttk.Label(frame2, text='to')
        labelto.grid(column=5, row=23+Va3, padx=10, pady=10)
        Vtovar3.append(0)
        Vtovar3[Va3] = IntVar()
        entryto = ttk.Entry(frame2, textvariable=Vtovar3[Va3])
        entryto.grid(column=6, row=23+Va3)
        auteurofcategories = ttk.Entry(frame2, textvariable=Vauteurvar3[Va3])
        auteurofcategories.grid(column=3+Va3, row=28)
        def VSupprimer3():
            global Va3
            global Vauteurvar3
            global Vfromvar3
            global Vtovar3
            labelauteur.destroy()
            entryauteur.destroy()
            labelfrom.destroy()
            entryfrom.destroy()
            labelto.destroy()
            entryto.destroy()
            auteurofcategories.destroy()
            Vbuttonsupprimer3.destroy()
            del Vauteurvar3[Va3]
            del Vfromvar3[Va3]
            del Vtovar3[Va3]
            temp3=Va3-1
            Va3=temp3
        Vbuttonsupprimer3 = ttk.Button(frame2, text='Supprimer', command=VSupprimer3)
        Vbuttonsupprimer3.grid(column=0, row=23+Va3)
    else:
        messagebox.showerror('ERROR!', 'Trop d\'auteurs à evaluer!')
ttk.Button(frame2, text='Ajouter', command=VAjouter3).grid(column=0, row=23)

ttk.Label(frame2, text='categories_disputees').grid(column=1, row=28, padx=10, pady=10)
ttk.Entry(frame2, textvariable=Vdisputees_auteur1var).grid(column=2, row=28)
ttk.Entry(frame2, textvariable=Vdisputees_auteur2var).grid(column=3, row=28)







"""cette fonction reset n'inclut pas la fonction supprimer. Donc il faut supprimer ce qu'on a ajouté manuellemnt et puis reset."""
def reset_verification():
    global verificateur
    if messagebox.askyesno('Confirmation!', 'Are you sure to reset all? You will lose all your choices.'):
        VLanguevar.set('')
        Vlangue=''
        Verificateurvar.set('')
        verificateur=''
        Vtaillevar.set(0)
        Vfull_textvar.set('')
        Vnormalisationvar.set('')
        VFreq_Gramvar.set('')
        VMarkov_Gramvar.set('')
        VFreq_Ngrammesvar.set('')
        VMarkov_Lettresvar.set('')
        VFreq_Ponctvar.set('')
        VLongueur_Phrasesvar.set('')
        VComplexite_Grammaticalevar.set('')
        VComplexite_Vocabulairevar.set('')
        VFreq_Stopwordsvar.set('')
        VA.clear()
        Vbase_auteur1var.set('')
        Vbase_from1var.set(0)
        Vbase_to1var.set(0)
        Vbase_auteur2var.set('')
        Vbase_from2var.set(0)
        Vbase_to2var.set(0)
        Vcalibrage_auteur1var.set('')
        Vcalibrage_from1var.set(0)
        Vcalibrage_to1var.set(0)
        Vcalibrage_auteur2var.set('')
        Vcalibrage_from2var.set(0)
        Vcalibrage_to2var.set(0)
        Vdisputees_auteur1var.set('')
        Vdisputees_from1var.set(0)
        Vdisputees_to1var.set(0)
        Vdisputees_auteur2var.set('')
        Vdisputees_from2var.set(0)
        Vdisputees_to2var.set(0)
ttk.Button(frame2, text='Reset', command=reset_verification).grid(column=6, row=30, sticky=(E, S), padx=5, pady=30)


def run_verification():
    if messagebox.askyesno('Confirmation!', 'Are you sure to run it?'):
        Vliste_fonctions=[]
        if VA.count(Freq_Gram):
            Vliste_fonctions.append(Freq_Gram(langue))
        if VA.count(Markov_Gram):
            Vliste_fonctions.append(Markov_Gram(langue,saut=1))
        if VA.count(Freq_Ngrammes):
            Vliste_fonctions.append(Freq_Ngrammes(langue,n=1))
        if VA.count(Markov_Lettres):
            Vliste_fonctions.append(Markov_Lettres(langue))
        if VA.count(Freq_Ponct):
            Vliste_fonctions.append(Freq_Ponct(langue))
        if VA.count(Longueur_Phrases):
            Vliste_fonctions.append(Longueur_Phrases())
        if VA.count(Complexite_Grammaticale):
            Vliste_fonctions.append(Complexite_Grammaticale(langue,saut=1))
        if VA.count(Complexite_Vocabulaire):
            Vliste_fonctions.append(Complexite_Vocabulaire())
        if VA.count(Freq_Stopwords):
            Vliste_fonctions.append(Freq_Stopwords(langue))
        analyseur=Analyseur(Vliste_fonctions)
        
        categories_base=[Vbase_auteur1var.get()]+[Vbase_auteur2var.get()]
        #categories_base = ["categorie1"] + ["categorie2"]
        id_oeuvres_base=[[(Vbase_auteur1var.get(),k) for k in range(Vbase_from1var.get(),Vbase_to1var.get())], [(Vbase_auteur2var.get(),k) for k in range(Vbase_from2var.get(),Vbase_to2var.get())]]
        for i in range(1,len(Vauteurvar1)):
            print (Vauteurvar1[i].get())
            print (Vfromvar1[i].get())
            print (Vtovar1[i].get())
            categories_base.append(Vauteurvar1[i].get())
            id_oeuvres_base.append([(Vauteurvar1[i].get(),k) for k in range(Vfromvar1[i].get(),Vtovar1[i].get())])
        
        categories_calibrage=[Vcalibrage_auteur1var.get()]+[Vcalibrage_auteur2var.get()]
        #categories_calibrage = ["categorie1"] + ["categorie2"]
        id_oeuvres_calibrage=[[(Vcalibrage_auteur1var.get(),k) for k in range(Vcalibrage_from1var.get(),Vcalibrage_to1var.get())], [(Vcalibrage_auteur2var.get(),k) for k in range(Vcalibrage_from2var.get(),Vcalibrage_to2var.get())]]
        for i in range(1,len(Vauteurvar2)):
            print (Vauteurvar2[i].get())
            print (Vfromvar2[i].get())
            print (Vtovar2[i].get())
            categories_calibrage.append(Vauteurvar2[i].get())
            id_oeuvres_calibrage.append([(Vauteurvar2[i].get(),k) for k in range(Vfromvar2[i].get(),Vtovar2[i].get())])
            
        categories_disputees=[Vdisputees_auteur1var.get()]+[Vdisputees_auteur2var.get()]
        #categories_disputees = ["categorie1"] + ["categorie2"]
        id_oeuvres_disputees=[[(Vdisputees_auteur1var.get(),k) for k in range(Vdisputees_from1var.get(),Vdisputees_to1var.get())], [(Vdisputees_auteur2var.get(),k) for k in range(Vdisputees_from2var.get(),Vdisputees_to2var.get())]]
        for i in range(1,len(Vauteurvar3)):
            print (Vauteurvar3[i].get())
            print (Vfromvar3[i].get())
            print (Vtovar3[i].get())
            categories_disputees.append(Vauteurvar3[i].get())
            id_oeuvres_disputees.append([(Vauteurvar3[i].get(),k) for k in range(Vfromvar3[i].get(),Vtovar3[i].get())])
        
        if Vfull_textvar.get()=='True':
            V = Verification(id_oeuvres_base, categories_base, id_oeuvres_calibrage, categories_calibrage, id_oeuvres_disputees, categories_disputees, Vtaillevar.get(), analyseur, verificateur, Vlangue, full_text = True)
        else:
            V = Verification(id_oeuvres_base, categories_base, id_oeuvres_calibrage, categories_calibrage, id_oeuvres_disputees, categories_disputees, Vtaillevar.get(), analyseur, verificateur, Vlangue, full_text = False)
        
        V.creer_textes()
        
        if Vnormalisationvar.get()=='True':
            V.analyser(normalisation = True)
        else:
            V.analyser(normalisation = False)
        
        V.appliquer_verificateur()
ttk.Button(frame2, text='Okay', command=run_verification).grid(column=7, row=30, sticky=(E, S), padx=5, pady=30)


def close_verification():
    if messagebox.askyesno('QUIT', 'Are you sure to close it?'):
        root.destroy()
ttk.Button(frame2, text='Cancel', command=close_verification).grid(column=8, row=30, sticky=(E, S), padx=5, pady=30)










"""notebook About the database"""

DBlangue="fr"
def DBsetLangue(self):
    global DBlangue
    if DBforLangue.get()=='Anglais':
        DBlangue="en"
    elif DBforLangue.get()=='Francais':
        DBlangue="fr"
    elif DBforLangue.get()=='Allemand':
        DBlangue="de"
    elif DBforLangue.get()=='Espagnol':
        DBlangue="es"
    elif DBforLangue.get()=='Chinois':
        DBlangue="zh"
ttk.Label(frame3, text="Langue").grid(column=0, row=0, padx=20, pady=20)
DBLanguevar = StringVar()
DBforLangue = ttk.Combobox(frame3, textvariable=DBLanguevar)
DBforLangue['values'] = ('Anglais', 'Francais', 'Allemand', 'Espagnol', 'Chinois')
DBforLangue.bind('<<ComboboxSelected>>', DBsetLangue)
DBforLangue.grid(column=1, row=0)

#genre=''
def setGenre(self):
    global genre
    genre = genrevar.get()
ttk.Label(frame3, text='Genre').grid(column=3, row=0, padx=20, pady=20)
genrevar = StringVar()
forGenre = ttk.Combobox(frame3, textvariable=genrevar)
forGenre['values'] = ('Poétique', 'Narratif', 'Théâtral', 'Épistolaire', 'Argumentatif', 'Descriptif', 'Graphique', 'Expérimental', 'Autre')
forGenre.bind('<<ComboboxSelected>>', setGenre)
forGenre.grid(column=4, row=0)

ttk.Label(frame3, text='Auteur').grid(column=0, row=1, padx=20, pady=20)
auteurvar=StringVar()
auteur = ttk.Entry(frame3, textvariable=auteurvar)
auteur.grid(column=1, row=1)

#pays=''
def setPays(self):
    global pays
    pays = paysvar.get()
ttk.Label(frame3, text='Pays').grid(column=3, row=1, padx=20, pady=20)
paysvar=StringVar()
forPays = ttk.Combobox(frame3, textvariable=paysvar)
forPays['values'] = ('France', 'Angleterre', 'Allmagne', 'Espagne', 'Chine')
forPays.bind('<<ComboboxSelected>>', setPays)
forPays.grid(column=4, row=1)

ttk.Label(frame3, text='Annee').grid(column=0, row=2, padx=20, pady=5)
ttk.Label(frame3, text='From').grid(column=1, row=2, padx=20, pady=5)
from1var=IntVar()
ttk.Entry(frame3, textvariable=from1var).grid(column=2, row=2)
ttk.Label(frame3, text='To').grid(column=1, row=3, padx=20, pady=5)
to1var=IntVar()
ttk.Entry(frame3, textvariable=to1var).grid(column=2, row=3)

ttk.Label(frame3, text='Sexe').grid(column=3, row=2, padx=20, pady=5)
sexevar=StringVar()
true = Radiobutton(frame3, text='True', variable=sexevar, value='True')
true.grid(column=4, row=2)
false = Radiobutton(frame3, text='False', variable=sexevar, value='False')
false.grid(column=4, row=3)

ttk.Label(frame3, text='Naissance').grid(column=0, row=4, padx=20, pady=20)
naissancevar=IntVar()
naissance = ttk.Entry(frame3, textvariable=naissancevar)
naissance.grid(column=1, row=4)


#ttk.Label(frame3, text='Fichier').grid(column=0, row=0, padx=20, pady=20)
#fichiervar=StringVar()
#fichier = ttk.Entry(frame3, textvariable=fichiervar)
#fichier.grid(column=1, row=0)
#
#ttk.Label(frame3, text='Nom').grid(column=0, row=1, padx=20, pady=20)
#nomvar=StringVar()
#nom = ttk.Entry(frame3, textvariable=nomvar)
#nom.grid(column=1, row=1)


def reset_database():
    if messagebox.askyesno('Confirmation!', 'Are you sure to reset all? You will lose all your choices.'):
        fichiervar.set('')
        nomvar.set('')
        anneevar.set(0)
        genrevar.set('')
        auteurvar.set('')
        naissancevar.set(0)
        sexevar.set('')
        languevar.set('')
        paysvar.set('')
        commentairesvar.set('')      
ttk.Button(frame3, text='Reset', command=reset_database).grid(column=6, row=30, sticky=(E, S), padx=5, pady=30)

"""a mofifier"""
def run_database():
    messagebox.askyesno('Confirmation!', 'Are you sure to run it?')
                  
ttk.Button(frame3, text='Okay', command=run_database).grid(column=7, row=30, sticky=(E, S), padx=5, pady=30)


def close_database():
    if messagebox.askyesno('QUIT', 'Are you sure to close it?'):
        root.destroy()
ttk.Button(frame3, text='Cancel', command=close_database).grid(column=8, row=30, sticky=(E, S), padx=5, pady=30)









root.mainloop()