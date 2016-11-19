import numpy as np

def distance(texte1, texte2):
    """ Distance entre les textes passés en arguments """
    
    return np.linalg.norm(texte1.vecteur - np.array(texte2.vecteur))

def distance_clusters_SL(textes,p,i,j):
    """ Distance single-linkage entre les clusters i et j """
    m=float("inf")
    for k in np.where(p[:,i] ==1)[0]:
        for l in np.where(p[:,j] ==1)[0]:
            m = min(m,distance(textes[k],textes[l]))
    return m

def huberts_externe(textes,p,p_ref):
    """ Statistique de Huberts externe pour la partition p avec la partition p_ref en référence"""
    N = len(textes)
    M = N*(N-1)/1

    num_clusters = [np.where(p[i] ==1)[0][0] for i in range(N)]
    num_clusters_ref = [np.where(p_ref[i] ==1)[0][0] for i in range(N)]
    
    gamma = 0
    for i in range(N):
        for j in range(i+1,N):
            gamma += distance_clusters_SL(textes,p,num_clusters[i],num_clusters[j]) * distance_clusters_SL(textes,p_ref,num_clusters_ref[i],num_clusters_ref[j])
    return gamma/M

def calcul_taux(textes,p,p_ref):
    """ Calcul des taux de liaisons et non-liaisons correctes et incorrectes """
    N = len(textes)
    num_clusters = [np.where(p[i] ==1)[0][0] for i in range(N)]
    num_clusters_ref = [np.where(p_ref[i] ==1)[0][0] for i in range(N)]
    
    a = 0 # liaisons correctes
    b = 0 # liaisons incorrectes
    c = 0 # non-liaisons incorrectes
    d = 0 # non_liaisons correctes
    
    for i in range(N):
        for j in range(i+1,N):
            if num_clusters[i] == num_clusters[j]:
                if num_clusters_ref[i] == num_clusters_ref[j]:
                    a+=1
                else:
                    b+=1
            if num_clusters_ref[i] == num_clusters_ref[j] and num_clusters[i] != num_clusters[j]:
                c+=1
            if num_clusters_ref[i] != num_clusters_ref[j] and num_clusters[i] != num_clusters[j]:
                d+=1
    
    return a,b,c,d

def rand(textes,p,p_ref):
    """ Calcul de l'indice de Rand"""
    a,b,c,d = calcul_taux(textes,p,p_ref)
    return (a+d)/(a+b+c+d)

def jaccard(textes,p,p_ref):
    """ Calcul de l'indice de Jaccard"""
    a,b,c,d = calcul_taux(textes,p,p_ref)
    den = a+b+c
    if den>0:
        return a/den
    else:
        return 0
    
def fowlkes_mallows(textes,p,p_ref):
    """ Calcul de l'indice de Fowlkes et Mallows"""
    a,b,c,d = calcul_taux(textes,p,p_ref)
    den = np.sqrt((a+b)*(a+c))
    if den>0:
        return a/den
    else:
        return 0

def entropie(textes,p,p_ref):
    """ Calcul de la pureté """
    N = len(textes)
    e = 0
    
    for i in range(len(p[0])):
        s = 0
        ci = set(np.where(p[:,i] == 1)[0])
        if len(ci)>0:
            for j in range(len(p_ref[0])):
                cj = set(np.where(p_ref[:,j] == 1)[0])
                pj = len(cj.intersection(ci))/len(ci)
                if pj !=0:
                    s+= pj*np.log(pj)
        e -= len(ci) * s
    return e/N      
