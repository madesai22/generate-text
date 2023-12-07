from PyPDF2 import PdfReader
import os
import re
from unidecode import unidecode
import string

def remove_whitespaces(text,paragraph=False):
    if paragraph:
       return re.sub(' +|\t+', ' ', text)
    else:
       end_chars = re.sub('\n ',' ',text)
       end_chars = re.sub('\n',' ',end_chars) 
       return re.sub(' +|\t+', ' ', end_chars)
    
def strip_punctuation(text):
    text =  unidecode(text)
    return text.translate(str.maketrans('', '', string.punctuation))

def pre_process_sentence(text, stopwords=None):
    pattern = pattern = "\.(\n|\s)+"
    text = re.split(pattern, text)
    new_text = []
    for i in range(len(text)):
       sentence = text[i]
       if sentence is not None:
          #sentence = strip_punctuation(sentence)
          sentence = remove_whitespaces(sentence)
          #sentence = strip_punctuation(sentence).lower().strip()
          new_text.append(sentence)
    return new_text
    
def find_inquiry_questions(text):
    # find question area:
    test = re.findall("QUESTIONS TO GUIDE INQUIRY\s*.*[0-9]\.\s.*\?",text)
    if test:
        print("test!!:{}".format(test))
        print("text:{}".format(text))
        question_area = re.findall("QUESTIONS TO GUIDE INQUIRY\s*.*[0-9]\.\s.*\?",text)[0]
        question_area = re.sub("QUESTIONS TO GUIDE INQUIRY\s*","",question_area) # remove header

        # split questions:
        question_list = re.split("\s?[0-9]+\.\s", question_area)
        question_list = list(filter(None, question_list)) # remove empty items
        question_mark = []
        for i in question_list:
            if i.endswith("?"): question_mark.append(i)
        return question_mark
    else:
        return None
    
def find_questions(text):
    pattern = "(?<=[?|\.|!|:]).*\?"
    questions = re.findall(pattern,clean_text)
    return questions
    
path = "/data/madesai/history-llm-data/mi-open-textbooks/"
    
files = ["HSUSFull.pdf","HSWorld.pdf"]
for f in files:
    reader = PdfReader(path+f)
    out_file = open(f[:-4]+".txt","w")
    file_questions = set()
    for page in reader.pages:
        raw_text = page.extract_text()
        clean_text = remove_whitespaces(raw_text)
        #questions = find_questions(clean_text)
        t = pre_process_sentence(clean_text)
        if t:
            for q in t:
                print(q)
        

        
        # if questions: 
        #     for q in questions:
        #         print(q.strip())
    #             file_questions.add(q)
    # for q in file_questions:
    #     out_file.write(q+"\n")
    # out_file.close()






