class Arbre:
    def __init__(self, nom, liste_fils):
        self.nom = nom
        self.fils = liste_fils


    def noms_composantes(self):
        res = []
        for f in self.fils:
            res += f.noms_composantes()
        return res

    def noms_fonctions(self):
        res = []
        for f in self.fils:
            res += f.noms_fonctions()
        return res

    def aux_numeroter(self, n):
        self.init = n
        for f in self.fils:
            n = f.aux_numeroter(n)
        self.end = n
        return self.end

    def numeroter(self):
        self.aux_numeroter(0)


class Feuille(Arbre):
    def __init__(self, nom, liste_composantes):
        super(Feuille, self).__init__("",[])
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

f1 = Feuille("Feuille 1", list(range(10)))
f2 = Feuille("Feuille 2",[10])
f3 = Feuille("Feuille 3",[11,12])
f4 = Feuille("Feuille 4",[13,14,15])
f5 = Feuille("Feuille 5",[16])

a12 = Arbre("1+2",[f1,f2])
a3 = Arbre("3",[f3])
a = Arbre("Père",[a12,a3,f4,f5])
a.numeroter()
print(a.init)
print(a.end)
print(f4.init)
print(f4.end)