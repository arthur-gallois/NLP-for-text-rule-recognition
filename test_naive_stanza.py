import stanza
from sympy import N
from dataset_utility import *
from naive_stanza import *

text = getJson('data2')
# print(len(text.rules[0].condition))
print(text.rules)
ratio_bon_cause = 0
ratio_nul_cause = 0
ratio_bon_conseq = 0
ratio_nul_conseq = 0
n = len(text.rules)
for k in range(n):
    cause, consequence = cause_consequences(text.rules[k].text)
    bon_mots = 0
    mauvais_mots = 0
    for mot in cause:
        if mot in text.rules[k].condition:
            bon_mots += 1
        else:
            mauvais_mots += 1
    ratio_bon_cause += bon_mots/len(text.rules[k].condition)
    ratio_nul_cause += mauvais_mots/len(cause)
    bon_mots = 0
    mauvais_mots = 0
    for mot in consequence:
        if mot in text.rules[k].consequence:
            bon_mots += 1
        else:
            mauvais_mots += 1
    ratio_bon_conseq += bon_mots/len(text.rules[k].condition)
    ratio_nul_conseq += mauvais_mots/len(cause)
ratio_bon_cause /= n*100
ratio_nul_cause /= n*100
ratio_bon_conseq /= n*100
ratio_nul_conseq /= n*100
print(ratio_bon_cause, ratio_nul_cause, ratio_bon_conseq, ratio_nul_conseq)
