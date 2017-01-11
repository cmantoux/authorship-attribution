import codecs
import csv
import pickle
import numpy as np
from treetaggerwrapper import TreeTagger, make_tags
from Evaluation import evaluation_externe as ee
from Evaluation import evaluation_interne as ei
from Evaluation import evaluation_relative as er
from Interpretation.importance_composantes import gain_information,importance, auteurs_majoritaires
from Utilitaires.importation_et_pretraitement import importer, formater
from Utilitaires.equilibrage_et_normalisation import normaliser1, equilibrer1, equilibrer2

from Representation.fenetre import FenetreAffichage


emplacement_maxime = "/Users/maximegodin/Google Drive/Groupe PSC/"
emplacement_guillaume = "/Users/Guillaume/Google Drive/Cours X/PSC/Groupe PSC/"
emplacement_clement = "C:/Users/Clement/Google Drive/Groupe PSC/"

emplacement_dossier_groupe = emplacement_maxime

dico_langues = {"fr" : "francais", "en" : "anglais", "es" : "espagnol", "de" : "allemand", "ch" : "chinois"}

class Infos:
    """Contient les méta-données concernant notre oeuvre : nom complet de l'auteur, titre de l'oeuvre, année, genre. Ces infos sont extraites du fichier csv (tableur) infos_corpus situé à la racine du dossier Corpus."""
    emplacement_infos = emplacement_dossier_groupe + "Corpus/infos_corpus.csv"

    def __init__(self,auteur,numero):
        """Va chercher dans le tableur infos_corpus les données associées à (auteur,numero)"""
        with codecs.open(self.emplacement_infos, 'r', encoding = 'utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            n = 0
            for row in spamreader:
                n+=1
                aut = row[0]
                num = int(row[1])
                if aut == auteur and num == numero:
                    self.nom_auteur = row[2]
                    self.titre = row[3]
                    self.annee = row[4]
                    self.genre = row[5]
                    break
                if n>1000:
                    break


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
        if not full_text:
            L = len(self.tags)
            for k in range(0,L-taille_morceaux,taille_morceaux):
                mots = self.mots[k:k+taille_morceaux]
                texte_brut = " ".join(mots)
                racines = self.racines[k:k+taille_morceaux]
                POS = self.POS[k:k+taille_morceaux]
                T = Texte(auteur,numero,langue,k//taille_morceaux,texte_brut,mots,racines,POS)
                tab_texts.append(T)
        elif full_text:
            k = 0
            mots = self.mots
            texte_brut = " ".join(mots)
            racines = self.racines
            POS = self.POS
            T = Texte(auteur, numero, langue, k // taille_morceaux, texte_brut, mots, racines, POS)
            tab_texts.append(T)
        return tab_texts

class Texte:
    """Un objet Texte correspondra à un point dans notre analyse et classification. Ses attributs sont les mêmes que pour Oeuvre, avec en plus :
    - vecteur = liste de réels correspondant à des caractéristiques littéraires (initialisée à None, elle sera remplie par l'analyseur)
    - composantes_vecteur = liste de strings expliquant la signification littéraire de chaque coordonnée du vecteur associé (ex : "fréquence du 3e mot le plus courant")
    """

    def __init__(self,auteur,numero,langue,numero_morceau,texte_brut,mots,racines,POS):
        self.auteur = auteur
        self.numero = numero
        self.langue = langue
        self.infos = Infos(auteur,numero)
        self.numero_morceau = numero_morceau
        self.texte_brut = texte_brut
        self.mots = mots
        self.racines = racines
        self.POS = POS
        self.vecteur = None
        self.vecteur_pca = None

    def __equal__(self,texte2):
        return (self.auteur == texte2.auteur) and (self.numero == texte2.numero) and (self.numero_morceau == texte2.numero_morceau)

    def copy(self):
        return Texte(self.auteur, self.numero, self.langue, self.numero_morceau, self.texte_brut, self.mots, self.racines, self.POS)

class Analyseur:
    """Un objet Analyseur représente un ensemble de fonctions d'analyse littéraire, qui extraient des données chiffrées du texte prétraité. Il contient essentiellement une liste de fonctions, chacune des fonctions doit renvoyer, à partir d'un objet Texte, un couple (vecteur, composantes_vecteur). On concatènera ensuite dans l'Analyseur les résultats de ces différentes fonctions."""

    def __init__(self, liste_fonctions):
        self.liste_fonctions = liste_fonctions
        self.noms_composantes = []

    # Je n'ai pas encore trouvé le moyen de pondérer les composantes les unes par rapport aux autres mais c'est potentiellement ici que ça se passera.
    def analyser(self, texte):
        """Remplit l'attribut vecteur du Texte avec le résultat concaténé des différentes fonctions de liste_fonctions."""
        V = []
        noms_composantes = []
        for f in self.liste_fonctions:
            a = f(texte)
            V.extend(a[0])
            noms_composantes.extend(a[1])
        texte.vecteur = V
        self.noms_composantes = noms_composantes


class Classifieur:
    """Un objet Classifieur correspond à une méthode d'analyse des données pour en extraire des regroupements ou des attributions. Deux fonctions sont nécessaires pour l'instant : une fonction analyser qui renvoie une classification sous une forme quelconque, et une fonction afficher. A terme la fonction afficher sera remplacée par l'interface graphique de Clément, et le résultat devra donc être sous le format défini par Maxime :
    - liste_textes = liste des textes fournis au classifieur
    - p = matrice de partition floue résultant de la classification, de taille (nb_textes, nb_classes), où le coefficient m_{i,j} est la probabilité d'appartenance du texte i à la classe j
    - p_ref = matrice de partition floue connue au préalable avec nos informations sur les auteurs des textes
    """

    def classifier(self, training_set, eval_set):
        self.liste_textes = training_set + eval_set
        self.training_set = training_set
        self.eval_set = eval_set
        self.p = None
        self.p_ref = None
        self.precision = 0
        self.classification = None
        self.clusters = None

    def poids_composantes(self):
        return importance(self.clusters)

    def afficher(self):
        print("tada")


class Probleme:
    """Un objet Problème rassemble tous les éléments d'un questionnement d'attribution :
    - liste_oeuvres = liste des objets Oeuvres que l'on veut étudier
    - liste_textes = textes obtenus en découpant chaque oeuvre en morceaux de longueur taille_morceaux
    - analyseur = objet Analyseur
    - classifieur = objet Classifieur
    """

    def __init__(self, liste_id_oeuvres_training_set, liste_id_oeuvres_eval_set, taille_morceaux, analyseur, classifieur, langue = "fr", full_text = False):
        print("Assemblage du problème")
        self.oeuvres_training_set = []
        self.oeuvres_eval_set = []
        self.taille_morceaux = taille_morceaux
        self.liste_oeuvres = []
        print("Création - importation des oeuvres : ")
        for id in liste_id_oeuvres_training_set:
            auteur = id[0]
            numero = id[1]
            oeuvre = Oeuvre(auteur,numero,langue)
            self.oeuvres_training_set.append(oeuvre)
        for id in liste_id_oeuvres_eval_set:
            auteur = id[0]
            numero = id[1]
            oeuvre = Oeuvre(auteur, numero, langue)
            self.oeuvres_eval_set.append(oeuvre)
        print()
        print("Liste_oeuvres remplie")
        self.analyseur = analyseur
        print("Analyseur basé sur " + " ".join([f.__name__ for f in analyseur.liste_fonctions]) + " initialisé")
        self.classifieur = classifieur
        print("Classifieur initialisé")
        self.eval_set = []
        self.training_set = []
        self.liste_texts = []
        self.full_text = full_text

    def creer_textes(self, equilibrage = True, equilibrage_eval = False):
        for oeuvre in self.oeuvres_training_set:
            self.training_set.extend(oeuvre.split(self.taille_morceaux,self.full_text))
        for oeuvre in self.oeuvres_eval_set:
             self.eval_set.extend(oeuvre.split(self.taille_morceaux, self.full_text))
        if equilibrage :
            self.training_set = equilibrer1(self.training_set)
        if equilibrage_eval :
            self.eval_set = equilibrer1(self.eval_set)
        self.liste_textes = self.training_set + self.eval_set
        print("Textes de training_set et eval_set initialisés")

    def analyser(self, normalisation = False):
        """Applique la méthode analyser de l'analyseur : elle remplit les coordonnées du vecteur associé à chaque texte, et calcule le vecteur normalisé."""
        for texte in self.liste_textes:
            self.analyseur.analyser(texte)
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
        print(len(self.analyseur.noms_composantes))
        self.classifieur.classifier(training_set=self.training_set, eval_set=self.eval_set)
        print("Classification effectuée")
        self.classifieur.afficher()

    def evaluer(self):
        print("/// Evaluation interne ///")
        print("Indice de Hubert interne : " + str(ei.huberts_interne(self.eval_set, self.classifieur.p)))
        print("/// Evaluation relative ///")
        #print("Trop long, décommentez les indices correspondants dans classes.py si vous avez du temps")
        #print("Indice de Hubert relatif : " + str(er.huberts_relatif(self.eval_set, self.classifieur.p)))
        print("Indice de Dunn : " + str(er.dunn(self.eval_set, self.classifieur.p)))
        print("Indice de Davies-Bouldin : " + str(er.davies_bouldin(self.eval_set, self.classifieur.p)))
        print("/// Evaluation externe ///")
        print("Précision : " + str(ee.precision(self.eval_set, self.classifieur.p, self.classifieur.p_ref)))
        print("Entropie de la classification : " + str(ee.entropie(self.eval_set, self.classifieur.p, self.classifieur.p_ref)))
        print("Indice de Rand : " + str(ee.jaccard(self.eval_set, self.classifieur.p, self.classifieur.p_ref)))
        print("Indice de Fowlkes & Mallows : " + str(ee.fowlkes_mallows(self.eval_set, self.classifieur.p, self.classifieur.p_ref)))
        print("Taux de liaisons et non-liaisons correctes et incorrectes : " + str(
                ee.calcul_taux(self.eval_set, self.classifieur.p, self.classifieur.p_ref)))

    def interpreter(self):
        print("Composantes les plus importantes dans la classification :")
        noms_composantes = self.analyseur.noms_composantes
        A = importance(self.classifieur.clusters, comp = True)
        #auteurs = auteurs_majoritaires(self.classifieur.clusters)
        auteurs = self.classifieur.auteurs
        importance1 = A[0]
        ecarts_inter = A[1]
        ecarts_intra = A[2]
        moyennes_clusters = A[3]
        indices_tries = sorted(list(range(len(importance1))), key = lambda k : importance1[k], reverse = True)
        noms_et_importance1 = [(noms_composantes[k],importance1[k]) for k in indices_tries]
        n=0
        while noms_et_importance1[n][1]>1:
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
                aut = auteurs[l]
                print("      Moyenne parmi les textes attribués à " + aut + " : {:.4f}".format(m[i]))
        print("")

    def afficher_graphique(self):
        fenetre = FenetreAffichage(self.analyseur, self.classifieur, self.classifieur.poids_composantes())
        fenetre.build()

    def afficher(self):

        attrib_oeuvres = {}
        for o in self.oeuvres_eval_set:
            attrib_oeuvres[o.auteur+str(o.numero)] = np.zeros((len(self.classifieur.auteurs)))
        for i in range(self.classifieur.p.shape[0]):
            t = self.eval_set[i]
            attrib_oeuvres[t.auteur + str(t.numero)]+= self.classifieur.p[i,:]
        for o in self.oeuvres_eval_set:
            j = np.argmax(attrib_oeuvres[o.auteur+str(o.numero)])
            if attrib_oeuvres[o.auteur+str(o.numero)][j] == 0:
                print(o.auteur + str(o.numero) + "n'a pas été attribué.")
            else:
                print(o.auteur+str(o.numero) + " a eté ecrit par "+ self.classifieur.auteurs[j] +" (" + str(attrib_oeuvres[o.auteur+str(o.numero)][j]*100/np.sum(attrib_oeuvres[o.auteur+str(o.numero)]))+" %).")


    def resoudre(self):
        print("Création des textes :")
        self.creer_textes()
        print("")
        print("Analyse :")
        self.analyser()
        print("")
        print("Classification et affichage :")
        self.appliquer_classifieur()
        print("")
        print("Evaluation :")
        self.evaluer()
        print("")
        print("Interprétation :")
        self.interpreter()

class Verification():
    
    def __init__(self, liste_id_oeuvres_base, liste_id_oeuvres_calibrage, liste_id_oeuvres_disputees, taille_morceaux, analyseur, verificateur, langue = "fr", full_text = False):
        print("Assemblage du problème de vérification")
        self.oeuvres_base = []
        self.oeuvres_calibrage = []
        self.oeuvres_disputees = []
        self.taille_morceaux = taille_morceaux
        self.liste_oeuvres = []
        print("Création - importation des oeuvres : ")
        for id in liste_id_oeuvres_base:
            auteur = id[0]
            numero = id[1]
            oeuvre = Oeuvre(auteur,numero,langue)
            self.oeuvres_base.append(oeuvre)
        for id in liste_id_oeuvres_calibrage:
            auteur = id[0]
            numero = id[1]
            oeuvre = Oeuvre(auteur, numero, langue)
            self.oeuvres_calibrage.append(oeuvre)
        for id in liste_id_oeuvres_disputees:
            auteur = id[0]
            numero = id[1]
            oeuvre = Oeuvre(auteur, numero, langue)
            self.oeuvres_disputees.append(oeuvre)
        print("")
        print("Liste_oeuvres remplie")
        self.analyseur = analyseur
        print("Analyseur basé sur " + " ".join([f.__name__ for f in analyseur.liste_fonctions]) + " initialisé")
        self.verificateur = verificateur
        self.verificateur.liste_id_oeuvres_base = liste_id_oeuvres_base
        self.verificateur.liste_id_oeuvres_calibrage = liste_id_oeuvres_calibrage
        self.verificateur.liste_id_oeuvres_disputees = liste_id_oeuvres_disputees
        self.verificateur.oeuvres_base = self.oeuvres_base
        self.verificateur.oeuvres_calibrage = self.oeuvres_calibrage
        self.verificateur.oeuvres_disputees = self.oeuvres_disputees
        self.verificateur.analyseur = analyseur
        self.verificateur.taille_morceaux = taille_morceaux
        print("Vérificateur initialisé")
        self.textes_base = []
        self.textes_calibrage = []
        self.textes_disputes = []
        self.full_text = full_text

    def creer_textes(self):
        for oeuvre in self.oeuvres_base:
            self.textes_base.extend(oeuvre.split(self.taille_morceaux,self.full_text))
        for oeuvre in self.oeuvres_calibrage:
             self.textes_calibrage.extend(oeuvre.split(self.taille_morceaux, self.full_text))
        for oeuvre in self.oeuvres_disputees:
            self.textes_disputes.extend(oeuvre.split(self.taille_morceaux,self.full_text))
        self.liste_textes = self.textes_base + self.textes_calibrage + self.textes_disputes
        print("Textes initialisés")

    def analyser(self, normalisation = True):
        """Applique la méthode analyser de l'analyseur : elle remplit les coordonnées du vecteur associé à chaque texte, et calcule le vecteur normalisé."""
        for texte in self.liste_textes:
            self.analyseur.analyser(texte)
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
