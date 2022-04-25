import stanza
# stanza.download('en')

liste_mots = ['if', 'unless', 'otherwise', 'when']

def take_id(mot):
    return mot[1]

def take_text(mot):
    return mot[0]

def fils(phrase):
    n = len(phrase)
    aux = [[] for k in range(n)]
    for mot in phrase:
        if mot['head'] != 0:
            aux[mot['head']-1].append(mot['id'])


def cause_consequences(text):
    nlp = stanza.Pipeline(
        'en', processors='tokenize,mwt,pos,lemma,depparse,ner,sentiment,constituency')
    doc = nlp(text)
    for p in range(len(doc.sentences)):
        phrase = doc.sentences[p].to_dict()
        # phrase=fils(phrase)
        causes = []
        causes_id = []
        consequences = []
        consequences_id = []
        for mot in phrase:
            if mot['lemma'] in liste_mots:
                h1 = mot['head']
                action = phrase[h1-1]
                h2 = action['head']
                if h2 != 0:
                    consequence = phrase[h2-1]['text']
                    consequences.append((consequence, h2))
                    consequences_id.append(h2)
                causes.append((action['text'], h1))
                causes_id.append(h1)
            break
        for k in range(2):
            for mot in phrase:
                h = mot['head']
                id = mot['id']
                if h in (causes_id) and (id not in causes_id):
                    causes.append((mot['text'], mot['id']))
                    causes_id.append(mot['id'])
                if (h in consequences_id) and (id not in consequences_id) and (h2 != 0) and (mot['id'] != h1) and (mot['upos'] != "PUNCT"):
                    consequences.append((mot['text'], mot['id']))
                    consequences_id.append(mot['id'])
        causes.sort(key=take_id)
        consequences.sort(key=take_id)
        causes = list(map(take_text, causes))
        consequences = list(map(take_text, consequences))
        print(causes)
        print(consequences)


cause_consequences(
    'If you don’t mind draining the pool, caulk or epoxy can also be used to repair cracks')
