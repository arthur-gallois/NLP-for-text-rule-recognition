import stanza
# from dataset_utility import *

# stanza.download('en')
nlp = stanza.Pipeline('en')

# Les phrases tests

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

# Quand les causes sont identifiées dans la phrase

test1 = nlp(
    "Use extreme care when inserting a spoon or other utensil into the container.")
test2 = nlp("Carefully attend the microwave oven if paper, plastic, or other combustible materials are placed inside the oven to facilitate cooking. ")

test3 = nlp(
    "Always use oven mitts or pot holders when removing dishes from the microwave oven. ")


def is_final(tree):
    return str(tree)[0] != '('


def test_is_final():
    for s in doc5.sentences:
        p = s.constituency
        return is_final(p)


# print(test_is_final())


def extract_all(tree):
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
    for s in doc5.sentences:
        p = s.constituency
        return extract_all(p)


def rebuild(l):
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
    l = ['If', 'food', 'is', 'foil', 'wrapped', ',', 'remove', 'foil',
         'and', 'place', 'it', 'in', 'a', 'suitable', 'container', '.']
    print(rebuild(l))


# test_rebuild()

##
# IDENTIFICATION CAUSE
##


def sbar_test(tree):
    words = ["unless", "Unless", "If", "if", "when",
             "When", "After", "after", "because", "Because", "Since", "since", "provided", "Provided", "that", "That", "while", "While", "as"]
    text = extract_all(tree)
    if text[0] in words:
        return True
    return False


def pp_test(tree):
    words = ["After", "after", "before", "Before"]
    text = extract_all(tree)
    for word in text:
        if word in words:
            return True
    return False


def search_sentence(tree):
    next = [tree]
    while len(next) > 0:
        t = next.pop()
        if t.label == "S":
            return True, extract_all(t)
    return False, None


def identify_cause(sentence):
    doc = nlp(sentence)
    for s in doc.sentences:
        tree = s.constituency
    next = [tree]
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
    print(identify_cause(sentence))


# test_identify_cause(s1)


def test_sentence(sentence):
    doc = nlp(sentence)
    for s in doc.sentences:
        c = s.constituency
        print(c.children[0])
        # print("\n"+"dependencies :")
        # print(s.dependencies)


#print(test_sentence("The easiest way to figure this is out is by installing one of a free system information tool, which should tell you if your BIOS is made by AMI, Award, Phoenix, or another company"))


# Forme exploitable de conséquences

#
# IDENTIFICATION CONSEQUENCES
#

def delete_sequence(sentence, sequence):
    """
    Suprime une séquence de mots dans une phrase, longueur de la séquence plus petite que la phrase, la séquence est nécessairement dans la phrase
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
    sentence = delete_sequence(
        "Do not operate the microwave oven if it has a damaged cord or plug, if it is not working properly, or if it has been damaged or dropped", "if it is not working properly, or if it has been damaged or dropped")
    print(sentence)


# test_delete_sequence()


def identify_consequence(sentence, cause):
    new_sentence = delete_sequence(sentence, cause)
    doc = nlp(str(new_sentence))
    for s in doc.sentences:
        tree = s.constituency
    next = [tree]
    while len(next) > 0:
        t = next.pop()
        # Construction de texte en SBAR
        if t.label == "VP":
            return extract_all(t)
        if not is_final(t):
            for c in t.children:
                next = [c]+next
    return new_sentence


def test_identify_consequence():
    sentence = s9
    print("\n"+"sentence :", sentence)
    cause = rebuild(identify_cause(sentence))
    print("\n" + "cause :", cause)
    consequence = rebuild(identify_consequence(sentence, cause))
    print("\n" + "consequence : ", consequence)


# test_identify_consequence()


def dic_consequences(tree):
    """
    Si la conséquence est connue, identifie des mots importants dedans
    Entrée: le sous arbre syntaxique de la conséquence
    Sortie: dictionnaire de mots importants dans la conséquence.
    """
    dic = {}
    next = [tree]
    while len(next) > 0:
        t = next.pop()
        if t.label == "VB":
            dic["VB"] = rebuild(extract_all(t))
        if t.label == "NN":
            dic["NN"] = rebuild(extract_all(t))
        if not is_final(t):
            for c in t.children:
                next.append(c)
    return dic


def test_dic_consequence(doc):
    for s in doc.sentences:
        p = s.constituency
        print(dic_consequences(p))

#
# ALGO FINAL
#


def cause_consequence(sentence):
    cause = rebuild(identify_cause(sentence))
    print("cause :", cause)
    consequence = rebuild(identify_consequence(sentence, cause))
    print("consequence :", consequence)


#cause_consequence("The easiest way to figure this is out is by installing one of a free system information tool, which should tell you if your BIOS is made by AMI, Award, Phoenix, or another company")


def list_cause_consequence(sentence):
    cause_list = identify_cause(sentence)
    cause = rebuild(cause_list)
    consequence_list = identify_consequence(sentence, cause)
    return cause_list, consequence_list


def compare_lists(l1, l2):
    n1 = len(l1)
    n2 = len(l2)
    set1 = set(l1)
    set2 = set(l2)
    z = set1.intersection(set2)
    return (len(z)*2)/(n1+n2)


#print(list_cause_consequence("Also, make a note if the beeps repeat"))

def test_compare_lists(sentence):
    cause = "if the beeps repeat"
    cause = cause.split()
    cause_algo = identify_cause(sentence)
    print(cause)
    print(cause_algo)
    print(compare_lists(cause, cause_algo))


#test_compare_lists("Also, make a note if the beeps repeat")
