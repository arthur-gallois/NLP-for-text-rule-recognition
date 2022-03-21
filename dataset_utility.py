import json
import docx


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
    doc = docx.Document("word.docx")
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


print(wordLoader("word.docx"))
