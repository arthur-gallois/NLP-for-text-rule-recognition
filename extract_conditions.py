import re 

def sentencify(text):
    '''
    Entree : Un texte complet (string).
    Sortie : Une liste contenant la liste des phrases du texte (list of string).
    '''
    text = text
    liste_phrases = re.split(r"\. |\? |\! |\.|\!|\?",text)
    return liste_phrases
     
def wordify(sentence):
    '''
    Entree : Une phrase (string).
    Sortie : liste des mots constitutifs de la phrase (list of string).
    '''
    liste_mots = re.split(r"\ |\, |\; |\: ",sentence)
    return liste_mots


print(wordify('tests, ds: pomme de terre; oui'))
print(sentencify("Salut, ce projet traite de l'extraction de règles? Ce texte est un lorem ipsum. If Yes then No! iF qsldfkqsdl thEn zepfidkj. Okambonac zuitel, oksof: yaya. If not true. If Then you !"))

def is_condition(sentence):
    liste_mots = wordify(sentence.upper())
    return ('IF' in liste_mots and 'THEN' in liste_mots)
    
        


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
    for sentence in liste_phrases:
        if is_condition(sentence.upper()):
            indices.append(i)
        i += 1
    return [(liste_phrases[i],i) for i in indices]

print(naive_condition_extract("Salut, ce projet traite de l'extraction de règles? Ce texte est un lorem ipsum. If Yes then No! iF qsldfkqsdl thEn zepfidkj. Okambonac zuitel, oksof: yaya. If not true. If Then you !"))
        

