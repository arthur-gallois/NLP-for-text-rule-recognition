import os
import json
import docx
import sys


class Text:
    rules = []
    text = ""

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '{' + f'"text" : "{self.text}","rules" : {self.rules}' + '}'

    def stringify(self):
        return self.__repr__()


class Rule:
    text = ""
    condition = ""
    consequence = ""
    action = ""

    def __init__(self, text, condition, consequence, action):
        self.text = text
        self.condition = condition
        self.consequence = consequence
        self.action = action

    def __repr__(self):
        return '{' + f'"text" : "{self.text}", "condition" : "{self.condition}", "consequence" : "{self.consequence}","action" : "{self.action}"' + '}'


def parse(input_json):
    try:
        text_dict = json.loads(input_json)
        text = Text(text_dict["text"])
        for rule in text_dict["rules"]:
            text.rules.append(Rule(rule["text"], rule["condition"],
                                   rule["consequence"], rule["action"]))
    except:
        print("Error : Wrong text format")
        return None
    return text


def wordLoader(documentWord):
    # documentWord est le chemin du docx (au format str)
    doc = docx.Document(documentWord)
    k = len(doc.paragraphs)
    word_text = ""
    for para in doc.paragraphs:
        word_text += para.text

    text = Text(word_text)

    rules = []
    for para in doc.paragraphs:
        rule = ""
        condition = ""
        consequence = ""
        action = ""
        for run in para.runs:
            if run.underline:
                rule += run.text
            if run.bold and not run.italic:
                condition += run.text
            if run.italic and not run.bold:
                consequence += run.text
            if run.bold and run.italic:
                action += run.text
            if not run.underline and rule != "":
                rules.append(Rule(rule, condition, consequence, action))
                rule = ""
                condition = ""
                consequence = ""
                action = ""
        if rule != "":
            rules.append(Rule(rule, condition, consequence, action))
            rule = ""
            condition = ""
            consequence = ""
            action = ""
    text.rules = rules
    return text


def saveJson(json_name, json_text):
    path = os.path.dirname(os.path.abspath(__file__))
    with open(f"{path}/dataset/json/{json_name}.json", 'w') as file:
        file.write(json_text)


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Veuillez spécifier le nom du word")
    else:
        path = os.path.dirname(os.path.abspath(__file__))
        json_text = wordLoader(f"{path}/dataset/docx/{sys.argv[1]}.docx")
        saveJson(sys.argv[1], json_text.stringify())
