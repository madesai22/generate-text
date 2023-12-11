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

def find_section_questions(text):
    pattern = "Checking for Understanding"
    return re.findall(pattern,text)

def section_questions(text):
    pattern = "Checking for Understanding.*?Write.*?\."
    return re.findall(pattern,text)

def split_section_questions(text):
    pattern = "Checking for Understanding.*?Write.*?\."
    questions = []
    question_area = re.findall(pattern,text)
    if question_area:
        question_area = question_area[0] 
        pattern = "Reviewing Themes|Critical Thinking|Analyzing Visuals"
        q = re.split(pattern, question_area)
        for i in q:
            questions += (re.split("[1-9]\.\s+", i))
    return questions





path = "/data/madesai/history-llm-data/Glencoe-US/"
    
#files = ["HSUSFull.pdf"]#,"HSWorld.pdf"]
files = get_chapters(path) # sample first 4 chapters 
for f in files:
    reader = PdfReader(path+f)
    #out_file = open(f[:-4]+".txt","w")
    file_questions = []
    seen_questions = set()
    pages = reader.pages#[-2:]
    for page in pages:
        
        raw_text = page.extract_text()
        clean_text = remove_whitespaces(raw_text)
        if find_section_questions(clean_text):
            print(path+f)
            questions = split_section_questions(clean_text)
            #question_section = section_questions(clean_text)

          #  find_questions_by_number(question_section)
            pattern = "[1-9]\.\s+"
            print(questions)
           # print(question_section[0])
            #q = re.split(pattern, question_section[0])
            #print(q)
            print("***")

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






