from time import time
import sys
sys.path.append("/Users/Lucile/Documents/PSC/programmes_git/psc")
from carac_gramm import *
from carac_lettres import *
from carac_ponct import *
from carac_complexite import *
from carac_stopwords import *
from classes import Analyseur, Probleme
from Clustering.kmeans import Kmeans
from Apprentissage.reseau_textes import reseau_neurones
from Apprentissage.svm import SVM
from Interpretation.importance_composantes import importance, gain_information
from Apprentissage.Bayes import Bayes


d = time()

id_training_set =[[("anne_reeve_aldrich_",1), ("belle_kendrick_abbott_",1), ("eleanor_hallowell_abbot_",1), ("mary_ashley_townsend_",1),("gertrude_atherton_",1),("elizabeth_stuart_phelps_ward_",1),("edwina_stanton_babcock_",1),("bernie_babcock_",1),("madeline_leslie_",1),("faith_baldwin_",1),("mary_bamford_",1),("lucille_van_slyke_",1),("edith_bancroft_",1),("anna_maynard_barbour_",1),("grace_livingston_hill_",1),("barnette_miller_",1),("frances_sterrett_",1),("willa_cather_",1),("laura_richards_",1),("katharine_ellis_barrett_",1),("harriet_caswell_",1),("mary_hallock_foote_",1),("sara_ware_basset_",1),("kathleen_thompson_norris_",1),("jacob_abbott_",1),("horatio_alger_",1),("mark_twain_",1),("george_washington_cable_",1),("robert_chambers_",1),("john_coryell_",1),("stephen_crane_",1),("francis_marion_crawford_",1),("howard_roger_garis_",1),("zane_grey_",1),("harry_castlemon_",1),("joel_chandler_harris_",1),("bret_harte_",1),("howard_pyle_",1),("franck_norris_",1),("herman_melville_",1),("mayne_reid_",1),("henry_james_",1),("william_dean_howells_",1),("oliver_wendell_holmes_",1),("edward_stratemeyer_",1),("charles_warren_stoddard_",1),("frank_richard_stockton_",1),("morgan_robertson_",1),("paschal_beverly_randolph_",1) ], [("louisa_may_alcott_",k) for k in range(1,16)]]
categories = ["categorie1"] + ["categorie2"]
id_eval_set = [[("elmer_boyd_smith_",1)] ,[("william_nelson_taft_",1)]]
categories_supposees = ["categorie1"] + ["categorie2"]

taille_morceaux = 5000

a1 = Freq_Gram(langue = "fr")
a2 = Markov_Gram(langue = "fr",saut = 1)
a3 = Freq_Ngrammes(langue = "fr",n=1)
a4 = Markov_Lettres(langue = "fr")
a5 = Freq_Ponct(langue = "fr")
a6 = Longueur_Phrases()
a7 = Complexite_Grammaticale(langue = "fr", saut= 1)
a8 = Complexite_Vocabulaire()


liste_fonctions = [a1,a2,a3,a4,a5,a6,a7,a8]
#liste_fonctions = [a1,a5]
analyseur = Analyseur(liste_fonctions)
classifieur = SVM()

P = Probleme(id_training_set, categories, id_eval_set, categories_supposees, taille_morceaux, analyseur, classifieur, langue = "fr")

#P.resoudre()

# equivalent à

P.creer_textes()
P.analyser()
P.appliquer_classifieur()
P.interpreter()
P.afficher()
P.evaluer()
#P.afficher_graphique()

f = time()
print()
print("Temps d'exécution : " + str(f-d) + "s")