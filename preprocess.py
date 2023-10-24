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