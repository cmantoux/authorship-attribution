import sqlite3
conn = sqlite3.connect('textes.db')
cursor = conn.cursor()

def InsererFichier(fichier, nom, annee, genre, auteur, naissance, sexe, langue, pays, corpus, commentaires):
    an = str(annee)
    ne = str(naissance)
    values = "('"+fichier+"','"+ nom+"',"+ an+",'"+ genre+"','"+ auteur+"',"+ ne+",'"+ sexe+"','"+ langue+"','"+ pays+"','"+corpus+"','"+commentaires+"')"
    query = "INSERT INTO textes (fichier, nom, annee, genre, auteur, naissance, sexe, langue, pays, corpus, commentaires) VALUES "+values
    cursor.execute(query)
    conn.commit()

def AfficherTable():
    cursor.execute("""SELECT * FROM textes""")
    table = ['']
    for row in cursor:
        print('{0} : {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
        table.append('{0} : {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
    return table

def AfficherFichier(champ, valeur_champ):
    if(champ=="annee" or champ=="naissance"):
        query = "SELECT * FROM textes WHERE "+champ+" = "+str(valeur_champ)
    else:
        query = "SELECT * FROM textes WHERE "+champ+" = '"+valeur_champ+"'"
    cursor.execute(query)
    table = ['']
    for row in cursor:
        print('{0} : {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
        table.append('{0} : {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
    return table

def InfosFichier(fichier):
    query = "SELECT * FROM textes WHERE fichier = '"+fichier+"'"
    cursor.execute(query)
    for row in cursor:
        return row

        
        
def ModifierFichier(fichier, champ_modif, valeur_champ_modif):
    if(champ_modif=="annee" or champ_modif=="naissance"):
        query = "UPDATE textes SET "+champ_modif+" = "+str(valeur_champ_modif)+"  WHERE fichier = '"+fichier+"'"
    else:
        query = "UPDATE textes SET "+champ_modif+" = '"+valeur_champ_modif+"'  WHERE fichier = '"+fichier+"'" 
    cursor.execute(query)
    conn.commit()

def SelectionnerFichiers(fichier, nom, annee_debut, annee_fin, genre, auteur, naissance_debut, naissance_fin, sexe, langue, pays, corpus):
    values = ""
    if(fichier != None):
        values += "fichier = '"+fichier+"'"
    if(nom != None):
        if(values == ""):
            values += "nom = '"+nom+"'"
        else:
            values += " AND nom = '"+nom+"'"
    if(annee_debut != None and annee_fin != None):
        if(values == ""):
            values += "annee >= "+str(annee_debut)+" AND annee <= "+str(annee_fin)
        else:
            values += " AND annee >= "+str(annee_debut)+" AND annee <= "+str(annee_fin)
    elif(annee_debut != None):
        if(values == ""):
            values += "annee >= "+str(annee_debut)
        else:
            values += " AND annee >= "+str(annee_debut)
    elif(annee_fin != None):
        if(values == ""):
            values += "annee <= "+str(annee_fin)
        else:
            values += " AND annee <= "+str(annee_fin)
    if(genre != None):
        if(values == ""):
            values += "genre = '"+genre+"'"
        else:
            values += " AND genre = '"+genre+"'"
    if(auteur != None):
        if(values == ""):
            values += "auteur = '"+auteur+"'"
        else:
            values += " AND auteur = '"+auteur+"'"
    if(naissance_debut != None and naissance_fin != None):
        if(values == ""):
            values += "naissance >= "+str(naissance_debut)+" AND naissance <= "+str(naissance_fin)
        else:
            values += " AND naissance >= "+str(naissance_debut)+" AND naissance <= "+str(naissance_fin)
    elif(naissance_debut != None):
        if(values == ""):
            values += "naissance >= "+str(naissance_debut)
        else:
            values += " AND naissance >= "+str(naissance_debut)
    elif(naissance_fin != None):
        if(values == ""):
            values += "naissance <= "+str(naissance_fin)
        else:
            values += " AND naissance <= "+str(naissance_fin)
    if(sexe != None):
        if(values == ""):
            values += "sexe = '"+sexe+"'"
        else:
            values += " AND sexe = '"+sexe+"'"
    if(langue != None):
        if(values == ""):
            values += "langue = '"+langue+"'"
        else:
            values += " AND langue = '"+langue+"'"
    if(pays != None):
        if(values == ""):
            values += "pays = '"+pays+"'"
        else:
            values += " AND pays = '"+pays+"'"
    if(corpus != None):
        if(values == ""):
            values += "corpus = '"+corpus+"'"
        else:
            values += " AND corpus = '"+corpus+"'"
    if(values!=""):
        query = "SELECT * FROM textes WHERE "+values
    else:
        query = "SELECT * FROM textes"
    cursor.execute(query)
    table = ['']
    for row in cursor:
        print('{0} : {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
        table.append('{0} : {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))
    return table
    

#bcp plus de résultats pour gertrude atherton sur le projet gutenberg

#InsererFichier("anne_reeve_aldrich_1", "A Village Ophelia", 1899, "Roman", "Anne Reeve Aldrich", 1866, "F", "English", "USA", "genre", "Publié à titre posthume (auteur morte en 1892)")
#InsererFichier("belle_kendrick_abbott_1", "Leah Mordecai", 1875, "Roman", "Belle Kendrick Abbott", 1842, "F", "English", "USA", "genre", "")    
#InsererFichier("eleanor_hallowell_abbot_1", "Peace on Earth, Good-will to Dogs ", 1920, "Roman", "Eleanor Hallowell Abbott", 1872, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_1", "Little Women", 1868, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_2", "Little men: life at Plumfield with Jo's Boys", 1871, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_3", "An Old-fashioned Girl", 1870, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_4", "Jo's boys", 1886, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_5", "Eight Cousins", 1875, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_6", "Rose in Bloom : A Sequel to Eight Cousins", 1876, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_7", "Little Women or Meg, Jo, Beth, and Amy", 1868, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "le texte comprend des phrases du type '[Illustration: A little figure in cloudy white]' qui ne sont pas de la main de l'auteur")
#InsererFichier("louisa_may_alcott_8", "Flower Fables", 1854, "Nouvelles pour enfants", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_9", "Work: A Story of Experience", 1872, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_10", "Jack and Jill", 1880, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_11", "Behind A Mask, Or A Woman’s Power", 1866, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_12", "The Mysterious Key And What It Opened", 1867, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_13", "Hospital Sketches", 1863, "Nouvelles", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_14", "Under the Lilacs", 1878, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("louisa_may_alcott_15", "A Garland for Girls", 1888, "Roman", "Louisa May Alcott", 1832, "F", "English", "USA", "genre", "")
#InsererFichier("mary_ashley_townsend_1", "The Brother Clerks", 1859, "Roman", "Mary Ashley Townsend", 1836, "F", "English", "USA", "genre", "")
#InsererFichier("gertrude_atherton_1", "Black Oxen", 1923, "Roman", "Gertrude Franklin Horn Atherton", 1857, "F", "English", "USA", "genre", "")
#InsererFichier("elizabeth_stuart_phelps_ward_1", "Avery", 1902, "Roman", "Elizabeth Stuart Phelps Ward", 1844, "F", "English", "USA", "genre", "")
#InsererFichier("edwina_stanton_babcock_1", "Under the Law", 1923, "Roman", "Edwina Stanton Babcock", 1875, "F", "English", "USA", "genre", "")
#InsererFichier("bernie_babcock_1", "The Coming of the King", 1921, "Roman", "Julia Burnelle Smade Babcock", 1868, "F", "English", "USA", "genre", "")
#InsererFichier("madeline_leslie_1", "Little Frankie and his Mother", 1860, "Roman", "Harriette Newell Woods Baker", 1815, "F", "English", "USA", "genre", "livre pour enfant")
#InsererFichier("faith_baldwin_1", "Mavis of Green Hill", 1921, "Roman", "Faith Baldwin", 1893, "F", "English", "USA", "genre", "")
#InsererFichier("mary_bamford_1", "Out of the Triangle: a Story of the Far East.", 1898, "Roman", "Mary Ellen Bamford", 1857, "F", "English", "USA", "genre", "")
#InsererFichier("lucille_van_slyke_1", "Little Miss By-The-Day", 1919, "Roman", "Lucille Van Slyke", 1880, "F", "English", "USA", "genre", "")
#InsererFichier("edith_bancroft_1", "Jane Allen: Right Guard", 1918, "Roman", "Edith Bancroft", 1888, "F", "English", "USA", "genre", "La date de naissance de l'auteure est hasardeuse")
#InsererFichier("anna_maynard_barbour_1", "At the Time Appointed", 1903, "Roman", "Anna Maynard Barbour", 1870, "F", "English", "USA", "genre", "La date de naissance de l'auteure est inconnue, j'ai mis 1870 car elle s'est mariée en 1893")
#InsererFichier("grace_livingston_hill_1", "The Enchanted Barn", 1918, "Roman", "Grace Livingston Hill", 1865, "F", "English", "USA", "genre", "")
#InsererFichier("barnette_miller_1", "Leigh Hunt's Relations with Byron, Shelley and Keats", 1910, "Roman", "Barnette Miller", 1852, "F", "English", "USA", "genre", "")
#InsererFichier("frances_sterrett_1", "Mary Rose of Mifflin", 1916, "Roman", "Frances R. Sterrett", 1869, "F", "English", "USA", "genre", "")
#InsererFichier("willa_cather_1", "Alexander's Bridge", 1912, "Roman", "Wilella (Willa) Sibert Cather", 1873, "F", "English", "USA", "genre", "")
#InsererFichier("laura_richards_1", "Fernley House", 1901, "Roman", "Laura Elizabeth Howe Richards", 1850, "F", "English", "USA", "genre", "")
#InsererFichier("katharine_ellis_barrett_1", "The Wide awake girls in Winsted", 1909, "Roman", "Katharine Ellis Barrett", 1879, "F", "English", "USA", "genre", "")
#InsererFichier("harriet_caswell_1", "The Path of Duty, and Other Stories", 1874, "Roman", "Harriet S. Caswell", 1874, "F", "English", "USA", "genre", "")
#InsererFichier("mary_hallock_foote_1", "In Exile and Other Stories", 1894, "Roman", "Mary Hallock Foote", 1847, "F", "English", "USA", "genre", "")
#InsererFichier("sara_ware_basset_1", "Flood Tide", 1921, "Roman", "Sara Ware Bassett", 1871, "F", "English", "USA", "genre", "")
#InsererFichier("kathleen_thompson_norris_1", "Poor, Dear Margaret Kirby", 1913, "Roman", "Kathleen Thompson Norris", 1880, "F", "English", "USA", "genre", "")
#InsererFichier("jacob_abbott_1", "Bruno or, lessons of fidelity, patience, and self-denial taught by a dog", 1854, "Roman", "Jacob Abbott", 1803, "M", "English", "USA", "genre", "")
#InsererFichier("horatio_alger_1", "Ragged Dick, Or, Street Life in New York with the Boot-Blacks", 1867, "Roman", "Horatio Alger", 1832, "M", "English", "USA", "genre", "")
#InsererFichier("mark_twain_1", "The Adventures of Tom Sawyer", 1876, "Roman", "Samuel Langhorne Clemens", 1835, "M", "English", "USA", "genre", "")
#InsererFichier("george_washington_cable_1", "Madame Delphine", 1881, "Roman", "George Washington Cable", 1844, "M", "English", "USA", "genre", "")
#InsererFichier("robert_chambers_1", "The Laughing Girl", 1918, "Roman", "Robert Williams Chambers", 1865, "M", "English", "USA", "genre", "")
#InsererFichier("john_coryell_1", "Diego Pinzon and the Fearful Voyage he took into the Unknown Ocean A.D. 1492", 1892, "Roman", "John R. Coryell", 1851, "M", "English", "USA", "genre", "")
#InsererFichier("stephen_crane_1", "Maggie: A Girl of the Streets", 1893, "Roman", "Stephen Crane", 1871, "M", "English", "USA", "genre", "")
#InsererFichier("francis_marion_crawford_1", "The Witch of Prague: A Fantastic Tale", 1891, "Roman", "Francis Marion Crawford", 1854, "M", "English", "USA", "genre", "")
#InsererFichier("howard_roger_garis_1", "Uncle Wiggily and Old Mother Hubbard", 1922, "Roman", "Howard Roger Garis", 1873, "M", "English", "USA", "genre", "")
#InsererFichier("zane_grey_1", "The Mysterious Rider", 1922, "Roman", "Zane Grey", 1872, "M", "English", "USA", "genre", "")
#InsererFichier("harry_castlemon_1", "Frank Nelson in the Forecastle, or, the Sportsman s Club Among the Whalers", 1876, "Roman", "Charles Austin Fosdick", 1842, "M", "English", "USA", "genre", "")
#InsererFichier("joel_chandler_harris_1", "Little Mr. Thimblefinger and His Queer Country", 1894, "Roman", "Joel Chandler Harris", 1848, "M", "English", "USA", "genre", "")
#InsererFichier("bret_harte_1", "The Queen of the Pirate Isle", 1885, "Roman", "Francis Bret Harte", 1836, "M", "English", "USA", "genre", "")
#InsererFichier("howard_pyle_1", "The Ruby of Kishmoor", 1908, "Roman", "Howard Pyle", 1853, "M", "English", "USA", "genre", "")
#InsererFichier("franck_norris_1", "A Man s Woman", 1900, "Roman", "Benjamin Franklin Norris Jr.", 1870, "M", "English", "USA", "genre", "")
#InsererFichier("herman_melville_1", "Moby Dick", 1851, "Roman", "Herman Melville", 1819, "M", "English", "USA", "genre", "")
#InsererFichier("mayne_reid_1", "The Quadroon", 1856, "Roman", "Thomas Mayne Reid", 1818, "M", "English", "USA", "genre", "")
#InsererFichier("henry_james_1", "The Portrait of a Lady", 1881, "Roman", "Henry James", 1843, "M", "English", "USA", "genre", "")
#InsererFichier("william_dean_howells_1", "The Rise of Silas Lapham", 1885, "Roman", "William Dean Howells", 1837, "M", "English", "USA", "genre", "")
#InsererFichier("oliver_wendell_holmes_1", "Grandmother s Story of Bunker Hill Battle", 1875, "Roman", "Oliver Wendell Holmes", 1809, "M", "English", "USA", "genre", "")
#InsererFichier("edward_stratemeyer_1", "The Rover Boys on the Great Lakes; Or, The Secret of the Island Cave", 1901, "Roman", "Edward Stratemeyer", 1862, "M", "English", "USA", "genre", "")
#InsererFichier("charles_warren_stoddard_1", "Summer Cruising in the South Seas", 1874, "Roman", "Charles Warren Stoddard", 1843, "M", "English", "USA", "genre", "")
#InsererFichier("frank_richard_stockton_1", "Kate Bonnet: The Romance of a Pirate s Daughter", 1902, "Roman", "Frank Richard Stockton", 1834, "M", "English", "USA", "genre", "")
#InsererFichier("morgan_robertson_1", "The Wreck of the Titan", 1898, "Roman", "Morgan Robertson", 1861, "M", "English", "USA", "genre", "")
#InsererFichier("paschal_beverly_randolph_1", "The Wonderful Story of Ravalette", 1863, "Roman", "Paschal Beverly Randolph", 1825, "M", "English", "USA", "genre", "")
#InsererFichier("elmer_boyd_smith_1", "The Story of Pocahontas and Captain John Smith", 1906, "Roman", "Elmer Boyd Smith", 1860, "M", "English", "USA", "genre", "")
#InsererFichier("william_nelson_taft_1", "On Secret Service", 1921, "Roman", "William Nelson Taft", 1835, "M", "English", "USA", "genre", "publié à titre posthume (auteur mort en 1910)")


#InsererFichier("balzac1", "La maison du chat-qui-pelote", 1830, "Nouvelle", "Honoré de Balzac", 1799, "M", "Français", "France", "soutenance", "")
#InsererFichier("balzac2", "Mémoires de deux jeunes mariées", 1830, "Roman épistolaire", "Honoré de Balzac", 1799, "M", "Français", "France", "soutenance", "")
#InsererFichier("balzac3", "La Femme de trente ans", 1842, "Roman", "Honoré de Balzac", 1799, "M", "Français", "France", "soutenance", "")
#InsererFichier("flaubert1", "Madame Bovary", 1857, "Roman", "Gustave Flaubert", 1821, "M", "Français", "France", "soutenance", "")
#InsererFichier("flaubert3", """L’Éducation sentimentale, Partie 1""", 1869, "Roman", "Gustave Flaubert", 1821, "M", "Français", "France", "soutenance", "")
#InsererFichier("flaubert4", """L’Éducation sentimentale, Partie 2""", 1869, "Roman", "Gustave Flaubert", 1821, "M", "Français", "France", "soutenance", "")
#InsererFichier("stendhal1", "Le Rouge et le Noir", 1830, "Roman", "Henri Beyle / Stendhal", 1783, "M", "Français", "France", "soutenance", "")
#InsererFichier("stendhal2", "Le Rouge et le Noir", 1839, "Roman", "Henri Beyle / Stendhal", 1783, "M", "Français", "France", "soutenance", "")


#AfficherTable()



