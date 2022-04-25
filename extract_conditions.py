import re 
import nltk

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

def is_condition(sentence):
    '''
    Entree : une phrase (string).
    Sortie : un booléen qui donne si la phrase est une condition (bool).
    '''
    if len(sentence) == 0 or sentence[-1] == '?':
        return False
    liste_mots = wordify(sentence.upper())
    return ('IF' in liste_mots) or ('UNLESS' in liste_mots) or ('AS' in liste_mots and ',' in liste_mots) and ('OTHERWISE' in liste_mots) #or ('WHEN' in liste_mots and ',' in liste_mots)
    


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


print(naive_condition_extract('When the cookies are in the oven, start it.')) 

