#########################################
# Importations
#########################################

from stanza_parseTree import *
import json

#########################################
# Importations des fichiers .json
#########################################


with open("pole-ia_NLP/dataset/json/DATA.json") as file:
    DATA_dict = json.load(file)
    DATA = DATA_dict["rules"]

with open("pole-ia_NLP/dataset/json/data2.json") as file:
    DATA_dict = json.load(file)
    data2 = DATA_dict["rules"]

with open("pole-ia_NLP/dataset/json/data3.json") as file:
    DATA_dict = json.load(file)
    data3 = DATA_dict["rules"]

with open("pole-ia_NLP/dataset/json/dataset.json") as file:
    DATA_dict = json.load(file)
    dataset = DATA_dict["rules"]

with open("pole-ia_NLP/dataset/json/electrical_box.json") as file:
    DATA_dict = json.load(file)
    electrical_box = DATA_dict["rules"]

with open("pole-ia_NLP/dataset/json/football_rule.json") as file:
    DATA_dict = json.load(file)
    footbal_rule = DATA_dict["rules"]

with open("pole-ia_NLP/dataset/json/Dense_Dataset.json") as file:
    DATA_dict = json.load(file)
    Dense_Dataset = DATA_dict["rules"]

with open("pole-ia_NLP/dataset/json/Musique_classique_rules.json") as file:
    DATA_dict = json.load(file)
    Musique_classique_rules = DATA_dict["rules"]

with open("pole-ia_NLP/dataset/json/Rules_of_grammar.json") as file:
    DATA_dict = json.load(file)
    Rules_of_grammar = DATA_dict["rules"]

with open("pole-ia_NLP/dataset/json/Sport_rules.json") as file:
    DATA_dict = json.load(file)
    Sport_rules = DATA_dict["rules"]

#########################################
# Fonction de comparaison
#########################################


def compare_lists(l1, l2):
    """
    Entrée : deux listes de mots, l1 liste en sortie de l'algorithme, l2 liste de mots de référence pour la cause/conséquence
    Sortie : un réel indiquant le pourcentage de ressemblance entre les mots de chaque liste (vrai positif et faux positif) 
    """
    if l1 == None:
        l1 = ''
    if l2 == None:
        l2 = ''
    n1 = len(l1)
    n2 = len(l2)

    # Si jamais les deux listes sont vides
    if n1 == n2 and n2 == 0:
        return 1

    # Sinon on considère l'intersection
    set1 = set(l1)
    set2 = set(l2)

    #
    z = set1.intersection(set2)
    x = set1 - set2

    # On retournne le taux de vrai positif et le taux de faux positif
    return [len(z)/n2, len(x)/n2]


def test_compare_lists(sentence, cause):
    """
    Fonction test de la comparaison
    Entrée : une phrase et une cause
    Sortie : affiche le pourcentage de ressemblance, et un couple (cause renseignée, cause renvoyée par l'algo)
    """

    cause = cause.split()
    cause_algo = identify_cause(sentence)
    print(cause)
    print(cause_algo)
    print(compare_lists(cause, cause_algo))


#test_compare_lists("Also, make a note if the beeps repeat","if the beeps repeat")


def compare(text):
    """
    Entrée : règles du dataset sous forme de liste de dictionnaires (texte, condition, conséquence)
    Sortie : print les causes et conséquences de l'algorithme par recherche syntaxique et du dataset
    """

    for s in text:
        print("\n"+"Phrase à traiter :", s["text"])
        print("\n"+"L'algo renvoie")
        cause_consequence(s["text"])
        print("\n" + "Le dataset propose :")
        print("cause du dataset :", s["condition"])
        print("consequence du dataset :", s["consequence"])
        print("\n")


# compare(Rules_of_grammar)


def pourcentage_ressemblance(text):
    """
    Entrée : règles du dataset sous forme de liste de dictionnaires (texte, condition, conséquence)
    Sortie : pourcentage de mots en commun entre les causes/conséquences du dataset et de l'ago de recherche syntaxique
    """
    s_cause = [0, 0]
    s_conséquence = [0, 0]
    M = len(text)
    for s in text:
        l = list_cause_consequence(s["text"])
        l1 = l[0]
        l2 = s["condition"].split()

        l3 = l[1]
        l4 = s["consequence"].split()

        # On somme les pourcentages
        ca = compare_lists(l1, l2)
        co = compare_lists(l3, l4)

        s_cause[0] += ca[0]
        s_cause[1] += ca[1]
        s_conséquence[0] += co[0]

        # On oublie les cas extrêmes, on ne prend pas en compte les cas où le score de fausse conséquence est trop élevé
        if co[1] < 2:
            s_conséquence[1] += co[1]

    # On divise par le nombre de listes comparées
    s_cause[0] = (s_cause[0]/M)*100
    s_cause[1] = (s_cause[1]/M)*100
    s_conséquence[0] = (s_conséquence[0]/M)*100
    s_conséquence[1] = (s_conséquence[1]/M)*100

    # On affiche les résultats
    print("\n")
    print("Pourcentage vrai cause :", s_cause[0])
    print("Pourcentage fausse cause :", s_cause[1])
    print("Pourcentage vrai conséquence :", s_conséquence[0])
    print("Pourcentage fausse conséquence :", s_conséquence[1])
    print("\n")

    return s_cause, s_conséquence


# pourcentage_ressemblance(Sport_rules)

#########################################
# Résultats des comparaisons
#########################################

##
# Dense_Dataset
##

# POURCENTAGES : [94,9,  9,2] et [95,9,  27,7]


##
# Musique_classique
##

# POURCENTAGES : [71,2,  12,3] et [94,6,  50,4]


##
# Rules_of_grammar
##

# POURCENTAGES : [64,1,  22,9] et [85,5,  25,8]


##
# Sport_rules
##

# POURCENTAGES : [55,5,  23] et [90,3, 42,7]
