import docx
L=[]
doc = docx.Document("test_doc.docx")

bolds=[]
italics=[]
for para in doc.paragraphs:
    for run in para.runs:
        if run.italic :
            italics.append(run.text)
        if run.bold :
            bolds.append(run.text)
            
print(bolds, italics)
