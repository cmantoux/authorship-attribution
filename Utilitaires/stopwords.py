def stopwords_en():
    """
    :return: liste des stopwords anglais
    :rtype: list
    """
    with open("stopwords_en.txt", "r") as fichier:
        s = fichier.read()
    return s.split()
    
def stopwords_fr():
    with open("stopwords_fr.txt", "r") as fichier:
        s = fichier.read()
    return s.split()