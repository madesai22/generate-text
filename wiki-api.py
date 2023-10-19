import wikipediaapi
import re
import random
from transformers import pipeline, set_seed
from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd


def print_categories(page):
        categories = page.categories
        for title in sorted(categories.keys()):
            print(title)
         #   print("%s: %s" % (title, categories[title]))

def check_exists(page):
    print("Page - Exists: %s" % page.exists())

def print_categorymembers(categorymembers, level=0, max_level=1):
        for c in categorymembers.values():
            print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)

def get_category_members(categorymembers, level = 0, max_level = 1, category_set = set()):
    for c in categorymembers.values():
            category_set.add(c.title)
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                get_category_members(c.categorymembers, level=level + 1, max_level=max_level,category_set=category_set)
    return category_set

def YEAR_NOT_FOUND():
    return -1999

def get_birth_year(page):
    birth_year = YEAR_NOT_FOUND()
    categories = page.categories
    for title in sorted(categories.keys()):
        if re.findall("Category:\d{4}\sbirths",title): birth_year = int(re.findall("\d{4}", title)[0])
    return birth_year

def get_death_year(page):
    death_year = YEAR_NOT_FOUND()
    categories = page.categories
    for title in sorted(categories.keys()):
        if re.findall("Category:\d{4}\sdeaths",title): death_year = int(re.findall("\d{4}", title)[0])
    return death_year

def get_people_who_died_in_year(year):
    cat = wiki_wiki.page("Category:"+str(year)+" deaths")
    return get_category_members(cat.categorymembers)

def get_random_sample(group, nsamples):
    return random.sample(group, nsamples)

def make_dictionary(group, death_year=None, birth_year=None):
    sample_dict = {}
    for item in group:
        item_page = wiki_wiki.page(item)
        if not birth_year: birth_year = get_birth_year(item_page)
        if not death_year: death_year = get_death_year(item_page)
        summmary = item_page.summary[0:60]
        sample_dict[item] = {"birth_year": birth_year, "death_year": death_year, "summary": summmary}
    return sample_dict



def initiate_flan5_text_to_text():
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base", device_map="auto")
    return model, tokenizer

def flant5_text_to_text(prompt, model,tokenizer):
    # text2text_generator = pipeline("text2text-generation",model ="google/flan-t5-base")
    # response = text2text_generator(prompt)
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
    outputs = model.generate(input_ids)
    return(tokenizer.decode(outputs[0]))



wiki_wiki = wikipediaapi.Wikipedia('GenerateText (madesai@umich.edu)', 'en')

people_died_in_1931 = get_people_who_died_in_year(1930)
random_sample = get_random_sample(people_died_in_1931,10)
sample_dict = make_dictionary(random_sample, death_year=1930)
print(sample_dict)

df_dict = {'Name':[],'Summary':[],'True birth year': [], 'Predicted birth year':[], "Years off": []}
#df = pd.DataFrame(columns=['Name','Summary','True birth year', 'Predicted birth year', 'Years off'])
model,tokenizer = initiate_flan5_text_to_text()
for person in sample_dict:
     
     # get summary and true birth year
     summary = sample_dict[person]['summary']
     true_birth_year = sample_dict[person]["birth_year"]
    
     # prompt model
     prompt = "What year was {} born?".format(person)
     response = flant5_text_to_text(prompt,model,tokenizer)

     # get prediction 
     years = re.findall("\d{4}",response)
     if years: 
          response_year = int(years[0])
          difference = true_birth_year-response_year
     else: 
          response_year = "no prediction"
          difference = "n/a"
     
     # add to dataframe dict
     df_dict['Name'].append(person)
     df_dict['Summary'].append(summary)
     df_dict['True birth year'].append(true_birth_year)
     df_dict['Predicted birth year'].append(response_year)
     df_dict['Years off'].append(difference)

     print(person, summary,true_birth_year,response_year,difference)

     

df = pd.DataFrame(df_dict)
df.to_csv("./birth_year_predictions.csv")

     
     
        


    
# possibly useful: page_py.summary[0:60]


