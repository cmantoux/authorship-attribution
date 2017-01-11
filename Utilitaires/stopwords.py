from nltk.corpus import stopwords

def stopwords_en():
    return stopwords.words("english")

def stopwords_fr():
    return stopwords.words("french")

def stopwords_en2():
    with open("stopwords_en.txt", "r") as fichier:
        s = fichier.read()
    return s.split()
    
def stopwords_fr2():
    with open("stopwords_fr.txt", "r") as fichier:
        s = fichier.read()
    return s.split()

def stopwords_zh():
    return stopwords.words("chinese")
    
def stopwords_zh2():
    with open("stopwords_zh.txt", "r") as fichier:
        s = fichier.read()
    return s.split()