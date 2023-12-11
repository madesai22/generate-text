from PyPDF2 import PdfReader
import os
import re
from unidecode import unidecode
import string

def remove_whitespaces(text,paragraph=False):
    if paragraph:
       end_chars = re.sub('\s+',' ',text)
       end_chars = re.sub("http(s?)://\S*\s"," ",end_chars)
       return re.sub(' +|\t+', ' ', end_chars)
    else:
       end_chars = re.sub('\n ',' ',text)
       end_chars = re.sub('\n',' ',end_chars) 
       end_chars = re.sub('\s+',' ',end_chars)
       end_chars = re.sub("http(s?)://\S*\s"," ",end_chars)
       return re.sub(' +|\t+', ' ', end_chars)

def remove_urls(text):
    return re.sub("http://.*\?"," ",text)

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
    pattern = "(?<=[?|\.|!|:]).*?\?"
    questions = re.findall(pattern,clean_text)
    return questions

def find_questions_by_number(text):
    pattern = "(?<=[1-9][\.|\)]).*?\?"
    question = re.findall(pattern,text)
    return question

def find_questions_after_bullet(text):
    pattern = "(?<=\u2022).*?\?"
    t = re.findall(pattern,text)
    return t

def get_chapters(path):
    files = os.listdir(path)
    return sorted(files)

def get_

path = "/data/madesai/history-llm-data/mi-open-textbooks/Glencoe-US/"
    
#files = ["HSUSFull.pdf"]#,"HSWorld.pdf"]
files = get_chapters(path) # sample first 4 chapters 
for f in files:
    reader = PdfReader(path+f)
    #out_file = open(f[:-4]+".txt","w")
    file_questions = []
    seen_questions = set()
    pages = reader.pages[:-2]
    for page in pages:
        print(page)
    #     raw_text = page.extract_text()
    #     clean_text = remove_whitespaces(raw_text)

    #     questions = find_questions_by_number(clean_text)
    #     if questions: 
    #         for q in questions:
    #             q = q.strip()
    #             if q not in seen_questions:
    #                 file_questions.append(q)
    #                 seen_questions.add(q)
    # for q in file_questions:
    #     out_file.write(q+"\n")
    #out_file.close()






