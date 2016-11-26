from scipy.spatial import distance
from numpy import sqrt
from classes import Oeuvre,Texte,Analyseur,Classifieur,Probleme
from carac import plus_courants, freq_gram


test=[(2,1),(2,2),(3,2),(1,3),(2,3),(3,3),(5,6),(7,6),(7,7),(6,8),(2,6),(7,2),(6,3),(6,2)]

def coreDistance (p,eps,Minpts,Points) : #distance au Minpts ième point le plus proche
    v=voisinage(p,eps,Points)
    if len(v)<Minpts :
        return None
    else :
        d=sorted([distance.euclidean(n[0].vecteur,p[0].vecteur) for n in v])
        return d[Minpts-1]

def voisinage (p,eps,Points) : #points à moins de eps de p
    N=[]
    for n in Points :
        if n!=p and distance.euclidean(p[0].vecteur,n[0].vecteur) <= eps :
            N.append(n)
    return N        



def update (N,p,F,eps,Minpts,Points) : #met à jour les reachability-distances des points non encore visités
    coreDist=coreDistance(p,eps,Minpts,Points)
    for o in N :
        if not o[1] :
            newReachDist=max(coreDist,distance.euclidean(p[0].vecteur,o[0].vecteur))
            if o[2]==None :
                o[2]=newReachDist
                F.append(o)
            else :
                if newReachDist<o[2] :
                        o[2]=newReachDist



def optics (liste_textes,eps,Minpts) :
    L=[]
    Points=[[p,False,None] for p in liste_textes] #p[0] contient l'objet texte, p[1] est False car p n'a pas été visité, p[2] est la reachability-distance de p
    #print("\n","Points=",Points)
    for p in Points :
        #print(p[1])
        if not p[1] :  
            N=voisinage(p,eps,Points)
            p[1]=True
            L.append((p[0],p[2])) 
            if coreDistance(p,eps,Minpts,Points)!=None : #si p a assez de voisins, on les ajoute à la file et on définit leur reachability-distance
                File=[]
                update(N,p,File,eps,Minpts,Points)
                while len(File)>0 :
                    File.sort(key=lambda q: q[2]) 
                    q=File.pop(0)  #on examine le voisin non visité avec la reachability-distance la plus faible
                    N2=voisinage(q,eps,Points)
                    q[1]=True
                    L.append((q[0],q[2]))
                    if coreDistance(q,eps,Minpts,Points)!=None : #si q a assez de voisins, on met à jour leur reachability-distance et on les ajoute à la file
                        update(N2,q,File,eps,Minpts,Points)
    print("\n","L=",L)
    return L     #retourne une liste de couples (texte,reachability-distance) ordonnée dans l'ordre de visite des points/textes par l'algorithme                


def auteur_dominant (clus) :
    A=[] #auteurs
    Occ=[] #occurrences correspondantes
    for t in clus :
        if t.auteur in A :
            Occ[A.index(t.auteur)]+=1
        else :
            A.append(t.auteur)
            Occ.append(1)
    return A[Occ.index(max(Occ))]            


def cluster_d_appartenance (texte,liste_clusters) :
    ind_clus=len(liste_clusters)
    for c in enumerate(liste_clusters) :
        if texte in c[1] :
            ind_clus=c[0]
    return ind_clus        


def defclusters (liste_textes,eps,Minpts,sep) :
    L=optics(liste_textes,eps,Minpts)
    S=[] #séparareurs
    C=[] #clusters
    for i in range (len(L)) :
        rd=L[i][1] if L[i][1] else float('infinity')
        if rd>sep : #les points ayant une reachability-distance trop élevée sont des séparateurs
            S.append(i)
    S.append(len(L))        
    for i in range (len(S)-1) :
             if S[i+1]-S[i]>Minpts : #si un groupe de points dépasse la taille critique, c'est un cluster
                 cluster=L[S[i]:S[i+1]]
                 C.append([p[0] for p in cluster])
    #print(S)
    Auteurs=[0]*(len(C)+1)
    for j in range (len(C)) :
        Auteurs[j]=auteur_dominant(C[j])
    Auteurs[len(C)]="auteur non attribué"    
    PartitionFloue=[[0]*(len(C)+1) for i in range (len(liste_textes))]
    for i in range (len(liste_textes)) :
        PartitionFloue[i][cluster_d_appartenance(liste_textes[i],C)]=1
    print([[t.auteur for t in C[j]] for j in range(len(C))],sum([PartitionFloue[i][len(C)] for i in range(len(liste_textes))]))   
    return Auteurs,PartitionFloue           
    
class OPTICS(Classifieur):
    
    def __init__(self):
        print("Création du classifieur OPTICS")
        pass
    
    def classifier(self, training_set, eval_set):
        #paramètres Proust/Hugo
        eps=0.03
        Minpts=5
        sep=0.025
        liste_textes=training_set+eval_set
        return defclusters(liste_textes, eps, Minpts, sep)
    











