import re
from unidecode import unidecode
import string

def remove_whitespaces(text,paragraph=False):
    if paragraph:
       return re.sub(' +|\t+', ' ', text)
    else:
       end_chars = re.sub('\n','',text)
       return re.sub(' +|\t+', ' ', end_chars)

def strip_punctuation(text):
    text =  unidecode(text)
    return text.translate(str.maketrans('', '', string.punctuation))

def tokenize(text, stopwords=None):
    if stopwords:
        text = [token for token in text.split() if token not in stopwords]
    else: 
        text = [token for token in text.split()]
    return text

def find_questions(text):
    # find question area:
    question_area = re.findall("QUESTIONS TO GUIDE INQUIRY\s[0-9]\.\s.*\?",text)[0]
    question_area = re.sub("QUESTIONS TO GUIDE INQUIRY\s","",question_area) # remove header

    # split questions:
    question_list = re.split("\s?[0-9]+\.\s", question_area)
    question_list = list(filter(None, question_list)) # remove empty items
    return question_list





