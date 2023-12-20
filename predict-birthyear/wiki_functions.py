import wikipediaapi
import re
import requests

def initiate_request():
    global wiki_wiki
    wiki_wiki = wikipediaapi.Wikipedia('GenerateText (madesai@umich.edu)', 'en')
    return wiki_wiki

def get_category_members(categorymembers, level = 0, max_level = 1, category_set = set()):
    for c in categorymembers.values():
            category_set.add(c.title)
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                get_category_members(c.categorymembers, level=level + 1, max_level=max_level,category_set=category_set)
    return category_set

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
    
def get_summary(page):
     first_sentence = page.summary.partition('.')[0] + '.'
     bio_pattern = re.findall("was an?.*\.",first_sentence)
     if bio_pattern:
          # take first sentence after "was an"
          summary = ' '.join(bio_pattern[0].split()[2:])[:-1] 
          return summary
     else: 
          return first_sentence
     
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

def get_people_who_died_in_year(year,wiki_wiki):
    cat = wiki_wiki.page("Category:"+str(year)+" deaths")
    return get_category_members(cat.categorymembers)

