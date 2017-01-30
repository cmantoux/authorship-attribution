import numpy as np

class PCA:
    
    def __init__(self,donnees):
        self.X = donnees
        s = np.shape(self.X)
        self.n = s[0]
        self.p = s[1]
        self.G = self.X.mean(axis = 0)
        self.V = self.X.var(axis = 0)
        self.Xc = self.X - self.G
        self.S = np.cov(np.transpose(self.Xc))
        #e = np.linalg.eig(self.S)
        e2 = np.linalg.svd(self.S)
        #print(e)
        #print(e2)
        v = e2[1]
        w = e2[0]
        unsorted_pairs = [(v[j],w[j]) for j in range(self.p)]
        sorted_pairs = sorted(unsorted_pairs, key = lambda pair : -pair[0])
        self.vals = [pair[0] for pair in sorted_pairs]
        self.vects = [pair[1] for pair in sorted_pairs]
        #print("vecteurs propres")
        #print(self.vects)
        #print("valeurs propres")
        #print(self.vals)
        s = sum(self.vals)
        self.explained_variance = [self.vals[j]/s for j in range(self.p)]
        self.A = np.array(self.vects)
        self.Y = np.dot(self.Xc,np.transpose(self.A))
        
def pca(vecteurs):
    donnees = np.array(vecteurs)
    my_pca = PCA(donnees)
    return my_pca.Y

def pca_matrice(vecteurs):
    donnees = np.array(vecteurs)
    my_pca = PCA(donnees)
    return my_pca.Y, my_pca.A

#p = PCA(vecteurs)