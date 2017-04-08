# -*- coding: utf-8 -*-
import codecs
import csv
import pickle
import numpy as np
from treetaggerwrapper import TreeTagger, make_tags
from Evaluation import evaluation_externe as ee
from Evaluation import evaluation_interne as ei
from Evaluation import evaluation_relative as er
from Interpretation.importance_composantes import importance, nouveaux_clusters
from Utilitaires.importation_et_pretraitement import importer, formater
#from Utilitaires.importation_et_pretraitement_pour_le_chinois import importer
from Utilitaires.equilibrage_et_normalisation import normaliser1, equilibrer1
from Utilitaires.defuzze import defuzze
from Representation.fenetre import FenetreAffichage
import random


emplacement_maxime = "/Users/maximegodin/Google Drive/Groupe PSC/"
emplacement_guillaume = "/Users/Guillaume/Google Drive/Cours X/PSC/Groupe PSC/"
emplacement_clement = "C:/Users/Clement/Google Drive/Groupe PSC/"
emplacement_wang = "/home/wang/Documents/PSC/GitDePSC/"
emplacement_lucile = "/Users/Lucile/Google Drive/Groupe PSC/"

emplacement_dossier_groupe = emplacement_clement


dico_langues = {"fr" : "francais", "en" : "anglais", "es" : "espagnol", "de" : "allemand", "zh" : "chinois"}

class Infos:
    """Contient les méta-données concernant notre oeuvre"""
    # A compléter avec la base de données

    def __init__(self,auteur,numero):
        pass


