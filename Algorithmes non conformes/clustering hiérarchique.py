# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import random as rd
import numpy as np

def genererNPoints(n):
    t = []
    for i in range(n):
        t.append([rd.random(), rd.random()])
    return t

def genererClusterDiagonal(clusters, tailleCluster):
    t = []
    for i in range(clusters):
        for j in range(tailleCluster):
            t.append([(i+rd.random())/clusters, (i+rd.random())/clusters])
    return t
        

def distancePoints(a,b):
    return np.sqrt(np.square(a[0]-b[0])+np.square(a[1]-b[1]))

def distanceClasses(a,b,methode = "moyenne"):
    distanceMax = 0
    for i in range(len(a)):
        for j in range(len(b)):
            d = distancePoints(a[i], b[j])
            if d>distanceMax:
                distanceMax = d
    return distanceMax

def clusterHierarchique(points, nbClasses):
    classes = []
    for i in range(len(points)):
        #Au début, il y a autant de classes que de points
        classes.append([points[i]])
    #On cherche et on fusionne les classes les plus proches jusqu'à ce qu'il en reste le nombre voulu
    while len(classes)>nbClasses:
        #On cherche les classes les plus proches
        indiceMin = [0,1]
        distanceMin = distanceClasses(classes[0], classes[1])
        for i in range(len(classes)):
            for j in range(i+1, len(classes)):
                d = distanceClasses(classes[i], classes[j])
                if d<distanceMin:
                    indiceMin = [i,j]
                    distanceMin = d

        #On fusionne les classes les plus proches
        i,j = indiceMin[0], indiceMin[1]
        for p in classes[j]:
            classes[i].append(p)
        del classes[j]
    return classes

def afficheClasses(classes):
    nbClasses = len(classes)
    for i in range(nbClasses):
        for j in range(len(classes[i])):
            plt.scatter(classes[i][j][0], classes[i][j][1], s=100, c =(float(i)/nbClasses,0,1-float(i)/nbClasses))
    plt.show()

afficheClasses(clusterHierarchique(genererClusterDiagonal(4,30), 4))






