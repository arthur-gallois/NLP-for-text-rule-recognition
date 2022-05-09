import stanza
# stanza.download('en')
nlp = stanza.Pipeline(
        'en', processors='tokenize,mwt,pos,lemma,depparse,ner,sentiment,constituency')
liste_mots = ['if', 'unless', 'otherwise', 'case']


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


def exception(phrase, mot):
    if mot['id'] != 1:
        if mot['lemma'] == 'if' and phrase[mot['id']-2]['lemma'] == 'even':
            print('EXCEPTION')
            return True
        if mot['lemma'] == 'case':
            if not(phrase[mot['id']-2]['lemma'] == 'in' and phrase[mot['id']]['lemma'] == 'of'):
                return True
    return False


def cause_consequences(text):
    compt = 0
    doc = nlp(text)
    for p in range(len(doc.sentences)):
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
                    # action est le mot principal de la phrase
                    action = phrase[h1-1]
                    h2 = action['head']
                    if h2 != 0:
                        consequence = phrase[h2-1]['text']
                        consequences.append((consequence, h2))
                        consequences_id.append(h2)
                    causes.append((action['text'], h1))
                    causes_id.append(h1)
            if len(causes) != 0:
                compt += 1
                for k in range(2):
                    for mot in phrase:
                        h = mot['head']
                        id = mot['id']
                        # si le mot appartient à la cause
                        if h in (causes_id) and (id not in causes_id) and (mot['upos'] != "PUNCT"):
                            causes.append((mot['text'], mot['id']))
                            causes_id.append(mot['id'])
                        # si le mot appartient à la conséquence
                        if (h in consequences_id) and (id not in consequences_id) and (h2 != 0) and (mot['id'] != h1) and (mot['upos'] != "PUNCT"):
                            consequences.append((mot['text'], mot['id']))
                            consequences_id.append(mot['id'])
                causes.sort(key=take_id)
                consequences.sort(key=take_id)
                causes = list(map(take_text, causes))
                consequences = list(map(take_text, consequences))
                # print('Cause:')
                # print(causes)
                # print('Conséquence:')
                # print(consequences)
                # print(compt)
                return causes, consequences


p1 = 'If your players will be wearing cleats, make sure they are soccer cleats.'
p2 = 'If food is foil wrapped, remove foil and place it in a suitable container.'
p3 = 'Unless the cookies aren\'t in the oven, start it'
p4 = 'You can determine if it\'s clogged by looking at your pool water'
p5 = 'Even if you are careful, pool chemicals, the sun, and time will eventually ruin the liner'
p6 = 'When opening your pool, take note that if there are no algae to kill, the algaecide will create some foam.'
p7 = 'If you are receiving an error message or an unexpected result, it is easy to include a log file that demonstrates the problem'
p8 = 'If you had 100 variables like that, the savings would be 300 bytes per observation, and if you had 3000000 observations, the total savings would be nearly 900 megabytes.'
text2 = '''Power on or restart the computer and listen carefully to the beeps.
Write down the number of beeps and whether they are long, short, or of equal length. Also, make a note if the beeps repeat.
Install a tool to determine the BIOS maker and then consult the appropriate online troubleshooting guide.
This article explains how to figure out why your PC is beeping by noting the beep pattern, determining your computer's BIOS maker, and consulting the matching online guide.

How to Troubleshoot Beep Codes
If you're hearing beep codes after you turn your computer on and then it doesn't start—it means the motherboard encountered some kind of problem before it was able to send any error information to the monitor.

Follow these steps below to determine what computer problem the beep code is representing. Once you know what's wrong, you can work to fix the problem.

Power on the computer or restart it if it's already on.

Listen very carefully to the beep codes that sound when the computer begins to boot.

Restart your computer if you need to hear the beeping again. You're probably not going to make whatever problem you have worse by restarting a few times.

Write down, in whatever way makes sense to you, how the beeps sound.

Pay close attention to the number of beeps, if the beeps are long or short (or all the same length), and if the beeping repeats or not. There is a big difference between a "beep-beep-beep" and a "beep-beep."

Yes, this might all seem a little crazy, but this is important information that will help determine what issue the beep codes are representing. If you get this wrong, you'll be trying to solve a problem your computer doesn't have and ignoring the real one.

Next, you'll need to figure out what company manufactured the BIOS chip that's on your computer motherboard. Unfortunately, the computer industry never agreed on a uniform way to communicate with beeps, so it's important to get this right.

The easiest way to figure this is out is by installing one of a free system information tool, which should tell you if your BIOS is made by AMI, Award, Phoenix, or another company. If that doesn't work, you could open your computer and take a peek at the actual BIOS chip on your computer motherboard, which should have the company name printed on or next to it.

Your computer maker isn't the same as the BIOS maker and your motherboard maker isn't necessarily the same as the BIOS maker, so don't assume you already know the right answer to this question.

Now that you know the BIOS manufacturer, choose the troubleshooting guide below based on that information:

AMI Beep Code Troubleshooting (AMIBIOS)
Award Beep Code Troubleshooting (AwardBIOS)
Phoenix Beep Code Troubleshooting (PhoenixBIOS)
Using the beep code information specific to those BIOS makers in those articles, you'll be able to figure out exactly what's wrong that's causing the beeping, be it a RAM issue, a video card problem, or some other hardware problem.

More Help With Beep Codes
Some computers, even though they may have BIOS firmware made by a particular company, like AMI or Award, further customize their beep-to-problem language, making this process a little frustrating. If you think this might be the case, or just worried it could be, almost every computer maker publishes their beep code list in their user guides, which you can probably find online.

If you need help digging up your computer's manual, go online to find tech support information.
'''

cause_consequences(text2)
