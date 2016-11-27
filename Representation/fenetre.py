# -*- coding: utf-8 -*-
from tkinter import *
from scipy.spatial import ConvexHull
from Utilitaires.pca import pca


class FenetreAffichage:

    def switch_theorique_concret(self):
        self.theorique = not self.theorique
        if self.theorique:
            self.theorique_concret_switch['text'] = "Afficher le résultat du classifieur"
        else:
            self.theorique_concret_switch['text'] = "Afficher la position théorique"
        self.repaint()
    
    def switch_points_enveloppe(self):
        self.affiche_enveloppe = not self.affiche_enveloppe
        self.repaint()

    # Renvoie le numéro de l'auteur théorique
    def auteur_theorique(self, indice):
        return self.noms_auteurs_inverses[self.liste_textes[indice].auteur]

    # A partir de p_ref
    def auteur_concret(self, indice):
        res = 0
        for i in range(0, len(self.p[indice])):
            if self.p[indice][i] > self.p[indice][res]:
                res = i
        return res
        
    def __init__(self, liste_textes, p, p_ref, noms_auteurs, methode_reduction):
        self.height = 600
        self.width = 600

        self.liste_textes = liste_textes
        self.p = p
        self.p_ref = p_ref

        # Application de methode_reduction
        if methode_reduction == "pca":
            vecteurs = []
            for texte in self.liste_textes:
                vecteurs.append(texte.vecteur)
            vecteurs = pca(vecteurs)
            for i in range(len(self.liste_textes)):
                self.liste_textes[i].vecteur = vecteurs[i]

        # On regarde les coordonnées extrémales pour les normaliser
        self.xMin = 0
        self.yMin = 0
        self.xMax = 0
        self.yMax = 0
        for texte in liste_textes:
            x = texte.vecteur[0]
            y = texte.vecteur[1]
            if x > self.xMax:
                self.xMax = x
            if x < self.xMin:
                self.xMin = x
            if y > self.yMax:
                self.yMax = y
            if y < self.yMin:
                self.yMin = y

        self.noms_auteurs = noms_auteurs
        self.noms_auteurs_inverses = {}
        self.clusters_theoriques_indices = [[] for i in range(len(noms_auteurs))]  # permettra de calculer l'enveloppe convexe
        self.clusters_concrets_indices = [[] for i in range(len(noms_auteurs))]
        for i in range(len(self.noms_auteurs)):
            self.noms_auteurs_inverses[self.noms_auteurs[i]] = i
        for i in range(len(self.liste_textes)):
            self.clusters_theoriques_indices[self.auteur_theorique(i)].append(i)
            self.clusters_concrets_indices[self.auteur_concret(i)].append(i)

        proportion_x = self.width / (self.xMax - self.xMin) * 0.90
        proportion_y = self.height / (self.yMax - self.yMin) * 0.90
        self.points = []

        for texte in self.liste_textes:
            self.points.append([(texte.vecteur[0] - self.xMin) * proportion_x + 0.05 * (self.xMax - self.xMin) * proportion_x,
                               (texte.vecteur[1] - self.yMin) * proportion_y + 0.05*(self.yMax - self.yMin) * proportion_y])

        self.theorique = True
        self.affiche_enveloppe = False
        
        self.objets_dessines = []
        self.fenetre = fenetre = Tk()
        self.canvas = Canvas(fenetre, width=self.width, height=self.height, background="white")
        self.couleurs = ["yellow", "red", "green", "blue", "black", "purple",
                         "brown1", "gray", "cyan", "white", "royal blue", "dark violet"]

        self.theorique_concret_switch = Button(self.fenetre, text="Afficher le résultat du classifieur",
                                               command=self.switch_theorique_concret)
        self.enveloppe_switch = Checkbutton(self.fenetre, text="Afficher les enveloppes convexes",
                                               command=self.switch_points_enveloppe)

    def repaint(self):
        for objet in self.objets_dessines:
            self.canvas.delete(objet)
        self.objets_dessines = []

        for i in range(len(self.liste_textes)):
            if self.theorique:
                indice = self.auteur_theorique(i)
            else:
                indice = self.auteur_concret(i)
            r = 10.
            self.objets_dessines.append(self.canvas.create_oval(
                self.points[i][0] - r / 2, self.points[i][1] - r / 2,
                self.points[i][0] + r / 2, self.points[i][1] + r / 2,
                fill=self.couleurs[indice]))

        if self.affiche_enveloppe:
            if self.theorique:
                clusters = self.clusters_theoriques_indices
            else:
                clusters = self.clusters_concrets_indices
            for k in range(len(clusters)):
                hull = ConvexHull([self.points[i] for i in clusters[k]])
                self.objets_dessines.append(self.canvas.create_polygon(
                    [self.points[clusters[k][i]] for i in hull.vertices],
                    outline=self.couleurs[k], fill="", width=3))

    def build(self):
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.repaint()

        self.theorique_concret_switch.grid(row=1, column=0)
        self.enveloppe_switch.grid(row=1, column=1)

        frame_auteurs = Frame(self.fenetre, borderwidth=2)
        frame_clusters = Frame(self.fenetre, borderwidth=2)
        for i in range(len(self.noms_auteurs)):
            # Ajout à frame_auteurs
            couleur_canvas = Canvas(frame_auteurs, width=20, height=20, background=self.couleurs[i])
            couleur_canvas.pack(side=LEFT, padx=3, pady=3)
            couleur_label = Label(frame_auteurs, text=self.noms_auteurs[i].title())
            couleur_label.pack(side=LEFT)

            # Ajout à frame_clusters
            cluster_label = Label(frame_clusters, text="Cluster ")
            cluster_label.grid(row=i, column=0, columnspan=2)
            couleur__cluster = Canvas(frame_clusters, width=20, height=20, background=self.couleurs[i])
            couleur__cluster.grid(row=i, column=2)
            cluster_canvas = Canvas(frame_clusters, width=self.width-100, height=20, background="white")

            # nombres_auteurs[n] = nombre de textes de l'auteur n dans le cluster i
            nombres_auteurs = [0] * len(self.noms_auteurs)
            for k in self.clusters_concrets_indices[i]:
                nombres_auteurs[self.auteur_theorique(k)] += 1

            x = 0
            for k in range(len(nombres_auteurs)):
                x2 = x + (self.width-100) * nombres_auteurs[k] / len(self.clusters_concrets_indices[i])
                cluster_canvas.create_rectangle(x, 0, x2, 21, fill=self.couleurs[k])
                x = x2+1
            cluster_canvas.grid(row=i, column=3, columnspan=6)
        frame_auteurs.grid(row=3, column=0, columnspan=2, sticky=W)
        frame_clusters.grid(row=4, column=0, columnspan=2, sticky=W)

        self.fenetre.mainloop()
