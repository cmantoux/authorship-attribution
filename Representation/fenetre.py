# -*- coding: utf-8 -*-
from tkinter import *
from scipy.spatial import ConvexHull
from Utilitaires.pca import pca_matrice
import numpy as np


def nouvelles_matrices(training_set, p, p_ref, categories):
    nt = len(training_set)
    ne = p.shape[0]
    nc = len(categories)
    p2 = np.zeros((nt + ne, nc))
    p_ref2 = np.zeros((nt + ne, nc))
    for i in range(nt):
        t = training_set[i]
        j = categories.index(t.categorie)
        p2[i, j] = 1
        p_ref2[i, j] = 1
    for i in range(nt, nt + ne):
        for j in range(len(categories)):
            p2[i][j] = p[i - nt, j]
            p_ref2[i][j] = p_ref[i - nt, j]
    return p2, p_ref2, categories


class FenetreAffichage:

    def __init__(self, analyseur, classifieur, poids_composantes):
        self.analyseur = analyseur
        self.poids_composantes = poids_composantes
        self.height = 600
        self.width = 600
        self.liste_textes = classifieur.training_set + classifieur.eval_set
        self.p, self.p_ref, self.noms_auteurs = nouvelles_matrices(classifieur.training_set, classifieur.p,
                                                                   classifieur.p_ref, classifieur.categories)
        # Nombre de points à afficher
        self.n_points = len(self.liste_textes)
        self.dimension = len(self.liste_textes[0].vecteur)

        self.matrice_proportions = None
        self.coefficients_coordonnees = None  # Pondère les coordonnées les plus séparatrices
        self.vecteurs_originaux = []  # Contient les vecteurs des textes avant PCA

        # Création des clusters
        self.noms_auteurs_inverses = {}
        self.clusters_theoriques_indices = [[] for i in
                                            range(len(self.noms_auteurs))]  # permettra de calculer l'enveloppe convexe
        self.clusters_concrets_indices = [[] for i in range(len(self.noms_auteurs))]
        for i in range(len(self.noms_auteurs)):
            self.noms_auteurs_inverses[self.noms_auteurs[i]] = i
        for i in range(len(self.liste_textes)):
            self.clusters_theoriques_indices[self.auteur_theorique(i)].append(i)
            self.clusters_concrets_indices[self.auteur_concret(i)].append(i)

        # Application de methode_reduction
        vecteurs = []
        for texte in self.liste_textes:
            vecteurs.append(texte.vecteur)
            self.vecteurs_originaux.append(texte.vecteur)
        vecteurs, self.matrice_proportions = pca_matrice(vecteurs)

        # Création des variables du système de réévaluation des composantes

        # Méthode basée sur la fonction importance_composantes
        clusters_concrets_textes = []
        for cluster_indice in self.clusters_concrets_indices:
            cluster = []
            for indice in cluster_indice:
                cluster.append(self.liste_textes[indice])
            clusters_concrets_textes.append(cluster)

        # Tableau des indices des composantes vectorielles, triées par importance
        indices_coefficients_separateurs = self.tri_par_importance(range(0, self.dimension))
        nb_minimal_curseurs = 12 # nombre minimal de curseurs à afficher
        # Nombres de composantes dont le curseur s'affiche à l'écran
        self.n_composantes_ajustables = min(nb_minimal_curseurs, len(self.liste_textes[0].vecteur))
        self.liste_composantes_ajustables = indices_coefficients_separateurs[:self.n_composantes_ajustables]

        self.coefficients_coordonnees = [1]*self.dimension

        self.points = self.normaliser_points(vecteurs)

        # Création des objets de la fenêtre
        self.theorique = True
        self.affiche_enveloppe = False

        self.objets_dessines = []
        self.fenetre = fenetre = Tk()
        self.canvas = Canvas(fenetre, width=self.width, height=self.height, background="white")
        self.canvas.bind("<Motion>", self.mouse_motion_canvas)
        self.couleurs = ["yellow", "red", "green", "blue", "black", "purple",
                         "brown1", "gray", "cyan", "white", "royal blue", "dark violet"]

        self.theorique_concret_switch = Button(self.fenetre, text="Afficher le résultat du classifieur",
                                               command=self.switch_theorique_concret)
        self.enveloppe_switch = Checkbutton(self.fenetre, text="Afficher les enveloppes convexes",
                                            command=self.switch_points_enveloppe)

        self.noms_composantes = analyseur.noms_composantes()

        # Sera redéfini au premier appel de build_fenetre, sert
        # à définir temporairement scales et noms_scales
        self.curseur_canvas = Canvas(fenetre)
        self.curseur_frame = None

        self.scales = []
        self.noms_scales = []

        for i in range(self.dimension):
            lb = Label(self.curseur_canvas, text=self.noms_composantes[i])
            self.noms_scales.append(lb)
            sc = Scale(self.curseur_canvas, orient='horizontal', resolution=1, from_=1, to=100,
                       command=self.change_proportion_builder(i))
            sc.set(1)
            self.scales.append(sc)

        self.intVars = [] # stocke les valeurs des boutons du menu
        for i in range(self.dimension):
            iv = IntVar()
            if i in self.liste_composantes_ajustables:
                iv.set(1)
            else:
                iv.set(0)
            self.intVars.append(iv)

        # Variables d'informations sur l'oeuvre courante
        self.frame_courant = Frame(self.fenetre, borderwidth=2, relief=SUNKEN)
        self.texte_courant = Label(self.frame_courant, text="Texte courant le plus proche : ",
                                   justify=LEFT)

    def mouse_motion_canvas(self, arg):
        tab = [(point[0]-arg.x)**2+(point[1]-arg.y)**2 for point in self.points]
        m = min(tab)
        indice = tab.index(m)
        s = "Texte le plus proche : \n" \
            "Auteur : {0} \n" \
            "Numéro oeuvre : {1} \n" \
            "Identifiant chunk : {2}".format(self.liste_textes[indice].auteur,
                                             self.liste_textes[indice].numero,
                                             self.liste_textes[indice].numero_morceau)
        self.texte_courant['text'] = s

    def tri_par_importance(self, liste_indices_composantes):
        importance_composantes = self.poids_composantes
        return sorted(liste_indices_composantes, key=(lambda k: importance_composantes[k]))[::-1]

    def switch_composante_builder(self, i):
        return lambda: self.switch_composante(i)

    # Ajoute ou supprime un curseur
    def switch_composante(self, i):
        if i in self.liste_composantes_ajustables:
            self.liste_composantes_ajustables.remove(i)
        else:
            self.liste_composantes_ajustables.append(i)
            self.liste_composantes_ajustables = self.tri_par_importance(self.liste_composantes_ajustables)
        self.build_curseurs()

    def change_proportion_builder(self, i):
        return lambda arg: self.change_proportion(i, arg)

    def change_proportion(self, i, arg2):
        if arg2 == 0:
            arg = 1
        else:
            arg = arg2
        # on multiplie la matrice de proportion à droite par une matrice de dilatation pour multiplier sa i-ème colonne
        """dilatation = np.identity(len(self.matrice_proportions))"""
        indice = i
        """dilatation[indice][indice] = float(arg)/max(float(self.coefficients_coordonnees[indice]), 0.1)
        self.matrice_proportions = np.dot(self.matrice_proportions, dilatation)"""
        for k in range(self.dimension):
            self.matrice_proportions[k][indice] *= float(arg)/max(float(self.coefficients_coordonnees[indice]), 0.1)
        self.coefficients_coordonnees[indice] = arg

        vecteurs = []
        for k in range(self.n_points):
            vecteurs.append(np.dot(self.matrice_proportions, self.liste_textes[k].vecteur))
        self.points = self.normaliser_points(vecteurs)
        self.repaint()

    def normaliser_points(self, vecteurs):
        """Transforme un tableau de vecteurs (ayant déjà subi methode_reduction)
        en gardant ses deux premieres dimensions et en les renormalisant pour
        l'affichage dans la fenetre"""
        # On regarde les coordonnees extremales pour les normaliser
        x_min = vecteurs[0][0]
        y_min = vecteurs[0][1]
        x_max = vecteurs[0][0]
        y_max = vecteurs[0][1]
        for vecteur in vecteurs:
            x = vecteur[0]
            y = vecteur[1]
            if x > x_max:
                x_max = x
            if x < x_min:
                x_min = x
            if y > y_max:
                y_max = y
            if y < y_min:
                y_min = y

        proportion_x = self.width / (x_max - x_min) * 0.90
        proportion_y = self.height / (y_max - y_min) * 0.90
        points = []

        for vecteur in vecteurs:
            points.append(
                [(vecteur[0] - x_min) * proportion_x + 0.05 * (x_max - x_min) * proportion_x,
                 (vecteur[1] - y_min) * proportion_y + 0.05 * (y_max - y_min) * proportion_y])

        return points

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
        return self.noms_auteurs_inverses[self.liste_textes[indice].categorie]

    # A partir de p_ref
    def auteur_concret(self, indice):
        res = 0
        for i in range(0, len(self.p[indice])):
            if self.p[indice][i] > self.p[indice][res]:
                res = i
        return res

    def repaint(self):
        for objet in self.objets_dessines:
            self.canvas.delete(objet)
        self.objets_dessines = []

        for i in range(self.n_points):
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

    def _on_mousewheel(self, canvas):
        return (
            lambda event:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        )

    def build_curseurs(self):
        # Scrolling list des CURSEURS
        scrollbar = Scrollbar(self.fenetre, orient=VERTICAL)
        scrollbar.grid(row=0, column=2, rowspan=10, sticky=NS)
        canvas = Canvas(self.fenetre, bd=0, highlightthickness=0, height=self.height,
                                 yscrollcommand=scrollbar.set)
        frame = Frame(canvas)
        scrollbar.config(command=canvas.yview)
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        interior_id = canvas.create_window(0, 0, window=frame,
                                           anchor=NW)

        def _configure_interior(event):
            size = (frame.winfo_reqwidth(), frame.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if frame.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=frame.winfo_reqwidth())

        frame.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if frame.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)
        canvas.bind_all("<MouseWheel>", self._on_mousewheel(canvas))

        for i in range(len(self.liste_composantes_ajustables)):
            lb = Label(frame, text=self.noms_composantes[i])
            self.noms_scales[self.liste_composantes_ajustables[i]] = lb
            lb.grid(row=2*i, column=0, rowspan=1, columnspan=1, sticky=W)

            sc = Scale(frame, orient='horizontal', resolution=1, from_=1, to=100,
                       command=self.change_proportion_builder(i))
            sc.set(self.scales[self.liste_composantes_ajustables[i]].get())
            self.scales[self.liste_composantes_ajustables[i]] = sc
            sc.grid(row=2*i+1, column=0, rowspan=1, columnspan=1, sticky=W)


        canvas.grid(row=0, column=3, columnspan=1, rowspan=10, sticky=NW)

    def build_menu(self, analyseur, pere):
        # Impossible d'utiliser instanceof, car il faudrait importer classes.py,
        # or c'est classes.py qui nous importe, donc on créerait une boucle
        # d'importations.
        # La ligne suivante est donc équivalente à
        # if instanceof(analyseur, FonctionAnalyse):
        localmenu = Menu(pere, tearoff=0)
        if analyseur.__class__.__name__ != "Analyseur":
            numeros = range(analyseur.init, analyseur.end)
            noms = analyseur.noms_composantes()
            for i in range(len(numeros)):
                localmenu.add_checkbutton(label=noms[i],
                                              command=self.switch_composante_builder(numeros[i]),
                                              variable=self.intVars[numeros[i]],
                                              onvalue=1,
                                              offvalue=0)
        else:
            for fils in analyseur.fils:
                self.build_menu(fils, localmenu)
        pere.add_cascade(label=analyseur.nom, menu=localmenu)

    def build(self):
        menu = Menu(self.fenetre)
        self.analyseur.numeroter()
        for fils in self.analyseur.fils:
            self.build_menu(fils, menu)
        self.fenetre.config(menu=menu)

        self.canvas.grid(row=0, column=0, rowspan=10, columnspan=2)
        self.repaint()

        self.theorique_concret_switch.grid(row=11, column=0)
        self.enveloppe_switch.grid(row=11, column=1)

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
        frame_auteurs.grid(row=12, column=0, columnspan=2, sticky=W)
        frame_clusters.grid(row=13, column=0, columnspan=2, sticky=W)

        self.build_curseurs()

        # Zone d'informations sur le point pointé
        self.frame_courant.grid(row=11, column=2, rowspan=3, columnspan=2, sticky=NSEW, padx=10, pady=10)
        self.texte_courant.grid(row=0, column=0, sticky=NW)

        self.fenetre.mainloop()
