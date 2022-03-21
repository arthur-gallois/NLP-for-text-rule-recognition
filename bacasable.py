import docx

doc = docx.Document("test_doc.docx")
result = [p.text for p in doc.paragraphs]
#print(result)