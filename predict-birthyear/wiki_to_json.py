import wikipediaapi
import re
import random
import requests
import file_handeling as fh
from numba import jit, cuda



# category functions: 
def get_category_members(categorymembers, level = 0, max_level = 1, category_set = set()):
    for c in categorymembers.values():
            category_set.add(c.title)
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                get_category_members(c.categorymembers, level=level + 1, max_level=max_level,category_set=category_set)
    return category_set

def get_people_who_died_in_year(year):
    cat = wiki_wiki.page("Category:"+str(year)+" deaths")
    return get_category_members(cat.categorymembers)

# making random sample functions: 
def get_random_sample(group, nsamples, clean = False):
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
         if (not clean) or (not re.findall("^(Category|List|Template)",item) and (get_birth_year(item_page) != YEAR_NOT_FOUND())) : 
              random_sample.add(item)
              nchosen += 1       
    return random_sample

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


# attribute functions: 

def YEAR_NOT_FOUND():
    return -1999

def get_birth_death_year(page):
    birth_year = YEAR_NOT_FOUND()
    death_year = YEAR_NOT_FOUND()
    categories = page.categories
    for title in sorted(categories.keys()):
        if re.findall("Category:\d{4}\sbirths",title): birth_year = int(re.findall("\d{4}", title)[0])
        if re.findall("Category:\d{4}\sdeaths",title): death_year = int(re.findall("\d{4}", title)[0])

    return birth_year, death_year

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
     if len(page.summary.partition('.')[0]) > 5: 
        first_sentence = page.summary.partition('.')[0] + '.'
     else: 
        first_sentence = page.summary.partition('.')[1] + '.'
     bio_pattern = re.findall("was an?.*\.",first_sentence)
     if bio_pattern:
          # take first sentence after "was an"
          summary = ' '.join(bio_pattern[0].split()[2:])[:-1] 
          return summary
     else: 
          return first_sentence
     
def get_page_views(page):
    name = page.fullurl.removeprefix("https://en.wikipedia.org/wiki/")
   # name = name.replace(" ", "_")    
    # calling monthly page views 
    address = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/" + name + "/monthly/2015010100/2023083100"
    headers = {'User-Agent': 'GenerateText (madesai@umich.edu)'}

    resp = requests.get(address, headers=headers, timeout=20.0)
    if resp.ok:
        details = resp.json()
        total_views = 0
        for month in details['items']:
            total_views += month['views']
        return total_views
    else:
         return None
    
# organizing data:
@jit(target_backend='cuda',nopython=True)  
def make_dictionary_long(group, death_year=None, birth_year=None, category=None, clean = True, born_before = 2023):
    # takes a set of strings (wikipedia names)
    # returns a dictionary of {name: {birth_year, death_year, summary, category, page_views}, ...}
    sample_dict = {}
    for item in group:
        item_page = wiki_wiki.page(item)
        birth_year, death_year = get_birth_death_year(item_page)
        if birth_year < born_before: 
            if (not clean) or ( not re.findall("^(Category|List|Template)",item)): #and (get_birth_year(item_page) != YEAR_NOT_FOUND())):
                item_page = wiki_wiki.page(item)
                summary = get_summary(item_page)
                page_views = get_page_views(item_page)
                sample_dict[item] = {"birth_year": birth_year, "death_year": death_year, "summary": summary, "category":category, "page_views": page_views}
    return sample_dict

def make_dictionary(group, birth_year):
    sample_dict = {}
    for item in group:
        sample_dict[item] = {"birth_year": birth_year}
    return sample_dict

# get sample here: 
def make_year_categories(start_year = 1600, end_year = 2000):
    year_cat_list = []
    for year in range(start_year,end_year+1):
        year_cat_list.append("Category:{} births".format(year))
    return year_cat_list

    # then need to get page views and save in JSON format 

def main():
     global wiki_wiki
     wiki_wiki = wikipediaapi.Wikipedia('GenerateText (madesai@umich.edu)', 'en')
     out_path = "/data/madesai/history-llm-data/wikipedia-json-files/"
     
     for year in range(1,100):
     #category_csv = open("./make_categories.csv","r")
     #for line in category_csv.readlines()[1:]:
         #items = line.split(";")
         #category = items[0].strip()
         #born_before = int(items[1])
         #born_after = int(items[2])
         category = "Category:{} births".format(year)
         birth_year = year
         file_name = category.partition(':')[2].lower().replace(" ","_")+".json"
         print(category,file_name)
         wiki_cat = wiki_wiki.page(category)
         category_members = get_category_members(wiki_cat.categorymembers)
         
         print(len(category_members))
         data = make_dictionary(category_members,birth_year=birth_year)
         #data = make_dictionary(category_members,category=category.partition(':')[2],clean=True,born_before=born_before)
         print("{} items in {}.".format(len(data), category))
    
         fh.write_to_json(data,out_path+file_name)


     
        #  dictionary_list = []
        #  for c in categories:
        #      print(c)
        #      wiki_cat = wiki_wiki.page(c)
        #     # wiki_cat = wiki_wiki.page(c.partition(':')[2])
        #      category_members = get_category_members(wiki_cat.categorymembers)
        #      category_dictionary = make_dictionary(category_members,category=c.partition(':')[2],clean=True,born_before=born_before)
        #      dictionary_list.append(category_dictionary)
        #      print("{} items in {}.".format(len(category_dictionary), c))
        #  data = dict()
        #  for d in dictionary_list:
        #      data.update(d)

         

if __name__ == "__main__":
    main()