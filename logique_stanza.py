import stanza
# stanza.download('en')
nlp = stanza.Pipeline(
    'en', processors='tokenize,mwt,pos,lemma,depparse,ner,sentiment,constituency')
liste_mots = ['if', 'unless', 'otherwise', 'case','when']

def take_id(mot):
    return mot[1]

def take_text(mot):
    return mot[0]

def exception(phrase, mot):
    if mot['id'] != 1:
        if mot['lemma'] == 'if' and phrase[mot['id']-2]['lemma'] == 'even': #"even if" ne correspond pas a une règle
            print('EXCEPTION')
            return True
        if mot['lemma'] == 'case':  #"in case of"  représente une règle
            if not(phrase[mot['id']-2]['lemma'] == 'in' and phrase[mot['id']]['lemma'] == 'of'):
                return True
    return False

def cause_consequences(text):
    doc = nlp(text)
    for p in range(len(doc.sentences)): # on parcours les phrases du texte
        phrase = doc.sentences[p].to_dict()
        if phrase[-1]['text'] == '?':  # on verifie que le phrase n'est pas une question
            print('C\'est un question')
            pass
        for mot in phrase:
            causes = []
            causes_id = []
            consequences = []
            consequences_id = []
            if mot['lemma'] in liste_mots:  # si on repere un des mots de la liste
                h1 = mot['head']
                if exception(phrase, mot):
                    pass
                else:            
                    action = phrase[h1-1]   # action est le mot principal de la phrase
                    h2 = action['head']
                    if h2 != 0:             # si on a une conséquence
                        consequence = phrase[h2-1]['text']  #la variable consequence est un mot important de la conséquence de la phrase
                        consequences.append((consequence, h2))
                        consequences_id.append(h2)
                    causes.append((action['text'], h1))
                    causes_id.append(h1)
            if len(causes) != 0:    #si on a repéré une cause
                boole=True
                while boole:    #tant que l'on rajoute des élements on continue
                    boole=False
                    for mot in phrase:
                        h = mot['head']
                        id = mot['id']
                        if h in (causes_id) and (id not in causes_id) and (mot['upos'] != "PUNCT"):# si le mot appartient à la cause
                            causes.append((mot['text'], mot['id']))
                            causes_id.append(mot['id'])
                            boole=True
                        if (h in consequences_id) and (id not in consequences_id) and (h2 != 0) and (mot['id'] != h1) and (mot['upos'] != "PUNCT"):# si le mot appartient à la conséquence
                            consequences.append((mot['text'], mot['id']))
                            consequences_id.append(mot['id'])
                            bool=True
                causes.sort(key=take_id)    #on trie la cause pour retrouver l'ordre présent dans la phrase
                consequences.sort(key=take_id)  #de même
                causes = list(map(take_text, causes)) #on retire les indices des mots(cela ne nous interesse pas)
                consequences = list(map(take_text, consequences))
                return causes, consequences
