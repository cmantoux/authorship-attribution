from sklearn.svm import SVC

from Interpretation.importance_composantes import *
from Utilitaires.conversion_classification import *
from Utilitaires.pca import pca
from classes import *


class SVM(Classifieur):
    
    def __init__(self, pc = True, kernel = 'rbf', gamma = "auto", C = 5, nombre_composantes = 5000):
        print("Création du classifieur SVM")
        self.pc = pc
        self.kernel = kernel
        self.gamma = gamma
        self.C = C
        self.nombre_composantes = nombre_composantes
        self.liste_textes = None
        self.precision = None
        self.classification = None
        self.clusters = None
        self.p = None
        self.p_ref = None
        self.eval_set = None
        self.training_set = None
        self.index = None
        self.importance_composantes = None
    
    def classifier(self, training_set, eval_set, noms_composantes):
        self.liste_textes = training_set + eval_set
        self.training_set = training_set
        self.eval_set = eval_set
        vecteurs = [t.vecteur for t in self.liste_textes]
        #print(vecteurs)
        nouveaux_vecteurs = pca(vecteurs)
        #print(nouveaux_vecteurs)
        if self.pc:
            for k in range(len(self.liste_textes)):
                self.liste_textes[k].vecteur_pca = nouveaux_vecteurs[k][:max(self.nombre_composantes, len(nouveaux_vecteurs[k]))]
        else:
            for k in range(len(self.liste_textes)):
                self.liste_textes[k].vecteur_pca = vecteurs[k][:max(self.nombre_composantes, len(nouveaux_vecteurs[k]))]
        vecteurs_training = np.array([t.vecteur_pca for t in self.training_set])
        auteurs_training = np.array([t.auteur for t in self.training_set])
        vecteurs_eval = np.array([t.vecteur_pca for t in self.eval_set])
        auteurs_eval = np.array([t.auteur for t in self.eval_set])
        clf = SVC(kernel = self.kernel, gamma=self.gamma, C=self.C)
        clf.fit(vecteurs_training, auteurs_training)
        self.precision = clf.score(vecteurs_eval, auteurs_eval)
        n = len(self.eval_set)
        classification = []
        for t in self.eval_set:
            auteur_reel = t.auteur
            auteur_suppose = clf.predict([t.vecteur_pca])[0]
            classification.append((t,auteur_reel,auteur_suppose))
        self.classification = classification
        self.clusters = classification_to_clusters(self.classification)
        self.p, self.p_ref = classification_to_matrices(self.classification)


    def afficher(self):
        print("Résultats du classifieur SVM sur le corpus étudié :")
        print("Précision : " + str(self.precision))