class Oeuvre:
    """Un objet Oeuvre est caractérisé par (auteur,numero). Ses attributs sont :
            - langue = "fr", "en", ...
            - infos = objet Infos défini plus haut
            - texte_brut = string contenant le texte de l'oeuvre
            - mots = tableau de strings contenant les mots et unités textuelles (ponctuation)
            - racines = tableau de strings contenant les racines de chaque élément de mots, autrement dit la version du dictionnaire (non conjugée, au singulier masculin, etc.)
            - POS = tableau de strings conenant les parts-of-speech associées à chaque mot, autrement dit sa nature grammaticale (verbe, nom, etc.). Attention : leur expression varie selon la langue du tagger : en français "NOM", en anglais "NN"
            """

    def __init__(self, auteur, numero, langue = "fr"):
        """Crée l'objet Oeuvre s'il n'existe pas encore et le sauvegarde dans un fichier du même nom. S'il existe déjà, on le reprend simplement dans le fichier."""
        self.auteur = auteur
        self.numero = numero
        self.langue = langue
        self.categorie = None
        emplacement_textes = emplacement_dossier_groupe + "Corpus/" + dico_langues[langue] + "/Fichiers txt/"
        emplacement_oeuvres = emplacement_dossier_groupe + "Corpus/" + dico_langues[langue] + "/Fichiers oeuvres/"
        #self.infos = Infos(auteur,numero)
        print(auteur + str(numero), end = " ")
        try:
            with open(emplacement_oeuvres + auteur + str(numero), "rb") as mon_fichier:
                o = pickle.load(mon_fichier)
            self.texte_brut = o.texte_brut
            self.tags = o.tags
            self.mots = o.mots
            self.racines = o.racines
            self.POS = o.POS
            print("(importation terminee)", end = " / ")
        except FileNotFoundError:
            tagger = TreeTagger(TAGLANG = self.langue)
            self.texte_brut = formater(importer(auteur, numero,emplacement_textes))
            self.tags = make_tags(tagger.tag_text(self.texte_brut))
            self.mots = [t[0] for t in self.tags if len(t) == 3]
            self.racines = [t[2] for t in self.tags if len(t) == 3]
            self.POS = [t[1] for t in self.tags if len(t) == 3]
            with open(emplacement_oeuvres + "/" + auteur + str(numero), "wb") as mon_fichier:
                pickle.dump(self,mon_fichier,protocol = 2)
            print("(creation terminee)", end = " / ")

    def __equal__(self, oeuvre2):
        return (self.auteur == oeuvre2.auteur) and (self.numero == oeuvre2.numero)

    def split(self,taille_morceaux, full_text = False):
        """Sépare une oeuvre en objets Texte de longueur taille_morceaux possédant les mêmes attributs que l'oeuvre."""
        tab_texts = []
        auteur = self.auteur
        numero = self.numero
        langue = self.langue
        categorie = self.categorie
        if not full_text:
            L = len(self.tags)
            for k in range(0,L-taille_morceaux,taille_morceaux):
                mots = self.mots[k:k+taille_morceaux]
                texte_brut = " ".join(mots)
                racines = self.racines[k:k+taille_morceaux]
                POS = self.POS[k:k+taille_morceaux]
                T = Texte(auteur,numero,categorie,langue,k//taille_morceaux,texte_brut,mots,racines,POS)
                tab_texts.append(T)
        elif full_text:
            k = 0
            mots = self.mots
            texte_brut = " ".join(mots)
            racines = self.racines
            POS = self.POS
            T = Texte(auteur, numero, categorie, langue, k // taille_morceaux, texte_brut, mots, racines, POS)
            tab_texts.append(T)
        return tab_texts

class Texte:
    """Un objet Texte correspondra à un point dans notre analyse et classification. Ses attributs sont les mêmes que pour Oeuvre, avec en plus :
    - vecteur = liste de réels correspondant à des caractéristiques littéraires (initialisée à None, elle sera remplie par l'analyseur)
    - composantes_vecteur = liste de strings expliquant la signification littéraire de chaque coordonnée du vecteur associé (ex : "fréquence du 3e mot le plus courant")
    - categorie : son rangement dans la classification, soit donné comme hypothèse (pour training_set) soit résultant de l'algorithme (pour eval_set)
    """

    def __init__(self,auteur,numero,categorie,langue,numero_morceau,texte_brut,mots,racines,POS):
        self.auteur = auteur
        self.numero = numero
        self.categorie = categorie
        self.langue = langue
        self.infos = Infos(auteur,numero)
        self.numero_morceau = numero_morceau
        self.texte_brut = texte_brut
        self.mots = mots
        self.racines = racines
        self.POS = POS
        self.vecteur = []
        self.vecteur_pca = None

    def __equal__(self,texte2):
        return (self.auteur == texte2.auteur) and (self.numero == texte2.numero) and (self.numero_morceau == texte2.numero_morceau)

    def copy(self):
        return Texte(self.auteur, self.numero, self.categorie, self.langue, self.numero_morceau, self.texte_brut, self.mots, self.racines, self.POS)

class Analyseur:
    def __init__(self, nom, liste_fils):
        self.nom = nom
        self.fils = liste_fils

    def analyser(self, liste_textes):
        for f in self.fils:
            f.analyser(liste_textes)

    def noms_composantes(self):
        res = []
        for f in self.fils:
            res+= f.noms_composantes()
        return res

    def noms_fonctions(self):
        res = []
        for f in self.fils:
            res += f.noms_fonctions()
        return res

    def aux_numeroter(self,n):
        self.init = n
        for f in self.fils:
            n = f.aux_numeroter(n)
        self.end = n
        return self.end

    def numeroter(self):
        self.aux_numeroter(0)

class FonctionAnalyse(Analyseur):

    def __init__(self,nom,liste_composantes):
        super(FonctionAnalyse, self).__init__("",[])
        self.liste_composantes = liste_composantes
        self.nom = nom

    def noms_composantes(self):
        return self.liste_composantes

    def noms_fonctions(self):
        return [self.nom]

    def analyser(self, liste_textes):
        return

    def aux_numeroter(self, n):
        self.init = n
        self.end = n + len(self.liste_composantes)
        return self.end

class Classifieur:
    """Un objet Classifieur correspond à une méthode d'analyse des données pour en extraire des regroupements ou des attributions. Deux fonctions sont nécessaires pour l'instant : une fonction analyser qui renvoie une classification sous une forme quelconque, et une fonction classifier. Les attributs qui doivent être remplis sont :
    - p = matrice de partition (floue) résultant de la classification, de taille (nb_textes, nb_classes), où le coefficient m_{i,j} est la probabilité d'appartenance du texte i à la catégorie j
    - p_ref = matrice de partition (floue) connue au préalable avec nos informations sur les catégories des textes
    """

    def __init__(self):
        self.clusters = None

    def classifier(self, training_set, eval_set, categories):
        pass

    def poids_composantes(self, clusters=None):
        return importance(self.clusters)

class Probleme:
    """Un objet Problème rassemble tous les éléments d'un questionnement d'attribution :
    - liste_oeuvres = liste des objets Oeuvres que l'on veut étudier
    - liste_textes = textes obtenus en découpant chaque oeuvre en morceaux de longueur taille_morceaux
    - analyseur = objet Analyseur
    - classifieur = objet Classifieur
    """

    def __init__(self, id_training_set, categories, id_eval_set, categories_supposees, taille_morceaux, analyseur, classifieur, langue = "fr", full_text = False):
        print("ASSEMBLAGE DU PROBLEME")
        print("")
        self.oeuvres_training_set = []
        self.oeuvres_eval_set = []
        self.categories = categories
        self.categories_supposees = categories_supposees
        self.taille_morceaux = taille_morceaux
        self.liste_oeuvres = []
        print("Création - importation des oeuvres : ")
        for k in range(len(id_training_set)):
            for ident in id_training_set[k]:
                auteur = ident[0]
                numero = ident[1]
                oeuvre = Oeuvre(auteur,numero,langue)
                oeuvre.categorie = categories[k]
                self.oeuvres_training_set.append(oeuvre)
        for k in range(len(id_eval_set)):
            for ident in id_eval_set[k]:
                auteur = ident[0]
                numero = ident[1]
                oeuvre = Oeuvre(auteur,numero,langue)
                oeuvre.categorie = categories_supposees[k]
                self.oeuvres_eval_set.append(oeuvre)
        print()
        print("Liste_oeuvres remplie")
        self.analyseur = analyseur
        print("Analyseur basé sur " + " ".join(self.analyseur.noms_fonctions()) + " initialisé")
        print("Nombre de composantes : {}".format(len(analyseur.noms_composantes())))
        self.classifieur = classifieur
        print("Classifieur initialisé")
        self.eval_set = []
        self.training_set = []
        self.liste_textes = []
        self.full_text = full_text

    def creer_textes(self, equilibrage = True, equilibrage_eval = False):
        for oeuvre in self.oeuvres_training_set:
            self.training_set.extend(oeuvre.split(self.taille_morceaux,self.full_text))
        for oeuvre in self.oeuvres_eval_set:
             self.eval_set.extend(oeuvre.split(self.taille_morceaux, self.full_text))
        if equilibrage :
            self.training_set = equilibrer1(self.training_set)
            print("Nombre de textes par catégorie après équilibrage : {}".format(len(self.training_set)//len(self.categories)))
        if equilibrage_eval :
            self.eval_set = equilibrer1(self.eval_set)
        self.liste_textes = self.training_set + self.eval_set
        print("Textes de training_set et eval_set initialisés")

    def analyser(self, normalisation = False):
        """Applique la méthode analyser de l'analyseur : elle remplit les coordonnées du vecteur associé à chaque texte, et calcule le vecteur normalisé."""
        self.analyseur.analyser(self.liste_textes)
        D = np.array([texte.vecteur for texte in self.liste_textes])
        A = D
        if normalisation:
            A = normaliser1(D)
        for k,texte in enumerate(self.liste_textes):
            texte.vecteur = A[k]
        print("Textes analysés et vectorisés")

    def appliquer_classifieur(self):
        """Applique la méthode classifier du classifieur pour obtenir une classification, sous un format a priori inconnu."""
        self.classifieur.liste_textes = self.liste_textes
        self.classifieur.training_set = self.training_set
        self.classifieur.eval_set = self.eval_set
        self.classifieur.categories = self.categories
        self.classifieur.categories_supposees = self.categories_supposees
        self.classifieur.classifier(training_set=self.training_set, eval_set=self.eval_set, categories = self.categories)
        print("Classification effectuée")

    def evaluer(self):
        p_d = defuzze(self.classifieur.p)
        print("/// Evaluation interne ///")
        print("Indice de Hubert interne : " + str(ei.huberts_interne(self.eval_set, p_d)))
        print("/// Evaluation relative ///")
        #print("Trop long, décommentez les indices correspondants dans classes.py si vous avez du temps")
        #print("Indice de Hubert relatif : " + str(er.huberts_relatif(self.eval_set, self.classifieur.p)))
        print("Indice de Dunn : " + str(er.dunn(self.eval_set, p_d)))
        print("Indice de Davies-Bouldin : " + str(er.davies_bouldin(self.eval_set, p_d)))
        print("/// Evaluation externe ///")
        print("Précision : " + str(ee.precision(self.eval_set, p_d, self.classifieur.p_ref)))
        print("Entropie de la classification : " + str(ee.entropie(self.eval_set, p_d, self.classifieur.p_ref)))
        print("Indice de Rand : " + str(ee.jaccard(self.eval_set, p_d, self.classifieur.p_ref)))
        print("Indice de Fowlkes & Mallows : " + str(ee.fowlkes_mallows(self.eval_set, p_d, self.classifieur.p_ref)))
        print("Taux de liaisons et non-liaisons correctes et incorrectes : " + str(
                ee.calcul_taux(self.eval_set, p_d, self.classifieur.p_ref)))

    def interpreter(self, utiliser_textes_training = True, alpha = 1):
        print("Composantes les plus importantes dans la classification :")
        noms_composantes = self.analyseur.noms_composantes()
        if utiliser_textes_training:
            new_clusters = nouveaux_clusters(self.classifieur.training_set, self.classifieur.clusters, self.classifieur.categories)
        else:
            new_clusters = self.classifieur.clusters
        A = importance(new_clusters, comp = True)
        categories = self.classifieur.categories
        importance1 = A[0]
        ecarts_inter = A[1]
        ecarts_intra = A[2]
        moyennes_clusters = A[3]
        indices_tries = sorted(list(range(len(importance1))), key = lambda k : importance1[k], reverse = True)
        noms_et_importance1 = [(noms_composantes[k],importance1[k]) for k in indices_tries]
        n=0
        while n<len(noms_et_importance1) and noms_et_importance1[n][1]>alpha and n<30:
            n+=1
        if n>=len(noms_et_importance1):
            n=len(noms_et_importance1)
        for k in range(n):
            print("")
            print(str(k+1) + ") " + noms_et_importance1[k][0])
            print("Importance : {:.4f}".format(noms_et_importance1[k][1]))
            i = indices_tries[k]
            print("   Ecart intra clusters pour cette composante : {:.4f} ".format(ecarts_intra[i]))
            print("   Ecart inter clusters pour cette composante : {:.4f} ".format(ecarts_inter[i]))
            for l in range(len(moyennes_clusters)):
                m = moyennes_clusters[l]
                cat = categories[l]
                print("      Moyenne parmi les textes de la categorie " + cat + " : {:.4f}".format(m[i]))

    def afficher_graphique(self, poids_composantes=None):
        print("Affichage graphique des résultats")
        if poids_composantes is None:
            poids_composantes = self.classifieur.poids_composantes
        fenetre = FenetreAffichage(self.analyseur, self.classifieur, poids_composantes(self.classifieur.clusters))
        fenetre.build()

    def afficher(self):
        print("Résultats de la classification :")
        attrib_oeuvres = {}
        for o in self.oeuvres_eval_set:
            attrib_oeuvres[o.auteur+str(o.numero)] = np.zeros((len(self.classifieur.categories)))
        for i in range(self.classifieur.p.shape[0]):
            t = self.eval_set[i]
            attrib_oeuvres[t.auteur + str(t.numero)]+= self.classifieur.p[i,:]
        for o in self.oeuvres_eval_set:
            j = np.argmax(attrib_oeuvres[o.auteur+str(o.numero)])
            if attrib_oeuvres[o.auteur+str(o.numero)][j] == 0:
                print(o.auteur + str(o.numero) + "n'a pas été attribué.")
            else:
                print(o.auteur+str(o.numero) + " est dans la catégorie "+ self.classifieur.categories[j] +" (" + str(attrib_oeuvres[o.auteur+str(o.numero)][j]*100/np.sum(attrib_oeuvres[o.auteur+str(o.numero)]))+" %).")


    def resoudre(self):
        print("")
        print("CREATION DES TEXTES")  
        print("")
        self.creer_textes()
        print("")
        print("ANALYSE")
        print("")
        self.analyser()
        print("")
        print("CLASSIFICATION")
        print("")
        self.appliquer_classifieur()
        print("")
        print("EVALUATION")
        print("")
        self.evaluer()
        print("")
        print("INTERPRETATION")
        print("")
        self.interpreter()
        print("")
        print("AFFICHAGE")
        print("")
        self.afficher()
        self.afficher_graphique()

class Verification:
    
    def __init__(self, id_oeuvres_base, categories_base, id_oeuvres_calibrage, categories_calibrage, id_oeuvres_disputees, categories_disputees, taille_morceaux, analyseur, verificateur, langue = "fr", full_text = False):
        print("Assemblage du problème de vérification")
        self.id_oeuvres_base = id_oeuvres_base
        self.id_oeuvres_calibrage = id_oeuvres_calibrage
        self.id_oeuvres_disputees = id_oeuvres_disputees
        self.liste_id_oeuvres_base = []
        self.liste_id_oeuvres_calibrage = []
        self.liste_id_oeuvres_disputees = []
        self.oeuvres_base = []
        self.oeuvres_calibrage = []
        self.oeuvres_disputees = []
        self.categories_base = categories_base
        self.categories_calibrage = categories_calibrage
        self.categories_disputees = categories_disputees
        self.taille_morceaux = taille_morceaux
        self.liste_oeuvres = []
        print("Création - importation des oeuvres : ")
        for k in range(len(id_oeuvres_base)):
            for ident in id_oeuvres_base[k]:
                auteur = ident[0]
                numero = ident[1]
                oeuvre = Oeuvre(auteur,numero,langue)
                oeuvre.categorie = categories_base[k]
                self.oeuvres_base.append(oeuvre)
                self.liste_id_oeuvres_base.append((auteur,numero))
        for k in range(len(id_oeuvres_calibrage)):
            for ident in id_oeuvres_calibrage[k]:
                auteur = ident[0]
                numero = ident[1]
                oeuvre = Oeuvre(auteur,numero,langue)
                oeuvre.categorie = categories_calibrage[k]
                self.oeuvres_calibrage.append(oeuvre)
                self.liste_id_oeuvres_calibrage.append((auteur,numero))
        for k in range(len(id_oeuvres_disputees)):
            for ident in id_oeuvres_disputees[k]:
                auteur = ident[0]
                numero = ident[1]
                oeuvre = Oeuvre(auteur,numero,langue)
                oeuvre.categorie = categories_disputees[k]
                self.oeuvres_disputees.append(oeuvre)
                self.liste_id_oeuvres_disputees.append((auteur,numero))
        print("")
        print("Liste_oeuvres remplie")
        self.analyseur = analyseur
        print("Analyseur basé sur " + " ".join(analyseur.noms_fonctions()) + " initialisé")
        self.verificateur = verificateur
        self.verificateur.liste_id_oeuvres_base = self.liste_id_oeuvres_base
        self.verificateur.liste_id_oeuvres_calibrage = self.liste_id_oeuvres_calibrage
        self.verificateur.liste_id_oeuvres_disputees = self.liste_id_oeuvres_disputees
        self.verificateur.oeuvres_base = self.oeuvres_base
        self.verificateur.oeuvres_calibrage = self.oeuvres_calibrage
        self.verificateur.oeuvres_disputees = self.oeuvres_disputees
        self.verificateur.categories_base = categories_base
        self.verificateur.categories_calibrage = categories_calibrage
        self.verificateur.categories_disputees = categories_disputees
        self.verificateur.analyseur = analyseur
        self.verificateur.taille_morceaux = taille_morceaux
        print("Vérificateur initialisé")
        self.textes_base = []
        self.textes_calibrage = []
        self.textes_disputes = []
        self.full_text = full_text
        self.liste_textes = []

    def creer_textes(self):
        for oeuvre in self.oeuvres_base:
            self.textes_base.extend(oeuvre.split(self.taille_morceaux,self.full_text))
        for oeuvre in self.oeuvres_calibrage:
             self.textes_calibrage.extend(oeuvre.split(self.taille_morceaux, self.full_text))
        for oeuvre in self.oeuvres_disputees:
            self.textes_disputes.extend(oeuvre.split(self.taille_morceaux,self.full_text))
        self.liste_textes = self.textes_base + self.textes_calibrage + self.textes_disputes
        print("Textes initialisés")
        print("Ensemble de base : {} textes".format(len(self.textes_base)))
        print("Ensemble de calibrage : {} textes".format(len(self.textes_calibrage)))
        print("Ensemble de verif : {} textes".format(len(self.textes_disputes)))

    def analyser(self, normalisation = True):
        """Applique la méthode analyser de l'analyseur : elle remplit les coordonnées du vecteur associé à chaque texte, et calcule le vecteur normalisé."""
        self.analyseur.analyser(self.liste_textes)
        D = np.array([texte.vecteur for texte in self.liste_textes])
        A = D
        if normalisation:
            A = normaliser1(D)
        for k,texte in enumerate(self.liste_textes):
            texte.vecteur = A[k]
        print("Textes analysés et vectorisés")

    def appliquer_verificateur(self):
        """Applique le verificateur pour determiner la paternité de l'oeuvre disputée.""" 
        self.verificateur.calibrer(self.textes_base, self.textes_calibrage)
        self.verificateur.verifier(self.textes_base, self.textes_disputes)
        self.verificateur.afficher()

    def resoudre(self):
        print("")
        print("Création des textes :")
        self.creer_textes()
        print("")
        print("Analyse :")
        self.analyser()
        print("")
        print("Calibrage, démasquage et affichage :")
        self.appliquer_verificateur()
        print("")


class CrossValidation:
    def __init__(self, id_oeuvres, categories, taille_morceaux, analyseur, createur_classifieur, pourcentage_eval = 0.1, nombre_essais = 20, langue = "fr", full_text = False, leave_one_out = False):
        print("ASSEMBLAGE DE LA VALIDATION CROISEE")
        print("")
        self.oeuvres = []
        self.categories = categories
        self.taille_morceaux = taille_morceaux
        self.liste_oeuvres = []
        print("Création - importation des oeuvres : ")
        for k in range(len(id_oeuvres)):
            for ident in id_oeuvres[k]:
                auteur = ident[0]
                numero = ident[1]
                oeuvre = Oeuvre(auteur,numero,langue)
                oeuvre.categorie = categories[k]
                self.oeuvres.append(oeuvre)
        print()
        print("Oeuvres initialisées")
        self.analyseur = analyseur
        print("Analyseur basé sur " + " ".join(self.analyseur.noms_fonctions()) + " initialisé")
        print("Nombre de composantes : {}".format(len(analyseur.noms_composantes())))
        self.liste_textes = []
        self.full_text = full_text
        self.pourcentage_eval = pourcentage_eval
        self.nombre_essais = nombre_essais
        self.leave_one_out = leave_one_out
        self.createur_classifieur = createur_classifieur

    def creer_textes(self, equilibrage = True):
        for oeuvre in self.oeuvres:
            self.liste_textes.extend(oeuvre.split(self.taille_morceaux,self.full_text))
        if equilibrage :
            self.liste_textes = equilibrer1(self.liste_textes)
        print("Textes initialisés")
        print("Nombre de textes par catégorie après équilibrage : {}".format(len(self.liste_textes)//len(self.categories)))

    def analyser(self, normalisation = False):
        """Applique la méthode analyser de l'analyseur : elle remplit les coordonnées du vecteur associé à chaque texte, et calcule le vecteur normalisé."""
        self.analyseur.analyser(self.liste_textes)
        D = np.array([texte.vecteur for texte in self.liste_textes])
        A = D
        if normalisation:
            A = normaliser1(D)
        for k,texte in enumerate(self.liste_textes):
            texte.vecteur = A[k]
        print("Textes analysés et vectorisés")

    def valider(self):
        if self.leave_one_out:
            prec = 0
            for i in range(len(self.liste_textes)):
                print("Texte {} sur {}".format(i+1,len(self.liste_textes)))
                classifieur = self.createur_classifieur()
                indices_eval_set = [i]
                eval_set = [self.liste_textes[i] for i in indices_eval_set]
                training_set = equilibrer1([self.liste_textes[j] for j in range(len(self.liste_textes)) if j not in indices_eval_set])
                classifieur.classifier(training_set, eval_set, self.categories)
                p = ee.precision(classifieur.eval_set, classifieur.p, classifieur.p_ref)
                prec += p
            prec /= len(self.liste_textes)
        else:
            prec = 0
            taille_eval = int(len(self.liste_textes)*self.pourcentage_eval)
            for e in range(self.nombre_essais):
                print("Essai n°{}".format(e+1))
                classifieur = self.createur_classifieur()
                indices_eval_set = random.sample(list(range(len(self.liste_textes))), taille_eval)
                eval_set = [self.liste_textes[i] for i in indices_eval_set]
                training_set = equilibrer1([self.liste_textes[j] for j in range(len(self.liste_textes)) if j not in indices_eval_set])
                classifieur.classifier(training_set, eval_set, self.categories)
                p = ee.precision(classifieur.eval_set, classifieur.p, classifieur.p_ref)
                prec += p
            prec/=self.nombre_essais
        print("")
        if self.leave_one_out:
            print("Validation croisée effectuée par méthode du 'leave one out'")
        else:
            print("Validation croisée effectuée en {} essais, sur un total de {} textes, dont environ {} % dans eval_set et {} % dans training_set".format(self.nombre_essais, len(self.liste_textes), int(self.pourcentage_eval*100), 100 - int(self.pourcentage_eval*100)))
        print("Précision de la validation croisée : {}".format(prec))
        self.prec = prec
        
    def resoudre(self):
        print("")
        print("CREATION DES TEXTES")  
        print("")
        self.creer_textes()
        print("")
        print("ANALYSE")
        print("")
        self.analyser()
        print("")
        print("VALIDATION")
        print("")
        self.valider()
        print("")
