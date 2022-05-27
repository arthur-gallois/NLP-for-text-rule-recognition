#########################################
# Importations des fichiers .json
#########################################

import stanza

# À décomenter pour la première utilisation de Stanza
# stanza.download('en')
nlp = stanza.Pipeline('en')

#########################################
# Phrases tests
#########################################

s1 = "If the cookies are in the oven, start it"
s2 = "When the cookies are in the oven, start it"
s3 = "Start the oven unless the cookies aren’t in "
s4 = "You should start the oven because the cookies are in "
s5 = "Unless the cookies aren’t in the oven, start it"
s6 = "Always use oven mitts or pot holders when removing dishes from the microwave oven. "
s7 = "Carefully attend the microwave oven if paper, plastic, or other combustible materials are placed inside the oven to facilitate cooking. "
s8 = "If food is foil wrapped, remove foil and place it in a suitable container. "
s9 = "If defrosted food is still icy in the center, return it to the microwave oven for more defrosting."
s10 = "Start the oven provided that the cookies are in "
s11 = "Keep the oven hot while cookies are in. "
s12 = "Keep the oven hot as long as cookies are in. "

doc1 = nlp(s1)
doc2 = nlp(s2)
doc3 = nlp(s3)
doc4 = nlp(s4)
doc5 = nlp(s5)
doc6 = nlp(s6)
doc7 = nlp(s7)

test1 = nlp(
    "Use extreme care when inserting a spoon or other utensil into the container.")
test2 = nlp("Carefully attend the microwave oven if paper, plastic, or other combustible materials are placed inside the oven to facilitate cooking. ")

test3 = nlp(
    "Always use oven mitts or pot holders when removing dishes from the microwave oven. ")

#########################################
# Fonctions utiles pour la manipulation d'arbre syntaxique
#########################################


def is_final(tree):
    """
    Renvoie un booléen indiquant si l'arbre syntaxique n'a pas de fils
    """

    return str(tree)[0] != '('


def test_is_final():
    """
    Test de la fonction is_final
    """

    for s in doc5.sentences:
        p = s.constituency
        return is_final(p)


# print(test_is_final())


def extract_all(tree):
    """
    Reconstitue un arbre syntaxique sous forme de liste
    Entrée : arbre syntaxique
    Sortie : liste ordonnée des mots de l'arbre syntaxique
    """

    sentence = []
    next = [tree]
    while len(next) > 0:
        t = next.pop()
        if not is_final(t):
            for c in t.children:
                next.append(c)
        else:
            sentence = [str(t)]+sentence
    return sentence


def test_extract_all():
    """
    Test de la fonction extract_all
    """
    for s in doc5.sentences:
        p = s.constituency
        return extract_all(p)


def rebuild(l):
    """
    Transforme une liste de mots en phrase
    """

    if l == None:
        return None
    sentence = str(l[0])
    contraction = ["n’t", "n't", ",", "'s", "'ll", "'re", ")", "("]
    not_okay = [".", "?", "!", ",", "-", "/", " "]
    for i in range(1, len(l)):
        word = l[i]
        if word in contraction:
            sentence += word
        else:
            sentence += " "+word
    while len(sentence) > 0 and sentence[-1] in not_okay:
        sentence = sentence[0:len(sentence)-1]
    while len(sentence) > 0 and sentence[0] in not_okay:
        sentence = sentence[1:len(sentence)]
    return sentence


def test_rebuild():
    """
    Test de la fonction rebuild
    """
    l = ['If', 'food', 'is', 'foil', 'wrapped', ',', 'remove', 'foil',
         'and', 'place', 'it', 'in', 'a', 'suitable', 'container', '.']
    print(rebuild(l))


# test_rebuild()

#########################################
# Identification cause
#########################################


def sbar_test(tree):
    """
    Teste si l'arbre syntaxique actuelle comporte une proposition subordonnée
    Entrée : arbre syntaxique
    Sortie : Booléen
    """

    words = ["unless", "Unless", "If", "if", "when",
             "When", "After", "after", "because", "Because", "Since", "since", "provided", "Provided", "while", "While"]
    text = extract_all(tree)
    if text[0] in words:
        return True
    return False


def pp_test(tree):
    """
    Teste si l'arbre syntaxique actuelle comporte une proposition prépositionelle 
    Entrée : arbre syntaxique
    Sortie : Booléen
    """

    words = ["After", "after", "before", "Before"]
    text = extract_all(tree)
    for word in text:
        if word in words:
            return True
    return False


