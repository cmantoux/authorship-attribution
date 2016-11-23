# -*- coding: utf-8 -*-
from tkinter import *

class FenetreAffichage():
    
    def switch_theorique_concret(self):
        self.theorique = not self.theorique
        if self.theorique:
            self.switch['text'] = "Théorique"
        else:
            self.switch['text'] = "Résultat"
        self.repaint()
    
    def switch_points_enveloppe(self):
        self.is_enveloppe = not self.is_enveloppe
        self.repaint()
        
    def __init__(self, classes):
        self.height = 600
        self.width = 600
        
        self.classes = classes #[[objet_texte, auteur_presume]]
                
        #On regarde les coordonnées extrémales pour les normaliser
        self.xMin=0
        self.yMin=0
        self.xMax=0
        self.yMax=0
        for texte in classes:
            x = texte[0].vecteur[0]
            y = texte[0].vecteur[1]
            if x>self.xMax:
                self.xMax = x
            if x<self.xMin:
                self.xMin = x
            if y>self.yMax:
                self.yMax = y
            if y<self.yMin:
                self.yMin = y

        self.theorique = True
        self.is_enveloppe = False
        
        self.objets_dessines = []
        self.fenetre = fenetre = Tk()
        self.canvas = Canvas(fenetre, width = self.width, height = self.height, background="white")
        self.couleurs = {}
        self.switch=Button(self.fenetre,text="Résultat",command=self.switch_theorique_concret)
        
        self.type_dessin = "points"
    
    def repaint(self):
        if self.type_dessin=="points":
            for point in self.objets_dessines:
                self.canvas.delete(point)
            self.objets_dessines = []

            proportion = self.width / max(self.xMax - self.xMin, self.yMax - self.yMin) * 0.95
            for texte in self.classes:
                if self.theorique:
                    indice = texte[0].auteur
                else:
                    indice = texte[1]
                self.objets_dessines.append(self.canvas.create_oval(
                                                    (texte[0].vecteur[0]-self.xMin)*proportion+10,
                                                    (texte[0].vecteur[1]-self.yMin)*proportion+10,
                                                    (texte[0].vecteur[0]-self.xMin)*proportion+20,
                                                    (texte[0].vecteur[1]-self.yMin)*proportion+20,
                                                    fill=self.couleurs[indice]))
    
    def show(self):
        self.canvas.pack()
        
        all_couleurs = ["yellow", "red", "green", "blue", "black","purple",
                        "brown1", "gray", "cyan", "white", "royal blue", "dark violet"]

        proportion = self.width / max(self.xMax - self.xMin, self.yMax - self.yMin) * 0.95
        for texte in self.classes:
            #Remplissage du tableau des couleurs
            if not texte[0].auteur in self.couleurs.keys():
                self.couleurs[texte[0].auteur]=all_couleurs[len(self.couleurs.keys())%len(all_couleurs)]
            if not texte[1] in self.couleurs.keys():
                self.couleurs[texte[1]]=all_couleurs[len(self.couleurs.keys())%len(all_couleurs)]
            
            self.objets_dessines.append(self.canvas.create_oval(
                                                    (texte[0].vecteur[0]-self.xMin)*proportion+10,
                                                    (texte[0].vecteur[1]-self.yMin)*proportion+10,
                                                    (texte[0].vecteur[0]-self.xMin)*proportion+20,
                                                    (texte[0].vecteur[1]-self.yMin)*proportion+20,
                                                    fill=self.couleurs[texte[0].auteur]))

        
        self.switch.pack()

        label = Label(self.fenetre, text="Affichage des classes")
        label.pack()
        
        for key in self.couleurs.keys():
            frame = Frame(self.fenetre, borderwidth = 2)
            couleur_canvas = Canvas(frame, width = 20, height = 20, background=self.couleurs[key])
            couleur_canvas.pack(side=LEFT, padx = 3, pady = 3)
            couleur_label = Label(frame, text=key)
            couleur_label.pack(side=LEFT)
            frame.pack(side=LEFT)
        
        self.fenetre.mainloop()