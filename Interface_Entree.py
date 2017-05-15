# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 16:27:33 2016

@author: wang
"""

from tkinter import *
from tkinter import ttk
#from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
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
#from Clustering.kmedoids import Kmedoids
from Apprentissage.reseau_textes import reseau_neurones
from Apprentissage.Bayes import Bayes
from Apprentissage.Apriori import Apriori
from Apprentissage.svm import SVM
from Interpretation.importance_composantes import importance, gain_information
from Verification.similarite import Similarity
from Verification.unmasking import Unmasking

from bdd import *



class FenetreEntree:
    def __init__(self):
        self.root = root = Tk()
        root.title("choose the parameters")

        # mainframe
        mainframe = ttk.Frame(root, padding='10 10 10 10', borderwidth='3', relief='flat')
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        # notebook
        notebook = ttk.Notebook(mainframe, width=1450, height=950)
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

        self.langue = ''

        def setLangue(event):
            if forLangue.get() == 'Anglais':
                self.langue = "en"
            elif forLangue.get() == 'Francais':
                self.langue = "fr"
            elif forLangue.get() == 'Allemand':
                self.langue = "de"
            elif forLangue.get() == 'Espagnol':
                self.langue = "es"
            elif forLangue.get() == 'Chinois':
                self.langue = "zh"

        ttk.Label(frame1, text="Langue").grid(column=0, row=0, padx=10, pady=10)
        Languevar = StringVar()
        forLangue = ttk.Combobox(frame1, textvariable=Languevar)
        forLangue['values'] = ('Anglais', 'Francais', 'Allemand', 'Espagnol', 'Chinois')
        forLangue.bind('<<ComboboxSelected>>', setLangue)
        forLangue.grid(column=1, row=0)

        self.classifieur = ''

        def setClassifieur(event):
            if forClassifieur.get() == 'SVM':
                self.classifieur = SVM()
            elif forClassifieur.get() == 'reseau_neurones':
                self.classifieur = reseau_neurones()
            elif forClassifieur.get() == 'Bayes':
                self.classifieur = Bayes()
            elif forClassifieur.get() == 'Apriori':
                self.classifieur = Apriori()
            elif forClassifieur.get() == 'Kmeans':
                self.classifieur = Kmeans()
            elif forClassifieur.get() == 'KMedoids':
                self.classifieur = KMedoids()
            elif forClassifieur.get() == 'kPPV':
                self.classifieur = kPPV()
            elif forClassifieur.get() == 'OPTICS':
                self.classifieur = OPTICS()

        ttk.Label(frame1, text="Classifieur").grid(column=0, row=1, padx=10, pady=10)
        Classifieurvar = StringVar()
        forClassifieur = ttk.Combobox(frame1, textvariable=Classifieurvar)
        forClassifieur['values'] = (
        'SVM', 'reseau_neurones', 'Bayes', 'Apriori', 'Kmeans', 'KMedoids', 'kPPV', 'OPTICS')
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

        self.A = []

        def callFreq_Gram():
            if Freq_Gramvar.get() == 'oui':
                if self.A.count(Freq_Gram) == 0:
                    self.A.append(Freq_Gram)
                    print('add Freq_Gram')
            else:
                self.A.remove(Freq_Gram)
                print('remove Freq_Gram')

        Freq_Gramvar = StringVar()
        Checkbutton(frame1, text='Freq_Gram', variable=Freq_Gramvar, command=callFreq_Gram, onvalue='oui',
                    offvalue='non').grid(column=5, row=2, padx=10, pady=10)

        self.Markov_Gram_saut = 0
        self.Markov_Gram_emondage = ''

        def callMarkov_Gram():
            if Markov_Gramvar.get() == 'oui':
                if self.A.count(Markov_Gram) == 0:
                    # Markov_Gram_root = Tk()
                    # Markov_Gram_root.title('choose the saut and emondage of Markov_Gram')
                    # Markov_Gram_frame = ttk.Frame(Markov_Gram_root, padding='10 10 10 10', borderwidth='3',
                    #                               relief='flat')
                    # Markov_Gram_frame.grid(column=0, row=0, sticky=(N, W, E, S))
                    # Markov_Gram_frame.columnconfigure(0, weight=1)
                    # Markov_Gram_frame.rowconfigure(0, weight=1)
                    #
                    # ttk.Label(Markov_Gram_frame, text='Saut').grid(column=0, row=0)
                    # Markov_Gram_sautvar = IntVar()
                    # ttk.Entry(Markov_Gram_frame, textvariable=Markov_Gram_sautvar).grid(column=1, row=0, padx=5)
                    #
                    # ttk.Label(Markov_Gram_frame, text="Emondage").grid(column=0, row=1, padx=10, pady=10)
                    # Markov_Gram_emondagevar = StringVar()
                    # true = Radiobutton(Markov_Gram_frame, text='True', variable=Markov_Gram_emondagevar, value='True')
                    # true.grid(column=1, row=1)
                    # false = Radiobutton(Markov_Gram_frame, text='False', variable=Markov_Gram_emondagevar, value='False')
                    # false.grid(column=1, row=2)
                    #
                    # def Markov_Gram_Okay():
                    #     self.Markov_Gram_saut = Markov_Gram_sautvar.get()
                    #     if Markov_Gram_emondagevar.get() == 'True':
                    #         self.Markov_Gram_emondage = True
                    #     else:
                    #         self.Markov_Gram_emondage = False
                    #     print(Markov_Gram_sautvar.get())
                    #     print(self.Markov_Gram_saut)
                    #     print(self.Markov_Gram_emondage)
                    #     Markov_Gram_root.destroy()
                    #
                    # ttk.Button(Markov_Gram_frame, text='Okay', command=Markov_Gram_Okay).grid(column=2, row=3, padx=5)
                    #
                    # def Markov_Gram_Cancel():
                    #     Markov_Gram_root.destroy()
                    #
                    # ttk.Button(Markov_Gram_frame, text='Cancel', command=Markov_Gram_Cancel).grid(column=3, row=3,
                    #                                                                              padx=5)

                    self.Markov_Gram_saut = simpledialog.askinteger("Insert the saut of Markov_Gram", "Saut")
                    emondage = simpledialog.askstring("Insert the emondage of Markov_Gram", "Emondage: True/False?")
                    if emondage == "True":
                        self.Markov_Gram_emondage = True
                    else:
                        self.Markov_Gram_emondage = False
                    self.A.append(Markov_Gram)
                    print('add Markov_Gram')
                    # Markov_Gram_root.mainloop()
            else:
                self.Markov_Gram_saut = 0
                self.Markov_Gram_emondage = ''
                self.A.remove(Markov_Gram)
                print('remove Markov_Gram')

        Markov_Gramvar = StringVar()
        Checkbutton(frame1, text='Markov_Gram', variable=Markov_Gramvar, command=callMarkov_Gram, onvalue='oui',
                    offvalue='non').grid(column=5, row=3, padx=10, pady=10)

        self.Freq_Ngrammes_n = 0

        def callFreq_Ngrammes():
            if Freq_Ngrammesvar.get() == 'oui':
                if self.A.count(Freq_Ngrammes) == 0:
                    # Freq_Ngrammes_root = Tk()
                    # Freq_Ngrammes_root.title('choose the n of Freq_Ngrammes')
                    # Freq_Ngrammes_frame = ttk.Frame(Freq_Ngrammes_root, padding='10 10 10 10', borderwidth='3',
                    #                                 relief='flat')
                    # Freq_Ngrammes_frame.grid(column=0, row=0, sticky=(N, W, E, S))
                    # Freq_Ngrammes_frame.columnconfigure(0, weight=1)
                    # Freq_Ngrammes_frame.rowconfigure(0, weight=1)
                    # ttk.Label(Freq_Ngrammes_frame, text='N').grid(column=0, row=0)
                    # Freq_Ngrammes_nvar = IntVar()
                    # ttk.Entry(Freq_Ngrammes_root, textvariable=Freq_Ngrammes_nvar).grid(column=1, row=0, padx=5)
                    #
                    # def Freq_Ngrammes_Okay():
                    #     self.Freq_Ngrammes_n = Freq_Ngrammes_nvar.get()
                    #     print (self.Freq_Ngrammes_n)
                    #     Freq_Ngrammes_root.destroy()
                    #
                    # ttk.Button(Freq_Ngrammes_root, text='Okay', command=Freq_Ngrammes_Okay).grid(column=2, row=0,
                    #                                                                              padx=5)
                    #
                    # def Freq_Ngrammes_Cancel():
                    #     Freq_Ngrammes_root.destroy()
                    #
                    # ttk.Button(Freq_Ngrammes_root, text='Cancel', command=Freq_Ngrammes_Cancel).grid(column=3, row=0,
                    #                                                                                  padx=5)

                    self.Freq_Ngrammes_n = simpledialog.askinteger("Insert the n of Freq_Ngrammes", "n")
                    self.A.append(Freq_Ngrammes)
                    print('add Freq_Ngrammes')
                    # Freq_Ngrammes_root.mainloop()
            else:
                self.Freq_Ngrammes_n = 0
                self.A.remove(Freq_Ngrammes)
                print('remove Freq_Ngrammes')

        Freq_Ngrammesvar = StringVar()
        Checkbutton(frame1, text='Freq_Ngrammes', variable=Freq_Ngrammesvar, command=callFreq_Ngrammes, onvalue='oui',
                    offvalue='non').grid(column=5, row=4, padx=10, pady=10)


        def callMarkov_Lettres():
            if Markov_Lettresvar.get() == 'oui':
                if self.A.count(Markov_Lettres) == 0:
                    self.A.append(Markov_Lettres)
                    print('add Markov_Lettres')
            else:
                self.A.remove(Markov_Lettres)
                print('remove Markov_Lettres')

        Markov_Lettresvar = StringVar()
        Checkbutton(frame1, text='Markov_Lettres', variable=Markov_Lettresvar, command=callMarkov_Lettres,
                    onvalue='oui', offvalue='non').grid(column=5, row=5, padx=10, pady=10)


        def callFreq_Ponct():
            if Freq_Ponctvar.get() == 'oui':
                if self.A.count(Freq_Ponct) == 0:
                    self.A.append(Freq_Ponct)
                    print('add Freq_Ponct')
            else:
                self.A.remove(Freq_Ponct)
                print('remove Freq_Ponct')

        Freq_Ponctvar = StringVar()
        Checkbutton(frame1, text='Freq_Ponct', variable=Freq_Ponctvar, command=callFreq_Ponct, onvalue='oui',
                    offvalue='non').grid(column=5, row=6, padx=10, pady=10)


        def callLongueur_Phrases():
            if Longueur_Phrasesvar.get() == 'oui':
                if self.A.count(Longueur_Phrases) == 0:
                    self.A.append(Longueur_Phrases)
                    print('add Longueur_Phrases')
            else:
                self.A.remove(Longueur_Phrases)
                print('remove Longueur_Phrases')

        Longueur_Phrasesvar = StringVar()
        Checkbutton(frame1, text='Longueur_Phrases', variable=Longueur_Phrasesvar, command=callLongueur_Phrases,
                    onvalue='oui', offvalue='non').grid(column=6, row=2, padx=10, pady=10)

        self.Complexite_Grammaticale_saut = 0

        def callComplexite_Grammaticale():
            if Complexite_Grammaticalevar.get() == 'oui':
                if self.A.count(Complexite_Grammaticale) == 0:
                    # Complexite_Grammaticale_root = Tk()
                    # Complexite_Grammaticale_root.title('choose the saut of Complexite_Grammaticale')
                    # Complexite_Grammaticale_frame = ttk.Frame(Complexite_Grammaticale_root, padding='10 10 10 10',
                    #                                           borderwidth='3', relief='flat')
                    # Complexite_Grammaticale_frame.grid(column=0, row=0, sticky=(N, W, E, S))
                    # Complexite_Grammaticale_frame.columnconfigure(0, weight=1)
                    # Complexite_Grammaticale_frame.rowconfigure(0, weight=1)
                    # ttk.Label(Complexite_Grammaticale_frame, text='Saut').grid(column=0, row=0)
                    # Complexite_Grammaticale_sautvar = IntVar()
                    # ttk.Entry(Complexite_Grammaticale_root, textvariable=Complexite_Grammaticale_sautvar).grid(column=1,
                    #                                                                                            row=0,
                    #                                                                                            padx=5)
                    #
                    # def Complexite_Grammaticale_Okay():
                    #     self.Complexite_Grammaticale_saut = Complexite_Grammaticale_sautvar.get()
                    #     print (self.Complexite_Grammaticale_saut)
                    #     Complexite_Grammaticale_root.destroy()
                    #
                    # ttk.Button(Complexite_Grammaticale_root, text='Okay', command=Complexite_Grammaticale_Okay).grid(
                    #     column=2, row=0, padx=5)
                    #
                    # def Complexite_Grammaticale_Cancel():
                    #     Complexite_Grammaticale_root.destroy()
                    #
                    # ttk.Button(Complexite_Grammaticale_root, text='Cancel',
                    #            command=Complexite_Grammaticale_Cancel).grid(column=3, row=0, padx=5)

                    self.Complexite_Grammaticale_saut = simpledialog.askinteger("Insert the saut of Complexite_Grammaticale", "Saut")
                    self.A.append(Complexite_Grammaticale)
                    print('add Complexite_Grammaticale')
                    # Complexite_Grammaticale_root.mainloop()
            else:
                self.Complexite_Grammaticale_saut = 0
                self.A.remove(Complexite_Grammaticale)
                print('remove Complexite_Grammaticale')

        Complexite_Grammaticalevar = StringVar()
        Checkbutton(frame1, text='Complexite_Grammaticale', variable=Complexite_Grammaticalevar,
                    command=callComplexite_Grammaticale, onvalue='oui', offvalue='non').grid(column=6, row=3, padx=10,
                                                                                             pady=10)


        def callComplexite_Vocabulaire():
            if Complexite_Vocabulairevar.get() == 'oui':
                if self.A.count(Complexite_Vocabulaire) == 0:
                    self.A.append(Complexite_Vocabulaire)
                    print('add Complexite_Vocabulaire')
            else:
                self.A.remove(Complexite_Vocabulaire)
                print('remove Complexite_Vocabulaire')

        Complexite_Vocabulairevar = StringVar()
        Checkbutton(frame1, text='Complexite_Vocabulaire', variable=Complexite_Vocabulairevar,
                    command=callComplexite_Vocabulaire, onvalue='oui', offvalue='non').grid(column=6, row=4, padx=10,
                                                                                            pady=10)

        def callFreq_Stopwords():
            if Freq_Stopwordsvar.get() == 'oui':
                if self.A.count(Freq_Stopwords) == 0:
                    self.A.append(Freq_Stopwords)
                    print('add Freq_Stopwords')
            else:
                self.A.remove(Freq_Stopwords)
                print('remove Freq_Stopwords')

        Freq_Stopwordsvar = StringVar()
        Checkbutton(frame1, text='Freq_Stopwords', variable=Freq_Stopwordsvar, command=callFreq_Stopwords,
                    onvalue='oui', offvalue='non').grid(column=6, row=5, padx=10, pady=10)

        # """here can only for one text, so do not use it"""
        # ttk.Label(mainframe, text='Training Set').grid(column=0, row=5, padx=10, pady=10)
        # def browsefunc():
        #    global trainingvar
        #    filename = fd.askopenfilename()
        #    trainingvar = os.path.dirname(filename)
        #    training.delete(0, END)
        #    training.insert(0, trainingvar)
        # trainingvar = StringVar()
        # training = Entry(mainframe, textvariable=trainingvar)
        # training.grid(column=1, row=5, padx=2, pady=2, sticky='we')
        # buttonBrowse = Button(mainframe, text='Browse', command=browsefunc)
        # buttonBrowse.grid(column=2, row=5)
        #
        #
        # """here can only for one text, so not use it"""
        # ttk.Label(mainframe, text='Evaluation Set').grid(column=0, row=6, padx=10, pady=10)
        # def browsefunc():
        #    #global content
        #    global evaluationvar
        #    filename = fd.askopenfilename()
        #    #infile = open(filename, 'r')
        #    #content = infile.read()
        #    evaluationvar = os.path.dirname(filename)
        #    evaluation.delete(0, END)
        #    evaluation.insert(0, evaluationvar)
        #    #return content
        # evaluationvar = StringVar()
        # evaluation = Entry(mainframe, textvariable=evaluationvar)
        # evaluation.grid(column=1, row=6, padx=2, pady=2, sticky='we')
        # buttonBrowse = Button(mainframe, text='Browse', command=browsefunc)
        # buttonBrowse.grid(column=2, row=6)

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

        self.a1 = 0
        self.auteurvar1 = ['']
        self.fromvar1 = [0]
        self.tovar1 = [0]
        self.categoriesvar = ['']

        def Ajouter1():
            if self.a1 < 2:
                temp1 = self.a1 + 1
                self.a1 = temp1
                labelauteur = ttk.Label(frame1, text='Auteur')
                labelauteur.grid(column=1, row=9 + self.a1, padx=10, pady=10)
                self.auteurvar1.append('')
                self.auteurvar1[self.a1] = StringVar()
                entryauteur = ttk.Entry(frame1, textvariable=self.auteurvar1[self.a1])
                entryauteur.grid(column=2, row=9 + self.a1)
                labelfrom = ttk.Label(frame1, text='from')
                labelfrom.grid(column=3, row=9 + self.a1, padx=10, pady=10)
                self.fromvar1.append(0)
                self.fromvar1[self.a1] = IntVar()
                entryfrom = ttk.Entry(frame1, textvariable=self.fromvar1[self.a1])
                entryfrom.grid(column=4, row=9 + self.a1)
                labelto = ttk.Label(frame1, text='to')
                labelto.grid(column=5, row=9 + self.a1, padx=10, pady=10)
                self.tovar1.append(0)
                self.tovar1[self.a1] = IntVar()
                entryto = ttk.Entry(frame1, textvariable=self.tovar1[self.a1])
                entryto.grid(column=6, row=9 + self.a1)
                self.categoriesvar.append('')
                self.categoriesvar[self.a1] = StringVar()
                auteurofcategories = ttk.Entry(frame1, textvariable=self.categoriesvar[self.a1])
                auteurofcategories.grid(column=3 + self.a1, row=14)

                def Supprimer1():
                    labelauteur.destroy()
                    entryauteur.destroy()
                    labelfrom.destroy()
                    entryfrom.destroy()
                    labelto.destroy()
                    entryto.destroy()
                    auteurofcategories.destroy()
                    buttonsupprimer1.destroy()
                    del self.auteurvar1[self.a1]
                    del self.fromvar1[self.a1]
                    del self.tovar1[self.a1]
                    del self.categoriesvar[self.a1]
                    temp1 = self.a1 - 1
                    self.a1 = temp1

                buttonsupprimer1 = ttk.Button(frame1, text='Supprimer', command=Supprimer1)
                buttonsupprimer1.grid(column=0, row=9 + self.a1)
            else:
                messagebox.showerror('ERROR!', 'Trop d\'auteurs à training!')

        ttk.Button(frame1, text='Ajouter', command=Ajouter1).grid(column=0, row=9)

        ttk.Label(frame1, text='Categories').grid(column=1, row=14, padx=10, pady=10)
        categorie1var = StringVar()
        ttk.Entry(frame1, textvariable=categorie1var).grid(column=2, row=14)
        categorie2var = StringVar()
        ttk.Entry(frame1, textvariable=categorie2var).grid(column=3, row=14)

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

        self.a2 = 0
        self.auteurvar2 = ['']
        self.fromvar2 = [0]
        self.tovar2 = [0]
        self.supposees = ['']

        def Ajouter2():
            if self.a2 < 2:
                temp2 = self.a2 + 1
                self.a2 = temp2
                labelauteur = ttk.Label(frame1, text='Auteur')
                labelauteur.grid(column=1, row=16 + self.a2, padx=10, pady=10)
                self.auteurvar2.append('')
                self.auteurvar2[self.a2] = StringVar()
                entryauteur = ttk.Entry(frame1, textvariable=self.auteurvar2[self.a2])
                entryauteur.grid(column=2, row=16 + self.a2)
                labelfrom = ttk.Label(frame1, text='from')
                labelfrom.grid(column=3, row=16 + self.a2, padx=10, pady=10)
                self.fromvar2.append(0)
                self.fromvar2[self.a2] = IntVar()
                entryfrom = ttk.Entry(frame1, textvariable=self.fromvar2[self.a2])
                entryfrom.grid(column=4, row=16 + self.a2)
                labelto = ttk.Label(frame1, text='to')
                labelto.grid(column=5, row=16 + self.a2, padx=10, pady=10)
                self.tovar2.append(0)
                self.tovar2[self.a2] = IntVar()
                entryto = ttk.Entry(frame1, textvariable=self.tovar2[self.a2])
                entryto.grid(column=6, row=16 + self.a2)
                self.supposees.append('')
                self.supposees[self.a2] = StringVar()
                auteurofcategories = ttk.Entry(frame1, textvariable=self.supposees[self.a2])
                auteurofcategories.grid(column=3 + self.a2, row=21)

                def Supprimer2():
                    labelauteur.destroy()
                    entryauteur.destroy()
                    labelfrom.destroy()
                    entryfrom.destroy()
                    labelto.destroy()
                    entryto.destroy()
                    auteurofcategories.destroy()
                    buttonsupprimer2.destroy()
                    del self.auteurvar2[self.a2]
                    del self.fromvar2[self.a2]
                    del self.tovar2[self.a2]
                    del self.supposees[self.a2]
                    temp2 = self.a2 - 1
                    self.a2 = temp2

                buttonsupprimer2 = ttk.Button(frame1, text='Supprimer', command=Supprimer2)
                buttonsupprimer2.grid(column=0, row=16 + self.a2)
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
                Languevar.set('')
                self.langue = ''
                Classifieurvar.set('')
                self.classifieur = ''
                taillevar.set(0)
                full_textvar.set('')
                equilibragevar.set('')
                equilibrage_evalvar.set('')
                normalisationvar.set('')
                utiliser_textes_trainingvar.set('')
                Freq_Gramvar.set('')
                Markov_Gramvar.set('')
                self.Markov_Gram_saut = 0
                self.Markov_Gram_emondage = ''
                Freq_Ngrammesvar.set('')
                self.Freq_Ngrammes_n = 0
                Markov_Lettresvar.set('')
                Freq_Ponctvar.set('')
                Longueur_Phrasesvar.set('')
                Complexite_Grammaticalevar.set('')
                self.Complexite_Grammaticale_saut = 0
                Complexite_Vocabulairevar.set('')
                Freq_Stopwordsvar.set('')
                self.A.clear()
                auteur1var.set('')
                from1var.set(0)
                to1var.set(0)
                auteur2var.set('')
                from2var.set(0)
                to2var.set(0)
                categorie1var.set('')
                categorie2var.set('')
                evalauteur1var.set('')
                evalfrom1var.set(0)
                evalto1var.set(0)
                evalauteur2var.set('')
                evalfrom2var.set(0)
                evalto2var.set(0)
                supposee1.set('')
                supposee2.set('')
                self.id_training_set = []
                self.id_eval_set = []
                self.training_use_BDD = False
                self.eval_use_BDD = False

        ttk.Button(frame1, text='Reset', command=reset_classification).grid(column=6, row=30, sticky=(E, S), padx=5,
                                                                            pady=30)

        self.id_training_set = []
        self.id_eval_set = []
        self.training_use_BDD = False
        self.eval_use_BDD = False

        def run_classification():
            if messagebox.askyesno('Confirmation!', 'Are you sure to run it?'):
                d = time()
                liste_fonctions = []
                nom_analyseurs = None
                if self.A.count(Freq_Gram) != 0:
                    liste_fonctions.append(Freq_Gram(self.langue))
                    if nom_analyseurs == None or nom_analyseurs == 'Grammaire':
                        nom_analyseurs = 'Grammaire'
                    else:
                        nom_analyseurs = 'Tout'
                if self.A.count(Markov_Gram) != 0:
                    liste_fonctions.append(Markov_Gram(self.langue, saut=self.Markov_Gram_saut, emondage=self.Markov_Gram_emondage))
                    if nom_analyseurs == None or nom_analyseurs == 'Grammaire':
                        nom_analyseurs = 'Grammaire'
                    else:
                        nom_analyseurs = 'Tout'
                if self.A.count(Freq_Ngrammes) != 0:
                    liste_fonctions.append(Freq_Ngrammes(self.langue, n=self.Freq_Ngrammes_n))
                    if nom_analyseurs == None or nom_analyseurs == 'Lettres':
                        nom_analyseurs = 'Lettres'
                    else:
                        nom_analyseurs = 'Tout'
                if self.A.count(Markov_Lettres) != 0:
                    liste_fonctions.append(Markov_Lettres(self.langue))
                    if nom_analyseurs == None or nom_analyseurs == 'Lettres':
                        nom_analyseurs = 'Lettres'
                    else:
                        nom_analyseurs = 'Tout'
                if self.A.count(Freq_Ponct) != 0:
                    liste_fonctions.append(Freq_Ponct(self.langue))
                    if nom_analyseurs == None or nom_analyseurs == 'Ponctuation':
                        nom_analyseurs = 'Ponctuation'
                    else:
                        nom_analyseurs = 'Tout'
                if self.A.count(Longueur_Phrases) != 0:
                    liste_fonctions.append(Longueur_Phrases())
                    if nom_analyseurs == None or nom_analyseurs == 'Ponctuation':
                        nom_analyseurs = 'Ponctuation'
                    else:
                        nom_analyseurs = 'Tout'
                if self.A.count(Complexite_Grammaticale) != 0:
                    liste_fonctions.append(Complexite_Grammaticale(self.langue, saut=self.Complexite_Grammaticale_saut))
                    if nom_analyseurs == None or nom_analyseurs == 'Complexite':
                        nom_analyseurs = 'Complexite'
                    else:
                        nom_analyseurs = 'Tout'
                if self.A.count(Complexite_Vocabulaire) != 0:
                    liste_fonctions.append(Complexite_Vocabulaire())
                    if nom_analyseurs == None or nom_analyseurs == 'Complexite':
                        nom_analyseurs = 'Complexite'
                    else:
                        nom_analyseurs = 'Tout'
                if self.A.count(Freq_Stopwords) != 0:
                    liste_fonctions.append(Freq_Stopwords(self.langue))
                    if nom_analyseurs == None or nom_analyseurs == 'Stopwords':
                        nom_analyseurs = 'Stopwords'
                    else:
                        nom_analyseurs = 'Tout'
                analyseur = Analyseur(nom_analyseurs, liste_fonctions)
                analyseur.numeroter()

                categories = [categorie1var.get()] + [categorie2var.get()]
                if self.training_use_BDD:
                    for i in range(1, len(self.auteurvar1)):
                        print(self.auteurvar1[i].get())
                        print(self.fromvar1[i].get())
                        print(self.tovar1[i].get())
                        print(self.categoriesvar[i].get())
                        categories.append(self.categoriesvar[i].get())
                else:
                    self.id_training_set = [[(auteur1var.get(), k) for k in range(from1var.get(), to1var.get())], [(auteur2var.get(), k) for k in range(from2var.get(), to2var.get())]]
                    for i in range(1, len(self.auteurvar1)):
                        print(self.auteurvar1[i].get())
                        print(self.fromvar1[i].get())
                        print(self.tovar1[i].get())
                        print(self.categoriesvar[i].get())
                        categories.append(self.categoriesvar[i].get())
                        self.id_training_set.append([(self.auteurvar1[i].get(), k) for k in range(self.fromvar1[i].get(), self.tovar1[i].get())])

                print('Training Set: ', self.id_training_set)

                categories_supposees = [supposee1.get()] + [supposee2.get()]
                if self.eval_use_BDD:
                    for i in range(1, len(self.auteurvar2)):
                        print(self.auteurvar2[i].get())
                        print(self.fromvar2[i].get())
                        print(self.tovar2[i].get())
                        print(self.supposees[i].get())
                        categories_supposees.append(self.supposees[i].get())
                else:
                    self.id_eval_set = [[(evalauteur1var.get(), k) for k in range(evalfrom1var.get(), evalto1var.get())], [(evalauteur2var.get(), k) for k in range(evalfrom2var.get(), evalto2var.get())]]
                    for i in range(1, len(self.auteurvar2)):
                        print(self.auteurvar2[i].get())
                        print(self.fromvar2[i].get())
                        print(self.tovar2[i].get())
                        print(self.supposees[i].get())
                        categories_supposees.append(self.supposees[i].get())
                        self.id_eval_set.append([(self.auteurvar2[i].get(), k) for k in range(self.fromvar2[i].get(), self.tovar2[i].get())])

                print('Evaluation Set: ', self.id_eval_set)

                if full_textvar.get() == 'True':
                    P = Probleme(self.id_training_set, categories, self.id_eval_set, categories_supposees, taillevar.get(),
                                 analyseur, self.classifieur, self.langue, full_text=True)
                else:
                    P = Probleme(self.id_training_set, categories, self.id_eval_set, categories_supposees, taillevar.get(),
                                 analyseur, self.classifieur, self.langue, full_text=False)

                if equilibragevar.get() == 'True':
                    if equilibrage_evalvar.get() == 'True':
                        P.creer_textes(equilibrage=True, equilibrage_eval=True)
                    else:
                        P.creer_textes(equilibrage=True, equilibrage_eval=False)
                else:
                    if equilibrage_evalvar.get() == 'True':
                        P.creer_textes(equilibrage=False, equilibrage_eval=True)
                    else:
                        P.creer_textes(equilibrage=False, equilibrage_eval=False)

                if normalisationvar.get() == 'True':
                    P.analyser(normalisation=True)
                else:
                    P.analyser(normalisation=False)

                P.appliquer_classifieur()
                P.afficher()
                if utiliser_textes_trainingvar.get() == 'True':
                    P.interpreter(utiliser_textes_training=True)
                else:
                    P.interpreter(utiliser_textes_training=False)

                P.afficher_graphique()
                f = time()
                print()
                print("Temps d'exécution : " + str(f - d) + "s")

        ttk.Button(frame1, text='Okay', command=run_classification).grid(column=7, row=30, sticky=(E, S), padx=5,
                                                                         pady=30)

        def close_classification():
            if messagebox.askyesno('QUIT', 'Are you sure to close it?'):
                root.destroy()

        ttk.Button(frame1, text='Cancel', command=close_classification).grid(column=8, row=30, sticky=(E, S), padx=5,
                                                                             pady=30)













        """notebook Verification"""

        """vertical before horizontal, otherwise false, I don't know why"""
        ttk.Separator(frame2, orient=VERTICAL).grid(column=3, rowspan=6, sticky="sn", padx=0, pady=10)
        ttk.Separator(frame2, orient=HORIZONTAL).grid(columnspan=7, row=6, sticky="ew", padx=20, pady=20)

        self.Vlangue = "fr"

        def VsetLangue(event):
            if VforLangue.get() == 'Anglais':
                self.Vlangue = "en"
            elif VforLangue.get() == 'Francais':
                self.Vlangue = "fr"
            elif VforLangue.get() == 'Allemand':
                self.Vlangue = "de"
            elif VforLangue.get() == 'Espagnol':
                self.Vlangue = "es"
            elif VforLangue.get() == 'Chinois':
                self.Vlangue = "zh"

        ttk.Label(frame2, text="Langue").grid(column=0, row=0, padx=10, pady=10)
        VLanguevar = StringVar()
        VforLangue = ttk.Combobox(frame2, textvariable=VLanguevar)
        VforLangue['values'] = ('Anglais', 'Francais', 'Allemand', 'Espagnol', 'Chinois')
        VforLangue.bind('<<ComboboxSelected>>', VsetLangue)
        VforLangue.grid(column=1, row=0)

        self.verificateur = ''

        def setVerificateur(event):
            if forVerificateur.get() == 'Unmasking':
                self.verificateur = Unmasking()
            elif forVerificateur.get() == 'Similarity':
                self.verificateur = Similarity()

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

        self.VA = []

        def VcallFreq_Gram():
            if VFreq_Gramvar.get() == 'oui':
                if self.VA.count(Freq_Gram) == 0:
                    self.VA.append(Freq_Gram)
                    print('add Freq_Gram')
            else:
                self.VA.remove(Freq_Gram)
                print('remove Freq_Gram')

        VFreq_Gramvar = StringVar()
        Checkbutton(frame2, text='Freq_Gram', variable=VFreq_Gramvar, command=VcallFreq_Gram, onvalue='oui',
                    offvalue='non').grid(column=5, row=1, padx=10, pady=10)

        self.VMarkov_Gram_saut = 0
        self.VMarkov_Gram_emondage = ''

        def VcallMarkov_Gram():
            if VMarkov_Gramvar.get() == 'oui':
                if self.VA.count(Markov_Gram) == 0:
                    # VMarkov_Gram_root = Tk()
                    # VMarkov_Gram_root.title('choose the saut of Markov_Gram')
                    # VMarkov_Gram_frame = ttk.Frame(VMarkov_Gram_root, padding='10 10 10 10', borderwidth='3',
                    #                                relief='flat')
                    # VMarkov_Gram_frame.grid(column=0, row=0, sticky=(N, W, E, S))
                    # VMarkov_Gram_frame.columnconfigure(0, weight=1)
                    # VMarkov_Gram_frame.rowconfigure(0, weight=1)
                    #
                    # ttk.Label(VMarkov_Gram_frame, text='Saut').grid(column=0, row=0)
                    # VMarkov_Gram_sautvar = IntVar()
                    # ttk.Entry(VMarkov_Gram_frame, textvariable=VMarkov_Gram_sautvar).grid(column=1, row=0, padx=5)
                    #
                    # ttk.Label(VMarkov_Gram_frame, text="Emondage").grid(column=0, row=1, padx=10, pady=10)
                    # VMarkov_Gram_emondagevar = StringVar()
                    # true = Radiobutton(VMarkov_Gram_frame, text='True', variable=VMarkov_Gram_emondagevar, value='True')
                    # true.grid(column=1, row=1)
                    # false = Radiobutton(VMarkov_Gram_frame, text='False', variable=VMarkov_Gram_emondagevar,
                    #                     value='False')
                    # false.grid(column=1, row=2)
                    #
                    # def VMarkov_Gram_Okay():
                    #     self.VMarkov_Gram_saut = VMarkov_Gram_sautvar.get()
                    #     if VMarkov_Gram_emondagevar.get() == 'True':
                    #         self.VMarkov_Gram_emondage = True
                    #     else:
                    #         self.VMarkov_Gram_emondage = False
                    #     VMarkov_Gram_root.destroy()
                    #
                    # ttk.Button(VMarkov_Gram_frame, text='Okay', command=VMarkov_Gram_Okay).grid(column=2, row=0, padx=5)
                    #
                    # def VMarkov_Gram_Cancel():
                    #     VMarkov_Gram_root.destroy()
                    #
                    # ttk.Button(VMarkov_Gram_frame, text='Cancel', command=VMarkov_Gram_Cancel).grid(column=3, row=0,
                    #                                                                                padx=5)

                    self.VMarkov_Gram_saut = simpledialog.askinteger("Insert the saut of Markov_Gram", "Saut")
                    Vemondage = simpledialog.askstring("Insert the emondage of Markov_Gram", "Emondage: True/False?")
                    if Vemondage == "True":
                        self.VMarkov_Gram_emondage = True
                    else:
                        self.VMarkov_Gram_emondage = False
                    self.VA.append(Markov_Gram)
                    print('add Markov_Gram')
                    # VMarkov_Gram_root.mainloop()
            else:
                self.VMarkov_Gram_saut = 0
                self.VMarkov_Gram_emondage = ''
                self.VA.remove(Markov_Gram)
                print('remove Markov_Gram')

        VMarkov_Gramvar = StringVar()
        Checkbutton(frame2, text='Markov_Gram', variable=VMarkov_Gramvar, command=VcallMarkov_Gram, onvalue='oui',
                    offvalue='non').grid(column=5, row=2, padx=10, pady=10)

        self.VFreq_Ngrammes_n = 0

        def VcallFreq_Ngrammes():
            if VFreq_Ngrammesvar.get() == 'oui':
                if self.VA.count(Freq_Ngrammes) == 0:
                    # VFreq_Ngrammes_root = Tk()
                    # VFreq_Ngrammes_root.title('choose the n of Freq_Ngrammes')
                    # VFreq_Ngrammes_frame = ttk.Frame(VFreq_Ngrammes_root, padding='10 10 10 10', borderwidth='3',
                    #                                  relief='flat')
                    # VFreq_Ngrammes_frame.grid(column=0, row=0, sticky=(N, W, E, S))
                    # VFreq_Ngrammes_frame.columnconfigure(0, weight=1)
                    # VFreq_Ngrammes_frame.rowconfigure(0, weight=1)
                    # ttk.Label(VFreq_Ngrammes_frame, text='N').grid(column=0, row=0)
                    # VFreq_Ngrammes_nvar = IntVar()
                    # ttk.Entry(VFreq_Ngrammes_root, textvariable=VFreq_Ngrammes_nvar).grid(column=1, row=0, padx=5)
                    #
                    # def VFreq_Ngrammes_Okay():
                    #     self.VFreq_Ngrammes_n = VFreq_Ngrammes_nvar.get()
                    #     VFreq_Ngrammes_root.destroy()
                    #
                    # ttk.Button(VFreq_Ngrammes_root, text='Okay', command=VFreq_Ngrammes_Okay).grid(column=2, row=0,
                    #                                                                                padx=5)
                    #
                    # def VFreq_Ngrammes_Cancel():
                    #     VFreq_Ngrammes_root.destroy()
                    #
                    # ttk.Button(VFreq_Ngrammes_root, text='Cancel', command=VFreq_Ngrammes_Cancel).grid(column=3, row=0,
                    #                                                                                    padx=5)

                    self.VFreq_Ngrammes_n = simpledialog.askinteger("Insert the n of Freq_Ngrammes", "n")
                    self.VA.append(Freq_Ngrammes)
                    print('add Freq_Ngrammes')
                    # VFreq_Ngrammes_root.mainloop()
            else:
                self.VFreq_Ngrammes_n = 0
                self.VA.remove(Freq_Ngrammes)
                print('remove Freq_Ngrammes')

        VFreq_Ngrammesvar = StringVar()
        Checkbutton(frame2, text='Freq_Ngrammes', variable=VFreq_Ngrammesvar, command=VcallFreq_Ngrammes, onvalue='oui',
                    offvalue='non').grid(column=5, row=3, padx=10, pady=10)


        def VcallMarkov_Lettres():
            if VMarkov_Lettresvar.get() == 'oui':
                if self.VA.count(Markov_Lettres) == 0:
                    self.VA.append(Markov_Lettres)
                    print('add Markov_Lettres')
            else:
                self.VA.remove(Markov_Lettres)
                print('remove Markov_Lettres')

        VMarkov_Lettresvar = StringVar()
        Checkbutton(frame2, text='Markov_Lettres', variable=VMarkov_Lettresvar, command=VcallMarkov_Lettres,
                    onvalue='oui', offvalue='non').grid(column=5, row=4, padx=10, pady=10)


        def VcallFreq_Ponct():
            if VFreq_Ponctvar.get() == 'oui':
                if self.VA.count(Freq_Ponct) == 0:
                    self.VA.append(Freq_Ponct)
                    print('add Freq_Ponct')
            else:
                self.VA.remove(Freq_Ponct)
                print('remove Freq_Ponct')

        VFreq_Ponctvar = StringVar()
        Checkbutton(frame2, text='Freq_Ponct', variable=VFreq_Ponctvar, command=VcallFreq_Ponct, onvalue='oui',
                    offvalue='non').grid(column=5, row=5, padx=10, pady=10)


        def VcallLongueur_Phrases():
            if VLongueur_Phrasesvar.get() == 'oui':
                if self.VA.count(Longueur_Phrases) == 0:
                    self.VA.append(Longueur_Phrases)
                    print('add Longueur_Phrases')
            else:
                self.VA.remove(Longueur_Phrases)
                print('remove Longueur_Phrases')

        VLongueur_Phrasesvar = StringVar()
        Checkbutton(frame2, text='Longueur_Phrases', variable=VLongueur_Phrasesvar, command=VcallLongueur_Phrases,
                    onvalue='oui', offvalue='non').grid(column=6, row=1, padx=10, pady=10)

        self.VComplexite_Grammaticale_saut = 0

        def VcallComplexite_Grammaticale():
            if VComplexite_Grammaticalevar.get() == 'oui':
                if self.VA.count(Complexite_Grammaticale) == 0:
                    # VComplexite_Grammaticale_root = Tk()
                    # VComplexite_Grammaticale_root.title('choose the saut of Complexite_Grammaticale')
                    # VComplexite_Grammaticale_frame = ttk.Frame(VComplexite_Grammaticale_root, padding='10 10 10 10',
                    #                                            borderwidth='3', relief='flat')
                    # VComplexite_Grammaticale_frame.grid(column=0, row=0, sticky=(N, W, E, S))
                    # VComplexite_Grammaticale_frame.columnconfigure(0, weight=1)
                    # VComplexite_Grammaticale_frame.rowconfigure(0, weight=1)
                    # ttk.Label(VComplexite_Grammaticale_frame, text='Saut').grid(column=0, row=0)
                    # VComplexite_Grammaticale_sautvar = IntVar()
                    # ttk.Entry(VComplexite_Grammaticale_root, textvariable=VComplexite_Grammaticale_sautvar).grid(
                    #     column=1, row=0, padx=5)
                    #
                    # def VComplexite_Grammaticale_Okay():
                    #     self.VComplexite_Grammaticale_saut = VComplexite_Grammaticale_sautvar.get()
                    #     VComplexite_Grammaticale_root.destroy()
                    #
                    # ttk.Button(VComplexite_Grammaticale_root, text='Okay', command=VComplexite_Grammaticale_Okay).grid(
                    #     column=2, row=0, padx=5)
                    #
                    # def VComplexite_Grammaticale_Cancel():
                    #     VComplexite_Grammaticale_root.destroy()
                    #
                    # ttk.Button(VComplexite_Grammaticale_root, text='Cancel',
                    #            command=VComplexite_Grammaticale_Cancel).grid(column=3, row=0, padx=5)

                    self.VComplexite_Grammaticale_saut = simpledialog.askinteger(
                        "Insert the saut of Complexite_Grammaticale", "Saut")
                    self.VA.append(Complexite_Grammaticale)
                    print('add Complexite_Grammaticale')
                    # VComplexite_Grammaticale_root.mainloop()
            else:
                self.VComplexite_Grammaticale_saut = 0
                self.VA.remove(Complexite_Grammaticale)
                print('remove Complexite_Grammaticale')

        VComplexite_Grammaticalevar = StringVar()
        Checkbutton(frame2, text='Complexite_Grammaticale', variable=VComplexite_Grammaticalevar,
                    command=VcallComplexite_Grammaticale, onvalue='oui', offvalue='non').grid(column=6, row=2, padx=10,
                                                                                              pady=10)


        def VcallComplexite_Vocabulaire():
            if VComplexite_Vocabulairevar.get() == 'oui':
                if self.VA.count(Complexite_Vocabulaire) == 0:
                    self.VA.append(Complexite_Vocabulaire)
                    print('add Complexite_Vocabulaire')
            else:
                self.VA.remove(Complexite_Vocabulaire)
                print('remove Complexite_Vocabulaire')

        VComplexite_Vocabulairevar = StringVar()
        Checkbutton(frame2, text='Complexite_Vocabulaire', variable=VComplexite_Vocabulairevar,
                    command=VcallComplexite_Vocabulaire, onvalue='oui', offvalue='non').grid(column=6, row=3, padx=10,
                                                                                             pady=10)


        def VcallFreq_Stopwords():
            if VFreq_Stopwordsvar.get() == 'oui':
                if self.VA.count(Freq_Stopwords) == 0:
                    self.VA.append(Freq_Stopwords)
                    print('add Freq_Stopwords')
            else:
                self.VA.remove(Freq_Stopwords)
                print('remove Freq_Stopwords')

        VFreq_Stopwordsvar = StringVar()
        Checkbutton(frame2, text='Freq_Stopwords', variable=VFreq_Stopwordsvar, command=VcallFreq_Stopwords,
                    onvalue='oui', offvalue='non').grid(column=6, row=4, padx=10, pady=10)

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

        self.Va1 = 0
        self.Vauteurvar1 = ['']
        self.Vfromvar1 = [0]
        self.Vtovar1 = [0]
        self.Vbases = ['']

        def VAjouter1():
            if self.Va1 < 2:
                temp1 = self.Va1 + 1
                self.Va1 = temp1
                labelauteur = ttk.Label(frame2, text='Auteur')
                labelauteur.grid(column=1, row=9 + self.Va1, padx=10, pady=10)
                self.Vauteurvar1.append('')
                self.Vauteurvar1[self.Va1] = StringVar()
                entryauteur = ttk.Entry(frame2, textvariable=self.Vauteurvar1[self.Va1])
                entryauteur.grid(column=2, row=9 + self.Va1)
                labelfrom = ttk.Label(frame2, text='from')
                labelfrom.grid(column=3, row=9 + self.Va1, padx=10, pady=10)
                self.Vfromvar1.append(0)
                self.Vfromvar1[self.Va1] = IntVar()
                entryfrom = ttk.Entry(frame2, textvariable=self.Vfromvar1[self.Va1])
                entryfrom.grid(column=4, row=9 + self.Va1)
                labelto = ttk.Label(frame2, text='to')
                labelto.grid(column=5, row=9 + self.Va1, padx=10, pady=10)
                self.Vtovar1.append(0)
                self.Vtovar1[self.Va1] = IntVar()
                entryto = ttk.Entry(frame2, textvariable=self.Vtovar1[self.Va1])
                entryto.grid(column=6, row=9 + self.Va1)
                self.Vbases.append('')
                self.Vbases[self.Va1] = StringVar()
                auteurofcategories = ttk.Entry(frame2, textvariable=self.Vbases[self.Va1])
                auteurofcategories.grid(column=3 + self.Va1, row=14)

                def VSupprimer1():
                    labelauteur.destroy()
                    entryauteur.destroy()
                    labelfrom.destroy()
                    entryfrom.destroy()
                    labelto.destroy()
                    entryto.destroy()
                    auteurofcategories.destroy()
                    Vbuttonsupprimer1.destroy()
                    del self.Vauteurvar1[self.Va1]
                    del self.Vfromvar1[self.Va1]
                    del self.Vtovar1[self.Va1]
                    del self.Vbases[self.Va1]
                    temp1 = self.Va1 - 1
                    self.Va1 = temp1

                Vbuttonsupprimer1 = ttk.Button(frame2, text='Supprimer', command=VSupprimer1)
                Vbuttonsupprimer1.grid(column=0, row=9 + self.Va1)
            else:
                messagebox.showerror('ERROR!', 'Trop d\'auteurs à training!')

        ttk.Button(frame2, text='Ajouter', command=VAjouter1).grid(column=0, row=9)

        ttk.Label(frame2, text='categories_base').grid(column=1, row=14, padx=10, pady=10)
        Vbase1 = StringVar()
        ttk.Entry(frame2, textvariable=Vbase1).grid(column=2, row=14)
        Vbase2 = StringVar()
        ttk.Entry(frame2, textvariable=Vbase2).grid(column=3, row=14)

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

        self.Va2 = 0
        self.Vauteurvar2 = ['']
        self.Vfromvar2 = [0]
        self.Vtovar2 = [0]
        self.Vcalibrages = ['']

        def VAjouter2():
            if self.Va2 < 2:
                temp2 = self.Va2 + 1
                self.Va2 = temp2
                labelauteur = ttk.Label(frame2, text='Auteur')
                labelauteur.grid(column=1, row=16 + self.Va2, padx=10, pady=10)
                self.Vauteurvar2.append('')
                self.Vauteurvar2[self.Va2] = StringVar()
                entryauteur = ttk.Entry(frame2, textvariable=self.Vauteurvar2[self.Va2])
                entryauteur.grid(column=2, row=16 + self.Va2)
                labelfrom = ttk.Label(frame2, text='from')
                labelfrom.grid(column=3, row=16 + self.Va2, padx=10, pady=10)
                self.Vfromvar2.append(0)
                self.Vfromvar2[self.Va2] = IntVar()
                entryfrom = ttk.Entry(frame2, textvariable=self.Vfromvar2[self.Va2])
                entryfrom.grid(column=4, row=16 + self.Va2)
                labelto = ttk.Label(frame2, text='to')
                labelto.grid(column=5, row=16 + self.Va2, padx=10, pady=10)
                self.Vtovar2.append(0)
                self.Vtovar2[self.Va2] = IntVar()
                entryto = ttk.Entry(frame2, textvariable=self.Vtovar2[self.Va2])
                entryto.grid(column=6, row=16 + self.Va2)
                self.Vcalibrages.append('')
                self.Vcalibrages[self.Va2] = StringVar()
                auteurofcategories = ttk.Entry(frame2, textvariable=self.Vcalibrages[self.Va2])
                auteurofcategories.grid(column=3 + self.Va2, row=21)

                def VSupprimer2():
                    labelauteur.destroy()
                    entryauteur.destroy()
                    labelfrom.destroy()
                    entryfrom.destroy()
                    labelto.destroy()
                    entryto.destroy()
                    auteurofcategories.destroy()
                    Vbuttonsupprimer2.destroy()
                    del self.Vauteurvar2[self.Va2]
                    del self.Vfromvar2[self.Va2]
                    del self.Vtovar2[self.Va2]
                    del self.Vcalibrages[self.Va2]
                    temp2 = self.Va2 - 1
                    self.Va2 = temp2

                Vbuttonsupprimer2 = ttk.Button(frame2, text='Supprimer', command=VSupprimer2)
                Vbuttonsupprimer2.grid(column=0, row=16 + self.Va2)
            else:
                messagebox.showerror('ERROR!', 'Trop d\'auteurs à evaluer!')

        ttk.Button(frame2, text='Ajouter', command=VAjouter2).grid(column=0, row=16)

        ttk.Label(frame2, text='categories_calibrage').grid(column=1, row=21, padx=10, pady=10)
        Vcalibrage1 = StringVar()
        ttk.Entry(frame2, textvariable=Vcalibrage1).grid(column=2, row=21)
        Vcalibrage2 = StringVar()
        ttk.Entry(frame2, textvariable=Vcalibrage2).grid(column=3, row=21)

        ttk.Label(frame2, text='id_oeuvres_disputees').grid(column=0, row=22, padx=10, pady=10)
        ttk.Label(frame2, text='Auteur').grid(column=1, row=22, padx=10, pady=10)
        Vdisputee_auteur1var = StringVar()
        ttk.Entry(frame2, textvariable=Vdisputee_auteur1var).grid(column=2, row=22)
        ttk.Label(frame2, text='from').grid(column=3, row=22, padx=60, pady=10)
        Vdisputee_from1var = IntVar()
        ttk.Entry(frame2, textvariable=Vdisputee_from1var).grid(column=4, row=22)
        ttk.Label(frame2, text='to').grid(column=5, row=22, padx=60, pady=10)
        Vdisputee_to1var = IntVar()
        ttk.Entry(frame2, textvariable=Vdisputee_to1var).grid(column=6, row=22)
        ttk.Label(frame2, text='Auteur').grid(column=1, row=23, padx=10, pady=10)
        Vdisputee_auteur2var = StringVar()
        ttk.Entry(frame2, textvariable=Vdisputee_auteur2var).grid(column=2, row=23)
        ttk.Label(frame2, text='from').grid(column=3, row=23, padx=60, pady=10)
        Vdisputee_from2var = IntVar()
        ttk.Entry(frame2, textvariable=Vdisputee_from2var).grid(column=4, row=23)
        ttk.Label(frame2, text='to').grid(column=5, row=23, padx=60, pady=10)
        Vdisputee_to2var = IntVar()
        ttk.Entry(frame2, textvariable=Vdisputee_to2var).grid(column=6, row=23)

        self.Va3 = 0
        self.Vauteurvar3 = ['']
        self.Vfromvar3 = [0]
        self.Vtovar3 = [0]
        self.Vdisputees = ['']

        def VAjouter3():
            if self.Va3 < 2:
                temp3 = self.Va3 + 1
                self.Va3 = temp3
                labelauteur = ttk.Label(frame2, text='Auteur')
                labelauteur.grid(column=1, row=23 + self.Va3, padx=10, pady=10)
                self.Vauteurvar3.append('')
                self.Vauteurvar3[self.Va3] = StringVar()
                entryauteur = ttk.Entry(frame2, textvariable=self.Vauteurvar3[self.Va3])
                entryauteur.grid(column=2, row=23 + self.Va3)
                labelfrom = ttk.Label(frame2, text='from')
                labelfrom.grid(column=3, row=23 + self.Va3, padx=10, pady=10)
                self.Vfromvar3.append(0)
                self.Vfromvar3[self.Va3] = IntVar()
                entryfrom = ttk.Entry(frame2, textvariable=self.Vfromvar3[self.Va3])
                entryfrom.grid(column=4, row=23 + self.Va3)
                labelto = ttk.Label(frame2, text='to')
                labelto.grid(column=5, row=23 + self.Va3, padx=10, pady=10)
                self.Vtovar3.append(0)
                self.Vtovar3[self.Va3] = IntVar()
                entryto = ttk.Entry(frame2, textvariable=self.Vtovar3[self.Va3])
                entryto.grid(column=6, row=23 + self.Va3)
                self.Vdisputees.append('')
                self.Vdisputees[self.Va3] = StringVar()
                auteurofcategories = ttk.Entry(frame2, textvariable=self.Vdisputees[self.Va3])
                auteurofcategories.grid(column=3 + self.Va3, row=28)

                def VSupprimer3():
                    labelauteur.destroy()
                    entryauteur.destroy()
                    labelfrom.destroy()
                    entryfrom.destroy()
                    labelto.destroy()
                    entryto.destroy()
                    auteurofcategories.destroy()
                    Vbuttonsupprimer3.destroy()
                    del self.Vauteurvar3[self.Va3]
                    del self.Vfromvar3[self.Va3]
                    del self.Vtovar3[self.Va3]
                    del self.Vdisputees[self.Va3]
                    temp3 = self.Va3 - 1
                    self.Va3 = temp3

                Vbuttonsupprimer3 = ttk.Button(frame2, text='Supprimer', command=VSupprimer3)
                Vbuttonsupprimer3.grid(column=0, row=23 + self.Va3)
            else:
                messagebox.showerror('ERROR!', 'Trop d\'auteurs à evaluer!')

        ttk.Button(frame2, text='Ajouter', command=VAjouter3).grid(column=0, row=23)

        ttk.Label(frame2, text='categories_disputees').grid(column=1, row=28, padx=10, pady=10)
        Vdisputee1 = StringVar()
        ttk.Entry(frame2, textvariable=Vdisputee1).grid(column=2, row=28)
        Vdisputee2 = StringVar()
        ttk.Entry(frame2, textvariable=Vdisputee2).grid(column=3, row=28)

        """cette fonction reset n'inclut pas la fonction supprimer. Donc il faut supprimer ce qu'on a ajouté manuellemnt et puis reset."""

        def reset_verification():
            if messagebox.askyesno('Confirmation!', 'Are you sure to reset all? You will lose all your choices.'):
                VLanguevar.set('')
                self.Vlangue = ''
                Verificateurvar.set('')
                self.verificateur = ''
                Vtaillevar.set(0)
                Vfull_textvar.set('')
                Vnormalisationvar.set('')
                VFreq_Gramvar.set('')
                VMarkov_Gramvar.set('')
                self.VMarkov_Gram_saut = 0
                self.VMarkov_Gram_emondage = ''
                VFreq_Ngrammesvar.set('')
                self.VFreq_Ngrammes_n = 0
                VMarkov_Lettresvar.set('')
                VFreq_Ponctvar.set('')
                VLongueur_Phrasesvar.set('')
                VComplexite_Grammaticalevar.set('')
                self.VComplexite_Grammaticale_saut = 0
                VComplexite_Vocabulairevar.set('')
                VFreq_Stopwordsvar.set('')
                self.VA.clear()
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
                Vdisputee_auteur1var.set('')
                Vdisputee_from1var.set(0)
                Vdisputee_to1var.set(0)
                Vdisputee_auteur2var.set('')
                Vdisputee_from2var.set(0)
                Vdisputee_to2var.set(0)
                Vbase1.set('')
                Vbase2.set('')
                Vcalibrage1.set('')
                Vcalibrage2.set('')
                Vdisputee1.set('')
                Vdisputee2.set('')
                self.id_oeuvres_base = []
                self.id_oeuvres_calibrage = []
                self.id_oeuvres_disputees = []
                self.base_use_BDD = False
                self.calibrage_use_BDD = False
                self.disputees_use_BDD = False

        ttk.Button(frame2, text='Reset', command=reset_verification).grid(column=6, row=30, sticky=(E, S), padx=5,
                                                                          pady=30)

        self.id_oeuvres_base = []
        self.id_oeuvres_calibrage = []
        self.id_oeuvres_disputees = []
        self.base_use_BDD = False
        self.calibrage_use_BDD = False
        self.disputees_use_BDD = False

        def run_verification():
            if messagebox.askyesno('Confirmation!', 'Are you sure to run it?'):
                Vliste_fonctions = []
                Vnom_analyseurs = None
                if self.VA.count(Freq_Gram) != 0:
                    Vliste_fonctions.append(Freq_Gram(self.Vlangue))
                    if Vnom_analyseurs == None or Vnom_analyseurs == 'Grammaire':
                        Vnom_analyseurs = 'Grammaire'
                    else:
                        Vnom_analyseurs = 'Tout'
                if self.VA.count(Markov_Gram) != 0:
                    Vliste_fonctions.append(
                        Markov_Gram(self.Vlangue, saut=self.VMarkov_Gram_saut, emondage=self.VMarkov_Gram_emondage))
                    if Vnom_analyseurs == None or Vnom_analyseurs == 'Grammaire':
                        Vnom_analyseurs = 'Grammaire'
                    else:
                        Vnom_analyseurs = 'Tout'
                if self.VA.count(Freq_Ngrammes) != 0:
                    Vliste_fonctions.append(Freq_Ngrammes(self.Vlangue, n=self.VFreq_Ngrammes_n))
                    if Vnom_analyseurs == None or Vnom_analyseurs == 'Lettres':
                        Vnom_analyseurs = 'Lettres'
                    else:
                        Vnom_analyseurs = 'Tout'
                if self.VA.count(Markov_Lettres) != 0:
                    Vliste_fonctions.append(Markov_Lettres(self.Vlangue))
                    if Vnom_analyseurs == None or Vnom_analyseurs == 'Lettres':
                        Vnom_analyseurs = 'Lettres'
                    else:
                        Vnom_analyseurs = 'Tout'
                if self.VA.count(Freq_Ponct) != 0:
                    Vliste_fonctions.append(Freq_Ponct(self.Vlangue))
                    if Vnom_analyseurs == None or Vnom_analyseurs == 'Ponctuation':
                        Vnom_analyseurs = 'Ponctuation'
                    else:
                        Vnom_analyseurs = 'Tout'
                if self.VA.count(Longueur_Phrases) != 0:
                    Vliste_fonctions.append(Longueur_Phrases())
                    if Vnom_analyseurs == None or Vnom_analyseurs == 'Ponctuation':
                        Vnom_analyseurs = 'Ponctuation'
                    else:
                        Vnom_analyseurs = 'Tout'
                if self.VA.count(Complexite_Grammaticale) != 0:
                    Vliste_fonctions.append(Complexite_Grammaticale(self.Vlangue, saut=self.VComplexite_Grammaticale_saut))
                    if Vnom_analyseurs == None or Vnom_analyseurs == 'Complexite':
                        Vnom_analyseurs = 'Complexite'
                    else:
                        Vnom_analyseurs = 'Tout'
                if self.VA.count(Complexite_Vocabulaire) != 0:
                    Vliste_fonctions.append(Complexite_Vocabulaire())
                    if Vnom_analyseurs == None or Vnom_analyseurs == 'Complexite':
                        Vnom_analyseurs = 'Complexite'
                    else:
                        Vnom_analyseurs = 'Tout'
                if self.VA.count(Freq_Stopwords) != 0:
                    Vliste_fonctions.append(Freq_Stopwords(self.Vlangue))
                    if Vnom_analyseurs == None or Vnom_analyseurs == 'Stopwords':
                        Vnom_analyseurs = 'Stopwords'
                    else:
                        Vnom_analyseurs = 'Tout'
                analyseur = Analyseur(Vnom_analyseurs, Vliste_fonctions)

                categories_base = [Vbase1.get()] + [Vbase2.get()]
                # categories_base = ["categorie1"] + ["categorie2"]
                if self.base_use_BDD:
                    for i in range(1, len(self.Vauteurvar1)):
                        print(self.Vauteurvar1[i].get())
                        print(self.Vfromvar1[i].get())
                        print(self.Vtovar1[i].get())
                        print(self.Vbases[i].get())
                        categories_base.append(self.Vbases[i].get())
                else:
                    self.id_oeuvres_base = [[(Vbase_auteur1var.get(), k) for k in range(Vbase_from1var.get(), Vbase_to1var.get())], [(Vbase_auteur2var.get(), k) for k in range(Vbase_from2var.get(), Vbase_to2var.get())]]
                    for i in range(1, len(self.Vauteurvar1)):
                        print(self.Vauteurvar1[i].get())
                        print(self.Vfromvar1[i].get())
                        print(self.Vtovar1[i].get())
                        print(self.Vbases[i].get())
                        categories_base.append(self.Vbases[i].get())
                        self.id_oeuvres_base.append([(self.Vauteurvar1[i].get(), k) for k in range(self.Vfromvar1[i].get(), self.Vtovar1[i].get())])


                categories_calibrage = [Vcalibrage1.get()] + [Vcalibrage2.get()]
                # categories_calibrage = ["categorie1"] + ["categorie2"]
                if self.calibrage_use_BDD:
                    for i in range(1, len(self.Vauteurvar2)):
                        print(self.Vauteurvar2[i].get())
                        print(self.Vfromvar2[i].get())
                        print(self.Vtovar2[i].get())
                        print(self.Vcalibrages[i].get())
                        categories_calibrage.append(self.Vcalibrages[i].get())
                else:
                    self.id_oeuvres_calibrage = [[(Vcalibrage_auteur1var.get(), k) for k in
                                                  range(Vcalibrage_from1var.get(), Vcalibrage_to1var.get())],
                                                 [(Vcalibrage_auteur2var.get(), k) for k in
                                                  range(Vcalibrage_from2var.get(), Vcalibrage_to2var.get())]]
                    for i in range(1, len(self.Vauteurvar2)):
                        print(self.Vauteurvar2[i].get())
                        print(self.Vfromvar2[i].get())
                        print(self.Vtovar2[i].get())
                        print(self.Vcalibrages[i].get())
                        categories_calibrage.append(self.Vcalibrages[i].get())
                        self.id_oeuvres_calibrage.append(
                            [(self.Vauteurvar2[i].get(), k) for k in
                             range(self.Vfromvar2[i].get(), self.Vtovar2[i].get())])

                categories_disputees = [Vdisputee1.get()] + [Vdisputee2.get()]
                # categories_disputees = ["categorie1"] + ["categorie2"]
                if self.disputees_use_BDD:
                    for i in range(1, len(self.Vauteurvar3)):
                        print(self.Vauteurvar3[i].get())
                        print(self.Vfromvar3[i].get())
                        print(self.Vtovar3[i].get())
                        print(self.Vdisputees[i].get())
                        categories_disputees.append(self.Vdisputees[i].get())
                else:
                    self.id_oeuvres_disputees = [[(Vdisputee_auteur1var.get(), k) for k in
                                                  range(Vdisputee_from1var.get(), Vdisputee_to1var.get())],
                                                 [(Vdisputee_auteur2var.get(), k) for k in
                                                  range(Vdisputee_from2var.get(), Vdisputee_to2var.get())]]
                    for i in range(1, len(self.Vauteurvar3)):
                        print(self.Vauteurvar3[i].get())
                        print(self.Vfromvar3[i].get())
                        print(self.Vtovar3[i].get())
                        print(self.Vdisputees[i].get())
                        categories_disputees.append(self.Vdisputees[i].get())
                        self.id_oeuvres_disputees.append(
                            [(self.Vauteurvar3[i].get(), k) for k in
                             range(self.Vfromvar3[i].get(), self.Vtovar3[i].get())])


                if Vfull_textvar.get() == 'True':
                    V = Verification(self.id_oeuvres_base, categories_base, self.id_oeuvres_calibrage, categories_calibrage,
                                     self.id_oeuvres_disputees, categories_disputees, Vtaillevar.get(), analyseur,
                                     self.verificateur, self.Vlangue, full_text=True)
                else:
                    V = Verification(self.id_oeuvres_base, categories_base, self.id_oeuvres_calibrage, categories_calibrage,
                                     self.id_oeuvres_disputees, categories_disputees, Vtaillevar.get(), analyseur,
                                     self.verificateur, self.Vlangue, full_text=False)

                V.creer_textes()

                if Vnormalisationvar.get() == 'True':
                    V.analyser(normalisation=True)
                else:
                    V.analyser(normalisation=False)

                V.appliquer_verificateur()

        ttk.Button(frame2, text='Okay', command=run_verification).grid(column=7, row=30, sticky=(E, S), padx=5, pady=30)

        def close_verification():
            if messagebox.askyesno('QUIT', 'Are you sure to close it?'):
                root.destroy()

        ttk.Button(frame2, text='Cancel', command=close_verification).grid(column=8, row=30, sticky=(E, S), padx=5,
                                                                           pady=30)












        """notebook About the database"""

        ttk.Separator(frame3, orient=VERTICAL).grid(column=5, rowspan=8, sticky="sn", padx=20, pady=10)
        ttk.Separator(frame3, orient=HORIZONTAL).grid(columnspan=9, row=8, sticky="ew", padx=20, pady=10)

        # fichier
        ttk.Label(frame3, text='Fichier').grid(column=0, row=0, padx=20, pady=10)
        fichiervar = StringVar()
        forFichier = ttk.Entry(frame3, textvariable=fichiervar)
        forFichier.grid(column=1, row=0)

        # nom
        ttk.Label(frame3, text='Nom').grid(column=0, row=1, padx=20, pady=10)
        nomvar = StringVar()
        forNom = ttk.Entry(frame3, textvariable=nomvar)
        forNom.grid(column=1, row=1)

        # genre
        self.genre = None

        def setGenre(event):
            self.genre = genrevar.get()

        ttk.Label(frame3, text='Genre').grid(column=0, row=2, padx=20, pady=10)
        genrevar = StringVar()
        forGenre = ttk.Combobox(frame3, textvariable=genrevar)
        forGenre['values'] = (
        'Roman', 'roman pour enfant', 'Nouvelles pour enfants', 'Nouvelles', 'traité historique', 'poésie')
        forGenre.bind('<<ComboboxSelected>>', setGenre)
        forGenre.grid(column=1, row=2)

        # auteur
        ttk.Label(frame3, text='Auteur').grid(column=0, row=3, padx=20, pady=10)
        auteurvar = StringVar()
        forAuteur = ttk.Entry(frame3, textvariable=auteurvar)
        forAuteur.grid(column=1, row=3)

        # langue
        self.DBlangue = None

        def DBsetLangue(event):
            self.DBlangue = DBforLangue.get()

        ttk.Label(frame3, text="Langue").grid(column=0, row=4, padx=20, pady=10)
        DBLanguevar = StringVar()
        DBforLangue = ttk.Combobox(frame3, textvariable=DBLanguevar)
        DBforLangue['values'] = ('English', 'French', 'Chinese')
        DBforLangue.bind('<<ComboboxSelected>>', DBsetLangue)
        DBforLangue.grid(column=1, row=4)

        # pays
        self.pays = None

        def setPays(event):
            self.pays = paysvar.get()

        ttk.Label(frame3, text='Pays').grid(column=0, row=5, padx=20, pady=10)
        paysvar = StringVar()
        forPays = ttk.Combobox(frame3, textvariable=paysvar)
        forPays['values'] = ('France', 'English', 'China', 'USA')
        forPays.bind('<<ComboboxSelected>>', setPays)
        forPays.grid(column=1, row=5)

        # corpus
        ttk.Label(frame3, text='Corpus').grid(column=0, row=6, padx=20, pady=10)
        corpusvar = StringVar()
        forCorpus = ttk.Entry(frame3, textvariable=corpusvar)
        forCorpus.grid(column=1, row=6)

        # commentaires
        ttk.Label(frame3, text='Commentaires').grid(column=0, row=7, padx=20, pady=10)
        commentairesvar = StringVar()
        forCommentaires = ttk.Entry(frame3, textvariable=commentairesvar)
        forCommentaires.grid(column=1, row=7)

        # annee
        ttk.Label(frame3, text='Annee').grid(column=2, row=0, padx=20, pady=10)
        ttk.Label(frame3, text='From').grid(column=3, row=0, padx=20, pady=10)
        annee_from1var = IntVar()
        ttk.Entry(frame3, textvariable=annee_from1var).grid(column=4, row=0)
        ttk.Label(frame3, text='To').grid(column=3, row=1, padx=20, pady=10)
        annee_to1var = IntVar()
        ttk.Entry(frame3, textvariable=annee_to1var).grid(column=4, row=1)

        # naissance
        ttk.Label(frame3, text='Naissance').grid(column=2, row=2, padx=20, pady=10)
        ttk.Label(frame3, text='From').grid(column=3, row=2, padx=20, pady=10)
        naissance_from1var = IntVar()
        ttk.Entry(frame3, textvariable=naissance_from1var).grid(column=4, row=2)
        ttk.Label(frame3, text='To').grid(column=3, row=3, padx=20, pady=10)
        naissance_to1var = IntVar()
        ttk.Entry(frame3, textvariable=naissance_to1var).grid(column=4, row=3)

        # sexe
        ttk.Label(frame3, text='Sexe').grid(column=2, row=4, padx=20, pady=10)
        sexevar = StringVar()
        forM = Radiobutton(frame3, text='', variable=sexevar, value='True')
        forM.grid(column=3, row=4)
        ttk.Label(frame3, text='Male').grid(column=4, row=4, padx=20, pady=10)
        forF = Radiobutton(frame3, text='', variable=sexevar, value='False')
        forF.grid(column=3, row=5)
        ttk.Label(frame3, text='Female').grid(column=4, row=5, padx=20, pady=10)

        def insert():
            if messagebox.askyesno('Confirmation!', 'Are you sure to insert this file?'):
                if annee_from1var.get() != annee_to1var.get():
                    messagebox.showerror('Error!', 'Wrong values for \'annee\'!')
                elif naissance_from1var.get() != naissance_to1var.get():
                    messagebox.showerror('Error!', 'Wrong values for \'naissance\'!')
                else:
                    fichier = fichiervar.get()
                    nom = nomvar.get()
                    annee = annee_from1var.get()
                    auteur = auteurvar.get()
                    naissance = naissance_from1var.get()
                    corpus = corpusvar.get()
                    commentaires = commentairesvar.get()
                    if sexevar.get() == 'True':
                        InsererFichier(fichier, nom, annee, self.genre, auteur, naissance, 'M', self.DBlangue, self.pays, corpus,
                                       commentaires)
                    else:
                        InsererFichier(fichier, nom, annee, self.genre, auteur, naissance, 'F', self.DBlangue, self.pays, corpus,
                                       commentaires)

        ttk.Button(frame3, text='Insert', command=insert).grid(column=4, row=6, padx=0, pady=10)

        def select():
            if messagebox.askyesno('Confirmation!', 'Are you sure to select those files?'):
                if fichiervar.get() == '':
                    fichier = None
                else:
                    fichier = fichiervar.get()
                if nomvar.get() == '':
                    nom = None
                else:
                    nom = nomvar.get()
                if annee_from1var.get() == 0:
                    annee_debut = None
                else:
                    annee_debut = annee_from1var.get()
                if annee_to1var.get() == 0:
                    annee_fin = None
                else:
                    annee_fin = annee_to1var.get()
                if auteurvar.get() == '':
                    auteur = None
                else:
                    auteur = auteurvar.get()
                if naissance_from1var.get() == 0:
                    naissance_debut = None
                else:
                    naissance_debut = naissance_from1var.get()
                if naissance_to1var.get() == 0:
                    naissance_fin = None
                else:
                    naissance_fin = naissance_to1var.get()
                if sexevar.get() == '':
                    sexe = None
                elif sexevar.get() == 'True':
                    sexe = 'M'
                else:
                    sexe = 'F'
                if corpusvar.get() == '':
                    corpus = None
                else:
                    corpus = corpusvar.get()
                table = SelectionnerFichiers(fichier, nom, annee_debut, annee_fin, self.genre, auteur, naissance_debut,
                                             naissance_fin, sexe, self.DBlangue, self.pays, corpus)
                lbox.delete(0, END)
                for i in range(1, len(table)):
                    ListBoxAdd(table[i])
                for i in range(0, len(table) - 1, 2):
                    lbox.itemconfigure(i, background='#f0f0ff')

        ttk.Button(frame3, text='Select', command=select).grid(column=4, row=7, padx=0, pady=10)

        # fichier
        ttk.Label(frame3, text='Fichier').grid(column=6, row=0, padx=20, pady=10)
        Mfichiervar = StringVar()
        MforFichier = ttk.Entry(frame3, textvariable=Mfichiervar)
        MforFichier.grid(column=7, row=0)

        # champ_modif
        ttk.Label(frame3, text='Field modified').grid(column=6, row=1, padx=20, pady=10)
        champ_modifvar = StringVar()
        forChamp_modif = ttk.Entry(frame3, textvariable=champ_modifvar)
        forChamp_modif.grid(column=7, row=1)

        # valeur_champ_modif
        ttk.Label(frame3, text='Value of field modified').grid(column=6, row=2, padx=20, pady=10)
        valeur_champ_modifvar = StringVar()
        forValeur_champ_modif = ttk.Entry(frame3, textvariable=valeur_champ_modifvar)
        forValeur_champ_modif.grid(column=7, row=2)

        def modify():
            if messagebox.askyesno('Confirmation!', 'Are you sure to modify this file?'):
                fichier = Mfichiervar.get()
                champ_modif = champ_modifvar.get()
                valeur_champ_modif = valeur_champ_modifvar.get()
                ModifierFichier(fichier, champ_modif, valeur_champ_modif)

        ttk.Button(frame3, text='Modify', command=modify).grid(column=7, row=3, padx=0, pady=10)

        # champ
        ttk.Label(frame3, text='Field').grid(column=6, row=4, padx=20, pady=10)
        champvar = StringVar()
        forChamp = ttk.Entry(frame3, textvariable=champvar)
        forChamp.grid(column=7, row=4)

        # valeur_champ
        ttk.Label(frame3, text='Value of field').grid(column=6, row=5, padx=20, pady=10)
        valeur_champvar = StringVar()
        forValeur_champ = ttk.Entry(frame3, textvariable=valeur_champvar)
        forValeur_champ.grid(column=7, row=5)

        def afficherFichier():
            if messagebox.askyesno('Confirmation!', 'Are you sure to list this file?'):
                champ = champvar.get()
                valeur_champ = valeur_champvar.get()
                table = AfficherFichier(champ, valeur_champ)
                lbox.delete(0, END)
                for i in range(1, len(table)):
                    ListBoxAdd(table[i])
                for i in range(0, len(table) - 1, 2):
                    lbox.itemconfigure(i, background='#f0f0ff')

        ttk.Button(frame3, text='List File', command=afficherFichier).grid(column=7, row=6, padx=0, pady=10)

        def afficherTable():
            if messagebox.askyesno('Confirmation!', 'Are you sure to list all files?'):
                table = AfficherTable()
                lbox.delete(0, END)
                for i in range(1, len(table)):
                    ListBoxAdd(table[i])
                for i in range(0, len(table) - 1, 2):
                    lbox.itemconfigure(i, background='#f0f0ff')

        ttk.Button(frame3, text='List Table', command=afficherTable).grid(column=7, row=7, padx=0, pady=10)

        def ListBoxAdd(string):
            lbox.insert(END, string)

        self.textList = []

        def addToList(event):
            self.textList = []
            indexs = lbox.curselection()
            for i in indexs:
                str = lbox.get(i).split(', ')[0].split(' : ')[1]
                strs = str.split('_')
                s = ""
                for j in range(0, len(strs) - 1):
                    s = s + strs[j] + "_"
                self.textList.append((s, int(strs[len(strs) - 1])))
            for k in range(0, len(self.textList)):
                print(self.textList[k])

        lbox = Listbox(frame3, selectmode=EXTENDED, height=20)
        lbox.grid(columnspan=8, row=9, rowspan=20, sticky=(N, S, E, W))
        lbox.bind('<Double-1>', addToList)

        def addToTraining():
            self.id_training_set = self.id_training_set + [self.textList]
            self.training_use_BDD = True
            print('Training Set: ', self.id_training_set)

        def addToEvaluation():
            self.id_eval_set = self.id_eval_set + [self.textList]
            self.eval_use_BDD = True
            print('Evaluation Set: ', self.id_eval_set)

        ttk.Label(frame3, text='Classification').grid(column=8, row=9, padx=20, pady=10)
        ttk.Button(frame3, text='To Training Set', command=addToTraining).grid(column=8, row=10, padx=20, pady=10)
        ttk.Button(frame3, text='To Evaluation Set', command=addToEvaluation).grid(column=8, row=11, padx=20, pady=10)

        def addToBase():
            self.id_oeuvres_base = self.id_oeuvres_base + [self.textList]
            self.base_use_BDD = True
            print('Base: ', self.id_oeuvres_base)

        def addToCalibrage():
            self.id_oeuvres_calibrage = self.id_oeuvres_calibrage + [self.textList]
            self.calibrage_use_BDD = True
            print('Calibrage: ', self.id_oeuvres_calibrage)

        def addToDisputees():
            self.id_oeuvres_disputees = self.id_oeuvres_disputees + [self.textList]
            self.disputees_use_BDD = True
            print('Disputees: ', self.id_oeuvres_disputees)

        ttk.Label(frame3, text='Verification').grid(column=8, row=12, padx=20, pady=10)
        ttk.Button(frame3, text='To base', command=addToBase).grid(column=8, row=13, padx=20, pady=10)
        ttk.Button(frame3, text='To calibrage', command=addToCalibrage).grid(column=8, row=14, padx=20, pady=10)
        ttk.Button(frame3, text='To disputees', command=addToDisputees).grid(column=8, row=15, padx=20, pady=10)

        def reset_database():
            if messagebox.askyesno('Confirmation!', 'Are you sure to reset all? You will lose all your choices.'):
                fichiervar.set('')
                nomvar.set('')
                genrevar.set('')
                auteurvar.set('')
                DBLanguevar.set('')
                paysvar.set('')
                corpusvar.set('')
                commentairesvar.set('')
                annee_from1var.set(0)
                annee_to1var.set(0)
                naissance_from1var.set(0)
                naissance_to1var.set(0)
                sexevar.set('')
                Mfichiervar.set('')
                champ_modifvar.set('')
                valeur_champ_modifvar.set('')
                champvar.set('')
                valeur_champvar.set('')
                self.genre = None
                self.DBlangue = None
                self.pays = None
                lbox.delete(0, END)
                self.textList = []
                self.training_use_BDD = False
                self.eval_use_BDD = False
                self.base_use_BDD = False
                self.calibrage_use_BDD = False
                self.disputees_use_BDD = False

        ttk.Button(frame3, text='Reset', command=reset_database).grid(column=8, row=20, padx=5, pady=10)

        def close_database():
            if messagebox.askyesno('QUIT', 'Are you sure to close it?'):
                root.destroy()

        ttk.Button(frame3, text='Cancel', command=close_database).grid(column=8, row=21, padx=5, pady=10)

    def build(self):
        self.root.mainloop()