def search_sentence(tree):
    """
    Teste si l'arbre syntaxique actuelle comporte une phrase
    Entrée : arbre syntaxique
    Sortie : Booléen
    """

    next = [tree]
    while len(next) > 0:
        t = next.pop()
        if t.label == "S":
            return True, extract_all(t)
    return False, None


def identify_cause(sentence):
    """
    Identifie la cause dans une phrase conditionnelle 
    Entrée : phrase
    Sortie : cause sous forme de liste de mots 
    """

    doc = nlp(sentence)
    for s in doc.sentences:
        tree = s.constituency
    next = [tree]

    # Parcours de l'arbre syntaxique en profondeur
    while len(next) > 0:
        t = next.pop()
        # Construction de cause sous la forme de subordonnée
        if t.label == "SBAR":
            if sbar_test(t):
                is_sentence = search_sentence(t)
                if is_sentence[0] == True:
                    print("aled")
                    return is_sentence[1]
                return extract_all(t)
        # Construction de cause sous la forme de phrase prépositionnelle
        if t.label == "PP":
            if pp_test(t):
                return extract_all(t)
        if not is_final(t):
            for c in t.children:
                next.append(c)
    return None


def test_identify_cause(sentence):
    """
    Teste de la fonction identify_cause
    """

    print(identify_cause(sentence))


def test_sentence(sentence):
    """
    Tests pour comprendre le fonctionnement des arbres syntaxiques
    """

    doc = nlp(sentence)
    for s in doc.sentences:
        c = s.constituency
        print(c.children[0])
        # print("\n"+"dependencies :")
        # print(s.dependencies)


#########################################
# Identification conséquence
#########################################


def delete_sequence(sentence, sequence):
    """
    Suprime une séquence de mots dans une phrase, longueur de la séquence plus petite que la phrase, la séquence est nécessairement dans la phrase
    Entrée : une phrase et une séquence de mots (str)
    Sortie : partie de la phrase sans la séquence identifiée
    """
    if sequence == None:
        return sentence
    n = len(sequence)
    m = len(sentence)
    for i in range(m):
        if i+n <= m and sentence[i:i+n] == sequence:
            return sentence[0:i]+sentence[i+n:m]
    return sentence


def test_delete_sequence():
    """
    Test de la fonction delete_sequence
    """

    sentence = delete_sequence(
        "Do not operate the microwave oven if it has a damaged cord or plug, if it is not working properly, or if it has been damaged or dropped", "if it is not working properly, or if it has been damaged or dropped")
    print(sentence)


# test_delete_sequence()


def identify_consequence(sentence, cause):
    """
    Identifie la conséquence dans une phrase conditionnelle 
    Entrée : phrase
    Sortie : conséquence sous forme de liste de mots 
    """

    # On supprime la cause identifée dans la phrase pour extraire la conséquence
    new_sentence = delete_sequence(sentence, cause)
    doc = nlp(str(new_sentence))
    for s in doc.sentences:
        tree = s.constituency
    next = [tree]
    while len(next) > 0:
        t = next.pop()
        # Construction de texte sous forme de phrase
        if t.label == "S":
            return extract_all(t)
        if not is_final(t):
            for c in t.children:
                next = [c]+next
    return new_sentence.split()


def test_identify_consequence():
    """
    Test de la fonction identify_consequence
    """

    sentence = "Power on the computer or restart it if it's already on"
    print("\n"+"sentence :", sentence)
    cause = rebuild(identify_cause(sentence))
    print("\n" + "cause :", cause)
    consequence = rebuild(identify_consequence(sentence, cause))
    print("\n" + "consequence : ", consequence)


# test_identify_consequence()


#########################################
# Algo final
#########################################


def cause_consequence(sentence):
    """
    Identifie la cause et la conséquence d'une phrase
    Entrée : phrase
    Sortie : affiche la cause et la conséquence d'une phrase sous forme de chaîne de caractères 
    """

    # Affiche la cause sous forme de phrase (str)
    cause = rebuild(identify_cause(sentence))
    print("cause :", cause)

    # Affiche la conséquence sous forme de phrase (str)
    consequence = rebuild(identify_consequence(sentence, cause))
    print("consequence :", consequence)


#cause_consequence("The easiest way to figure this is out is by installing one of a free system information tool, which should tell you if your BIOS is made by AMI, Award, Phoenix, or another company")


def list_cause_consequence(sentence):
    """
    Identifie la cause et la conséquence d'une phrase
    Entrée : phrase
    Sortie : retourne la cause et la conséquence d'une phrase sous forme de listes
    """

    cause_list = identify_cause(sentence)
    cause = rebuild(cause_list)
    consequence_list = identify_consequence(sentence, cause)
    return cause_list, consequence_list
