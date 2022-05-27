import stanza
from sympy import N
from dataset_utility import *
from naive_stanza import *

text = getJson('data2')
ratio = [0, 0, 0, 0]    #ratio_bon_cause/ratio_mauvais_cause/ratio_bon_consequence/ratio_mauvais_consequence
n = len(text.rules)
for k in range(n):      #on boucle sur les phrases
    cause, consequence = cause_consequences(text.rules[k].text)
    bon_mots = 0
    mauvais_mots = 0
    for mot in cause:   #on compare les causes
        if mot in text.rules[k].condition:
            bon_mots += 1
        else:
            mauvais_mots += 1
    ratio[0] += bon_mots/len(text.rules[k].condition)
    ratio[1] += mauvais_mots/len(cause)
    bon_mots = 0
    mauvais_mots = 0
    for mot in consequence: #on compare les conséquences
        if mot in text.rules[k].consequence:
            bon_mots += 1
        else:
            mauvais_mots += 1
    ratio[2] += bon_mots/len(text.rules[k].condition)
    ratio[3] += mauvais_mots/len(cause)
ratio[0] *= 100/n   #on exprime les ratios en %
ratio[1] *= 100/n
ratio[2] *= 100/n
ratio[3] *= 100/n
print(ratio)
