import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
ax1.add_patch(
    patches.Rectangle(
        (0.1, 0.1),   # (x,y)
        0.5,          # width
        0.5,          # height
        color = (1,0,0), # r g b
    )
)
fig1.canvas.draw()
plt.show()

def barycentre(vecteurs,p,i):
    d = len(vecteurs[0])
    idx = np.where(p[:,i] ==1)[0]
    s = np.zeros((d))
    for j in idx:
        s+=vecteurs[j]
    return s/len(idx)


def variance_cluster(vecteurs,p,i):
    s = barycentre(vecteurs,p,i)
    idx = np.where(p[:,i] ==1)[0]
    v = sum([np.linalg.norm(textes[j].vecteur - s)**2 for j in idx])
    return v

def intensité(textes,p,i):
    def f(x,y):
        N = len(textes)
        v = variance(textes,p,i)
        s = 0
        res = 0
        for i in range(N):
            res += laplace((x-textes.vecteur
            
        
    