from PyPDF2 import PdfReader
import os
import re
from unidecode import unidecode
import string
from datetime import date

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

def section_questions(text,removed):
    pattern = "Checking for Understanding.*?Write.*?\."
    questions = []
    return_questions = []
    question_area = re.findall(pattern,text)
    if question_area:
        question_area = question_area[0] 
        pattern = "Reviewing Themes|Critical Thinking|Analyzing Visuals"
        q = re.split(pattern, question_area)
        for i in q:
            questions += (re.split("[1-9]\.\s+", i))
            for q in questions:
                q = q.strip()
                if q and not re.findall(removed,q):
                    q = remove_question_type_words(q)
                    return_questions.append(q)
    return return_questions[1:] # first question is always "Checking for Understanding"

def remove_question_type_words(q):
    split_point = 0
    q_list = q.split()
    if len(q_list)>50:
        return " "

    if len(q_list[0])>4 and q_list[0][-3:] == "ing":
        q = " ".join(q_list[1:])

    for count, word in enumerate(q_list[:5]):
        if word == "What" or word == "How" or word == "Which" or word =="Were" or word =="Identify:" or word == "Define:":
            split_point = count
        elif word == "Writing":
            split_point = count + 1
    q = " ".join(q_list[split_point:])

    
    return q



def update_readme(path_to_readme, filename,path_to_data,removed):
    f = open(path_to_readme,"a")
    today = str(date.today())
    out_string = "{};{};{};{}\n".format(filename,today,path_to_data,removed)
    f.write(out_string)
    f.close()


path_to_data = "/data/madesai/history-llm-data/Glencoe-US/"
path_to_readme = "./readme.txt"
removed = "graphic organizer|above|below|page"
out_file = "Glencoe-US-section-questions.txt"
update_readme(path_to_readme,out_file,path_to_data,removed)
#files = ["HSUSFull.pdf"]#,"HSWorld.pdf"]

file_questions = [] # use to keep order of questions 
seen_questions = set() # to remove duplicates 
files = get_chapters(path_to_data)

for f in files:
    reader = PdfReader(path_to_data+f)
    pages = reader.pages
    for page in pages:
        raw_text = page.extract_text()
        clean_text = remove_whitespaces(raw_text)

        if find_section_questions(clean_text):
            questions = section_questions(clean_text,removed)
            for q in questions:
                if q not in seen_questions:
                    file_questions.append(q)
                    seen_questions.add(q)
of = open(out_file,"w")
for q in file_questions:
    of.write(q+"\n")
of.close()






