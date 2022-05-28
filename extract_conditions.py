#from lib2to3.pgen2.literals import test
import re
#from pyparsing import Or 
import stanza
import nltk
import pattern
import keyword_list as kl
nlp = stanza.Pipeline("en")

def test_stanza(sentence,indice):
    '''
    input:
        sentence: str
        indice: int
    
    output:
        dict

    Cette fonction prend en argument une phrase et un indice i et
    renvoie les informations stanza du i-eme mot de la phrase sous la 
    forme d'un dictionnaire
    '''
    doc = nlp(sentence)
    phrase = doc.sentences[0].to_dict()
    return phrase[indice]

def Conjugaison(sentence,indice,time,method='Any'):
    '''
    input:
        sentence: str
        indice: int
        time: str
        method: str
    
    output:
        bool

    Cette fonction prend en argument une phrase contenant un mot clé se trouvant à 
    la position indice ainsi qu'un temps (exemple 'Past') et un méthode qui peut 
    être un entier ou 'Any' la fonction renvoie True si il existe un verbe
    conjugué au temps time dans la phrase.
    
    Exemple:    sentence: 'If I were here'
                indice: 0
                time: 'Past'
                method: 2
    Cet appel renvoie True car à la position indice + method = 2 il y a bien un verbe
    'were' conjugué au passé.

    Remarque: la méthode 'Any' permet de rechercher n'importe où dans la phrase
    '''
    if time == 'Past':
        time_condition = 'Tense=Past'
    elif time == 'ing':
        time_condition = 'Tense=Pres|VerbForm=Part','VerbForm=Ger'
    else:
        raise Exception('''Le temps rentré n'est pas pris en charge''')
    doc = nlp(sentence)
    phrase = doc.sentences[0].to_dict()
    if method=='Any':
        for mot in phrase:
            if 'feats' in mot:
                for tc in time_condition:
                    if tc in mot['feats']:
                        return True
    elif type(method) == int:
        if indice+method < 0 or indice+method >= len(phrase):
            return False
        mot = phrase[indice+method]
        if 'feats' in mot:
            if time_condition in mot['feats']:
                return True
    return False

def sentencify(text):
    '''
    Input : Un texte complet (string).
    Output : Une liste contenant la liste des phrases du texte ainsi
    que le numéro de la phrase,
    l'indice de début et de fin (list of (string,int,int,int)).
    '''
    liste_phrases = []
    debut_phrase = 0
    num_phrase = 0
    indice_texte = 0
    while indice_texte < len(text):
        if text[indice_texte] in ['.','!','?']:
            if indice_texte+2<len(text) and text[indice_texte+2] == '.':
                indice_texte += 2
            liste_phrases.append((text[debut_phrase:indice_texte+1],num_phrase,debut_phrase,indice_texte))
            debut_phrase = indice_texte + 2
            num_phrase += 1
        indice_texte += 1
    return liste_phrases

print(sentencify('Hello.. My name is Valentin. If I were rich, I would be happy !'))

def wordify(sentence):
    '''
    Entree : Une phrase (string).
    Sortie : liste des mots constitutifs de la phrase (list of string).
    '''
    return nltk.word_tokenize(sentence)


def is_exception(sentence,list_excep,indice):
    for excep in list_excep:
        if excep[0] == 'Word':
            liste_mots = wordify(sentence.upper())
            if type(excep[1]) == int:
                if ((indice + excep[1] < 0) or (indice + excep[1] >= len(liste_mots)) or (liste_mots[indice+excep[1]] != excep[2])):
                    return False
            else:
                #Rentrer ici les différents mots clés d'emplacement
                if  excep[1] == 'Any':
                    for k in range(len(liste_mots)):
                        if not liste_mots[k] == excep[2]:
                            return False
        elif excep[0] == 'Verb':
            if not Conjugaison(sentence,indice,excep[2],method=excep[1]):
                return False
    return True

def is_condition(sentence):
    '''
    Entree : une phrase (string).
    Sortie : un booléen qui donne si la phrase est une condition (bool).
    '''
    if len(sentence) == 0 or sentence[-1] == '?':
        return False
    liste_mots = wordify(sentence.upper())
    for i in range(len(liste_mots)):
        if liste_mots[i] in kl.keyword_list:
            is_cond = True
            if 'Composite' in kl.keyword_list[liste_mots[i]]:
                for list_comp in kl.keyword_list[liste_mots[i]]['Composite']:
                    if is_exception(sentence,list_comp,i):
                        is_cond = True
                        break
            if is_cond and 'Exception' in kl.keyword_list[liste_mots[i]]:
                for list_excep in kl.keyword_list[liste_mots[i]]['Exception']:
                    if is_exception(sentence,list_excep,i):
                        is_cond = False
                        break
            if is_cond:
                return True
    return False

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
#print(is_ing('''I walked there''',0))
#print(is_condition('When I boil water, It evaporates'))

'''Idées à faire, chercher des conditions sur les verbes dans les phrases pour être des règles'''