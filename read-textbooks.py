from PyPDF2 import PdfReader
import preprocess as pp
import os
import re

path = "/data/madesai/history-llm-data/mi-open-textbooks/"
    
files = ["HSUSFull.pdf","HSWorld.pdf"]
for f in files:
    reader = PdfReader(path+f)
    out_file = f[:-4]+".csv"
    file_questions = set()
    for page in reader.pages:
        raw_text = page.extract_text()
        clean_text = pp.remove_whitespaces(raw_text)
        questions = pp.find_questions(clean_text)
        print(questions)
        
        if questions: 
            for q in questions:
                file_questions.add(questions)
    for q in file_questions:
        out_file.write(q+"\n")
    out_file.close()






