# -*- coding: utf-8 -*-
import numpy as np

import classes
from Representation.fenetre import FenetreAffichage


class kPPV(classes.Classifieur):
    """
    NB : le training_set du KPPV DOIT contenir un texte de chaque auteur
    """
    def __init__(self):
        print("Classication par la méthode des k plus proches voisins")

    def scalaire(self, x, y):
        return sum([x[i] * y[i] for i in range(min(len(x), len(y)))])

    def norme(self, x):
        return np.sqrt(self.scalaire(x, x))

    def distance(self, x, y):
        return self.norme([x[i] - y[i] for i in range(min(len(x), len(y)))])

    def k_plus_proches_voisins(self, liste_textes_tuples, k, texte):
        """Prend un tableau de (texte, classe) et le point considéré et retourne
        la liste des k éléments (vecteur, classe) les plus proches de texte.vecteur"""
        return sorted(liste_textes_tuples, key=(lambda x: self.distance(x[0].vecteur, texte.vecteur)))[1:k+1]

    def classe_majoritaire(self, ensemble):
        """Retourne la classe majoritaire dans un ensemble de points (texte, classe)"""
        tailles_classes = np.zeros(len(self.clusters))
        for x in ensemble:
            tailles_classes[x[1]] = 0
        for x in ensemble:
            tailles_classes[x[1]] += 1
        indice_max = 0
        for i in range(len(tailles_classes)):
            if tailles_classes[i] > tailles_classes[indice_max]:
                indice_max = i
        return indice_max

    def ajouter_texte(self, nombre_voisins, texte):
        """Attribue le texte donné en entrée"""
        kppv_list = self.k_plus_proches_voisins(self.liste_textes_tuples, nombre_voisins, texte)
        self.liste_textes_tuples += [[texte, self.classe_majoritaire(kppv_list)]]

    def classifier(self, training_set, eval_set, noms_composantes):
        # format d'entrée : training_set contient les textes déjà classés, et eval_set contient les textes à classifier

        self.k = min(len(training_set),9)  # Initialisation du nombre de voisins, à adapter si besoin
        self.liste_textes = training_set + eval_set
        self.training_set = training_set
        self.eval_set = eval_set
        self.p = None
        self.p_ref = None
        self.classification = None
        self.noms_composantes = noms_composantes

        # Initialisation de classes_auteurs, clusters et liste_textes_tuples
        self.classes_auteurs = {}  # auteurs_classes[auteur de la classe] = numero_classe
        self.clusters = []
        for texte in self.training_set:
            if not texte.auteur in self.classes_auteurs.keys():
                self.classes_auteurs[texte.auteur] = len(self.classes_auteurs)
                self.clusters.append([texte])
            else:
                self.clusters[self.classes_auteurs[texte.auteur]].append(texte)

        self.liste_textes_tuples = [] # liste de tuples (texte, classe)
        for i in range(len(self.clusters)):
            self.liste_textes_tuples += [[texte,i] for texte in self.clusters[i]]

        # Classification des textes de eval_set
        for texte in eval_set:
            self.ajouter_texte(self.k, texte)

        # Actualisation de self.clusters
        self.clusters = [[] for i in range(len(self.clusters))]
        for tuple in self.liste_textes_tuples:
            self.clusters[tuple[1]].append(tuple[0])

        # On constitue la liste des auteurs => sert à construire p_ref
        self.auteurs = []
        self.auteurs_inverses = {}
        for texte in training_set:
            if texte.auteur not in self.auteurs:
                self.auteurs.append(texte.auteur)
                self.auteurs_inverses[texte.auteur] = len(self.auteurs) - 1

        # Création de p et de p_ref
        self.p = np.zeros([len(self.liste_textes_tuples), len(self.clusters)])
        self.p_ref = np.zeros([len(self.liste_textes_tuples), len(self.clusters)])
        for i in range(len(self.liste_textes_tuples)):
            self.p[i][self.liste_textes_tuples[i][1]] = 1  # [texte, classe du texte]
            self.p_ref[i][self.auteurs_inverses[self.liste_textes_tuples[i][0].auteur]] = 1

    def afficher(self):
        fenetre = FenetreAffichage([], self.liste_textes, self.p, self.p_ref, self.auteurs, "pca", self.poids_composantes(), self.noms_composantes)
        fenetre.build()