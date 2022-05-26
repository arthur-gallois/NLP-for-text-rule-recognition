from lib2to3.pgen2.literals import test
import re 
import stanza
import nltk
import pattern

def test_stanza(sentence,indice):
    nlp = stanza.Pipeline("en")
    doc = nlp(sentence)
    phrase = doc.sentences[0].to_dict()
    return phrase[indice]


def is_past(sentence):
    nlp = stanza.Pipeline("en")
    doc = nlp(sentence)
    phrase = doc.sentences[0].to_dict()
    for mot in phrase:
        if 'feats' in mot:
            if 'Tense=Past' in mot['feats']:
                return True
    return False

def sentencify(text):
    '''
    Entree : Un texte complet (string).
    Sortie : Une liste contenant la liste des phrases du texte ainsi
    que le numéro de la phrase,
    l'indice de début et de fin (list of (string,int,int,int)).
    '''
    liste_phrases = []
    debut_phrase = 0
    num_phrase = 0
    for indice_texte in range(len(text)):
        if text[indice_texte] in ['.','!','?']:
            liste_phrases.append((text[debut_phrase:indice_texte+1],num_phrase,debut_phrase,indice_texte))
            debut_phrase = indice_texte + 2
            num_phrase += 1
    return liste_phrases

#print(sentencify("Salut, ce projet traite de l'extraction de règles? Ce texte est un lorem ipsum. If Yes then No! iF qsldfkqsdl thEn zepfidkj. Okambonac zuitel, oksof: yaya. If not true. If Then you !"))

def wordify(sentence):
    '''
    Entree : Une phrase (string).
    Sortie : liste des mots constitutifs de la phrase (list of string).
    '''
    return nltk.word_tokenize(sentence)


#print(wordify('tests, ds: pomme de terre; oui'))
#print(sentencify("Salut, ce projet traite de l'extraction de règles? Ce texte est un lorem ipsum. If Yes then No! iF qsldfkqsdl thEn zepfidkj. Okambonac zuitel, oksof: yaya. If not true. If Then you !"))

def has_keyword(sentence):
    '''
    Entree : une phrase (string).
    Sortie : un booléen qui donne si la phrase est une condition (bool).
    '''
    if len(sentence) == 0 or sentence[-1] == '?':
        return False
    liste_mots = wordify(sentence.upper())
    for i in range(len(liste_mots)):
        if liste_mots[i] == 'IF' and not (i!=0 and liste_mots[i-1] in ['EVEN', 'AS']) and not (i!=len(liste_mots)-1 and liste_mots[i+1] == 'ONLY'):
            return True
        if liste_mots[i] == 'UNLESS':
            return True
        '''if liste_mots[i] == 'UNTIL':
            return True'''
        if liste_mots[i] == 'PROVIDED' and liste_mots[i+1] == 'THAT':
            return True
        if liste_mots[i] == 'ASSUMING' and liste_mots[i+1] == 'THAT':
            return True
        if liste_mots[i] == 'OTHERWISE':
            return True
        '''if liste_mots[i] == 'AS':
            return True'''
        #Pour le WHEN, il faut vérifier si le verbe qui suit n'est pas au passé
        if liste_mots[i] == 'WHEN' and not is_past(sentence):
            return True
    return False
    return ('IF' in liste_mots) or ('UNLESS' in liste_mots) or ('AS' in liste_mots and ',' in liste_mots) and ('OTHERWISE' in liste_mots) #or ('WHEN' in liste_mots and ',' in liste_mots)

def is_condition(sentence):
    return has_keyword(sentence)

def naive_condition_extract(text):
    '''
    Entree : un texte (string).
    Sortie : une liste de couple (phrase,indice) où phrase est une phrase
    contenant une condition et indice est le numéro (commençant à 0) de la phrase
    en question (list of (string,int)).
    '''
    indices = []
    i = 0
    liste_phrases = sentencify(text)
    for sentence in [sent for sent,_,_,_ in liste_phrases]:
        su = sentence.upper()
        if is_condition(su):
            indices.append(i)
        i += 1
    return [(liste_phrases[i]) for i in indices]

#print(naive_condition_extract("Salut, ce projet traite de l'extraction de règles? Ce texte est un lorem ipsum. If Yes then No! iF qsldfkqsdl thEn zepfidkj. Okambonac zuitel, oksof: yaya. If not true. If Then you !"))
#print(has_keyword('''It is Sunny, but if it rains I will take my umbrella''')) 
print(test_stanza('Treat People and Property With Respect.',0))
#print(is_condition('When I boil water, It evaporates'))