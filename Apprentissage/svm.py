from sklearn.svm import SVC
from Utilitaires.pca import pca
from classes import *

class SVM(Classifieur):
    
    def __init__(self, pc=True, kernel='rbf', gamma="auto", C=5, nombre_composantes=5000):
        #print("Création du classifieur SVM")
        super().__init__()
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
        self.categories = None
        
    def classification_to_clusters(self):
        clusters = [[]] + [[]]
        for c in self.classification:
            t = c[0]
            categorie_supposee = c[2]
            ind = self.categories.index(categorie_supposee)
            clusters[ind].append(t)
        return clusters
        
    def classification_to_matrices(self):
        nb_textes = len(self.classification)
        nb_categories = len(self.categories)
        p = np.zeros((nb_textes,nb_categories))
        p_ref = np.zeros((nb_textes,nb_categories))
        for i in range(nb_textes):
            item = self.classification[i]
            categorie_reelle = item[1]
            categorie_supposee = item[2]
            p[i,self.categories.index(categorie_supposee)] = 1
            p_ref[i,self.categories.index(categorie_reelle)] = 1
        return p,p_ref
    
    def classifier(self, training_set, eval_set, categories):
        self.liste_textes = training_set + eval_set
        self.training_set = training_set
        self.eval_set = eval_set
        self.categories = categories
        vecteurs = [t.vecteur for t in self.liste_textes]
        nouveaux_vecteurs = pca(vecteurs)
        if self.pc:
            for k in range(len(self.liste_textes)):
                self.liste_textes[k].vecteur_pca = nouveaux_vecteurs[k][:max(self.nombre_composantes, len(nouveaux_vecteurs[k]))]
        else:
            for k in range(len(self.liste_textes)):
                self.liste_textes[k].vecteur_pca = vecteurs[k][:max(self.nombre_composantes, len(nouveaux_vecteurs[k]))]
        vecteurs_training = np.array([t.vecteur_pca for t in self.training_set])
        categories_training = np.array([t.categorie for t in self.training_set])
        clf = SVC(kernel = self.kernel, gamma=self.gamma, C=self.C)
        clf.fit(vecteurs_training, categories_training)
        classification = []
        for t in self.eval_set:
            categorie_reelle = t.categorie
            categorie_supposee = clf.predict([t.vecteur_pca])[0]
            classification.append((t, categorie_reelle, categorie_supposee))
        self.classification = classification
        self.clusters = self.classification_to_clusters()
        self.p, self.p_ref = self.classification_to_matrices()