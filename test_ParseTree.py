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

#########################################
# Fonction de comparaison
#########################################


def compare_lists(l1, l2):
    """
    Entrée : deux listes de mots
    Sortie : un réel indiquant le pourcentage de ressemblance entre les mots de chaque liste 
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
    z = set1.intersection(set2)

    return (len(z)*2)/(n1+n2)


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


compare(footbal_rule)


def pourcentage_ressemblance(text):
    """
    Entrée : règles du dataset sous forme de liste de dictionnaires (texte, condition, conséquence)
    Sortie : pourcentage de mots en commun entre les causes/conséquences du dataset et de l'ago de recherche syntaxique
    """
    p = 0
    M = len(text)
    for s in text:
        l = list_cause_consequence(s["text"])
        l1 = l[0]
        l2 = s["condition"].split()

        l3 = l[1]
        l4 = s["consequence"].split()

        # On somme les pourcentages
        p += compare_lists(l1, l2)+compare_lists(l3, l4)

    # On divise par le nombre de listes comparées
    return p/(2*M)*100


print(pourcentage_ressemblance(footbal_rule))

#########################################
# Résultats des comparaisons
#########################################

##
# DATA (non viable)
##

# POURCENTAGE : 26,8%


##
# data2 (viable)
##

# POURCENTAGE 47,8%


##
# data3 (non viable)
##

# POURCENTAGE 23,3%


##
# dataset (non viable)
##

# POURCENTAGE 29,9


##
# electrical_box (non viable)
##

# POURCENTAGE 26%


##
# footaball_rule
##

# POURCENTAGE 27%
