import os
import json
import sys


class Text:
    rules = []
    text = ""

    min_sentence_len = 10

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        text = repr(self.text).replace('\\', '/')
        text = text.replace('"', '\\"')
        text = text.replace("‘", '\\"')
        text = text.replace("’", '\\"')
        return '{' + f'"text" : "{text}","rules" : {self.rules}' + '}'

    def stringify(self):
        return self.__repr__()

    def get_sentences(self):
        sentences = [sentence.strip(" ") for sentence in self.text.split(
            '.') if len(sentence.strip(" ")) > self.min_sentence_len]
        conditions = [rule.text for rule in self.rules]
        non_conditional_sentences = []
        conditional_sentences = []
        for sentence in sentences:
            is_conditional = False
            n = 0
            for condition in conditions:
                if condition in sentence:
                    is_conditional = True
                    n += 1
            if is_conditional:
                conditional_sentences.append(sentence)
            else:
                non_conditional_sentences.append(sentence)
            return(conditional_sentences, non_conditional_sentences)


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
        text = repr(self.text).replace('\\', '/')
        text = text.replace('"', '\\"')
        text = text.replace("‘", '\\"')
        text = text.replace("’", '\\"')

        condition = repr(self.condition).replace('\\', '/')
        condition = condition.replace('"', '\\"')
        condition = condition.replace("‘", '\\"')
        condition = condition.replace("’", '\\"')

        consequence = repr(self.consequence).replace('\\', '/')
        consequence = consequence.replace('"', '\\"')
        consequence = consequence.replace("‘", '\\"')
        consequence = consequence.replace("’", '\\"')

        action = repr(self.action).replace('\\', '/')
        action = action.replace('"', '\\"')
        action = action.replace("‘", '\\"')
        action = action.replace("’", '\\"')

        return '{' + f'"text" : "{text}", "condition" : "{condition}", "consequence" : "{consequence}","action" : "{action}"' + '}'


def parseJson(input_json):
    try:
        text_dict = json.loads(input_json)
        text = Text(text_dict["text"])
        for rule in text_dict["rules"]:
            text.rules.append(Rule(rule["text"], rule["condition"],
                                   rule["consequence"], rule["action"]))
    except:
        print("\033[91m Error : Wrong text format \033[0m")
        return None
    return text


def getJson(json_name):
    file_path = os.path.dirname(os.path.abspath(__file__))
    json_path = f"{file_path}\\dataset\\json\\{json_name}.json"
    f = open(json_path, "r", encoding='utf-8')
    lines = f.readlines()
    return parseJson(lines[0])


def wordLoader(documentWord):
    import docx

    # documentWord est le chemin du docx (au format str)
    doc = docx.Document(documentWord)
    k = len(doc.paragraphs)
    word_text = ""
    for para in doc.paragraphs:
        word_text += para.text.replace('\n', '').replace("\xa0", '')
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
                rules.append(
                    Rule(rule.strip(".").replace('\n', '').replace("\xa0", ''), condition, consequence, action))
                rule = ""
                condition = ""
                consequence = ""
                action = ""
        if rule != "" and condition != "":
            rules.append(Rule(rule.strip(".").replace('\n', '').replace(
                "\xa0", ''), condition, consequence, action))
            rule = ""
            condition = ""
            consequence = ""
            action = ""
    text.rules = rules
    return text


def saveJson(json_name, json_text):
    path = os.path.dirname(os.path.abspath(__file__))
    with open(f"{path}/dataset/json/{json_name}.json", 'w', encoding='utf8') as file:
        file.write(json_text)


if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("\033[91m Veuillez spécifier le nom du word \033[0m")
    elif(sys.argv[1] == "all"):
        path = os.path.dirname(os.path.abspath(__file__))
        for _, _, filenames in os.walk(f'{path}/dataset/docx/'):
            for filename in filenames:
                name = filename.split(".")[0]
                print(f"Generating {name}.json")
                json_text = wordLoader(f"{path}/dataset/docx/{name}.docx")
                saveJson(name, json_text.stringify())
                test = parseJson(json_text.stringify())
    else:
        path = os.path.dirname(os.path.abspath(__file__))
        json_text = wordLoader(f"{path}/dataset/docx/{sys.argv[1]}.docx")
        saveJson(sys.argv[1], json_text.stringify())
        test = parseJson(json_text.stringify())
