# Pôle IA - NLP - Détection de règles

Le but de ce projet est de détecter des "règles" dans un texte écrit en Anglais (du types if ... then ...)

Le projet est programmé en python

Les algorithmes principaux implémentés permettent : 
1) De détecter si une phrase est une règle conditionnelle
2) Étant donnée une phrase conditionnelle, dégager la partie cause et la partie conséquence

# Prérequis pour l'utilisation

Installation des modules nécessaires : pip install -r requirement.txt

# Les fonctions répondant au but du projet sont présentes dans le fichier main.py
Elles sont pour l'instant programmée pour être utilisée qu'avec un seule phrase et les outputs sont noyés dans un print généré par les librairies utilisées.
Nous n'avons pas eu le temps de trouver une solution pour masquer ces différents prints. D'autre part, modifier les fonctions pour leur permettre de prendre une liste de phrase en entrée est également essentiel. (d'autre part cela devrait être rapide à faire)

Nous avons mis l'essentiel des librairies dans le requirements.txt, cependant il n'est pas exclu qu'il en manque quelques-une (Nous ne savons pas comment s'assurer que le programme tourne uniquement avec celles-ci)

# Datasets

Le projet compte un certain nombre de datasets, cependant la pluspart sont de pietre qualités.
Les datasets de haute qualités sont :
-Dense_dataset
-Musique_classique_rules
-Rules_of_grammar
-Sport_rules
