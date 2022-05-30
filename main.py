import keyword_extract_rules as ker
import naive_stanza as ns
import stanza_parseTree as sp
import stanza
nlp = stanza.Pipeline("en")

def is_rule(method,sentence):
    '''
    method: 'keyword' or 'bert'
    sentence: a string
    '''
    if method == 'keyword':
        return ker.is_rule(sentence)
    elif method == 'bert':
        ###ARTHUR
        pass
    else:
        raise Exception('Incorrect method')

def extract_rules(method,text):
    L = []
    phrases = [s for s,_,_,_ in ker.sentencify(text)]
    for phrase in phrases:
        if is_rule(method,phrase):
            L.append(phrase)
    return L

def cause_consequence(method,sentence):
    '''
    method: 'logic' or 'syntaxic'
    sentence: a string
    '''

