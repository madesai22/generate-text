import wikipediaapi
import re
import random
from transformers import pipeline, set_seed
from transformers import T5Tokenizer, T5ForConditionalGeneration
import pandas as pd
import requests


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

def get_summary(page):
     first_sentence = page.summary.partition('.')[0] + '.'
     bio_pattern = re.findall("was an?.*\.",first_sentence)
     if bio_pattern:
          # take first sentence after "was an"
          summary = ' '.join(bio_pattern[0].split()[2:])[:-1] 
          return summary
     else: 
          return first_sentence
     

def get_people_who_died_in_year(year):
    cat = wiki_wiki.page("Category:"+str(year)+" deaths")
    return get_category_members(cat.categorymembers)

def get_random_sample(group, nsamples):
    # takes a random sample of names from the return of get_category_members
    random_sample = set()
    group_list = list(group)
    random.shuffle(group_list)
    index = 0
    nchosen = 0
    while nchosen <= nsamples:
         item = group_list[index]
         index +=1
         item_page = wiki_wiki.page(item)
         # doing this here instead of cleaning the whole sample to save time because we are currently randomly sampling 
         # in the future if I do a purposeful sample I will change this
         if not re.findall("^(Category|List|Template)",item) and (get_birth_year(item_page) != YEAR_NOT_FOUND()) : 
              random_sample.add(item)
              nchosen += 1       
    return random_sample


def make_dictionary(group, death_year=None, birth_year=None, category=None):
    # returns a dictionary of {name: {birth_year, death_year, summary, category}, ...}
    sample_dict = {}
    for item in group:
        item_page = wiki_wiki.page(item)
        summary = get_summary(item_page)
        birth_year = get_birth_year(item_page)
        death_year = get_death_year(item_page)
        sample_dict[item] = {"birth_year": birth_year, "death_year": death_year, "summary": summary, "category":category}
    return sample_dict

def initiate_flan5_text_to_text(xxl = False):
    if xxl: 
         tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xxl")
         model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xxl", device_map="auto")
    else:
         tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
         model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base", device_map="auto") 
    return model, tokenizer

def flant5_text_to_text(prompt, model,tokenizer):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
    outputs = model.generate(input_ids)
    return(tokenizer.decode(outputs[0]))

def get_sample_dict_by_death_year(death_year, sample_size):
     people_who_died_in_X_year = get_people_who_died_in_year(death_year)
     random_sample = get_random_sample(people_who_died_in_X_year,sample_size)
     sample_dict = make_dictionary(random_sample, death_year=death_year)
     return sample_dict

def get_sample_dict_by_category(category, sample_size):
     cat = wiki_wiki.page(category)
     category_string = category.partition(':')[2] 
     category_members = get_category_members(cat.categorymembers)
     random_sample = get_random_sample(category_members, sample_size)
     sample_dict = make_dictionary(random_sample, death_year = YEAR_NOT_FOUND(),category=category_string)
     return sample_dict

def get_page_views(name):
    name = name = name.replace(" ", "_")    
    # calling monthly page views 
    address = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/" + name + "/monthly/2015010100/2023083100"
    headers = {'User-Agent': 'GenerateText (madesai@umich.edu)'}

    resp = requests.get(address, headers=headers)
    if resp.ok:
        details = resp.json()
        total_views = 0
        for month in details['items']:
            total_views += month['views']
        return total_views
    else:
         return None
    
def main():
     global wiki_wiki
     wiki_wiki = wikipediaapi.Wikipedia('GenerateText (madesai@umich.edu)', 'en')
     
     sample_1 = get_sample_dict_by_category("Category:Activists", 30)
     sample_2 = get_sample_dict_by_category("Category:Chief executives in the technology industry",30)
     sample_3 = get_sample_dict_by_category("Category:Scientists",30)
     
     sample_dict = dict(sample_1,**sample_2)
     sample_dict.update(sample_3)
     
     df_dict = {'Name':[],'Summary':[],'Category':[],'True birth year': [], 'Predicted birth year':[], "Years off": [], "Full response": []}
     model,tokenizer = initiate_flan5_text_to_text()

     for person in sample_dict:
        # get summary and true birth year
        summary = sample_dict[person]['summary']
        true_birth_year = sample_dict[person]["birth_year"]
        if true_birth_year != YEAR_NOT_FOUND():
            
            category = sample_dict[person]["category"]
            
            # prompt model
            prompt_name = re.sub(r'\([^)]*\)', '', person) # strip parentheses and contents
            prompt = "What year was {} born?".format(prompt_name)
            #prompt = "{} was born in the year".format(prompt_name)
            response = flant5_text_to_text(prompt,model,tokenizer)

            # get prediction 
            years = re.findall("\d{4}",response)
            if years: 
                response_year = int(years[0])
                difference = abs(true_birth_year-response_year)
            else: 
                response_year = "no prediction"
                difference = "n/a"
            
            # add to dataframe dict
            df_dict['Name'].append(person)
            df_dict['Summary'].append(summary)
            df_dict['Category'].append(category)
            df_dict['True birth year'].append(true_birth_year)
            df_dict['Predicted birth year'].append(response_year)
            df_dict['Years off'].append(difference)
            df_dict['Full response'].append(response)

            # print(person, summary,true_birth_year,response_year,difference)

     df = pd.DataFrame(df_dict)
     df.to_csv("./birth_year_predictions.csv")