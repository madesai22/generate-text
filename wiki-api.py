import wikipediaapi
import re
import random

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
        if not birth_year: birth_year = get_birth_year(wiki_wiki.page(item))
        if not death_year: death_year = get_death_year(wiki_wiki.page(item))
        sample_dict[item] = {"birth_year": birth_year, "death_year": death_year}
    return sample_dict



wiki_wiki = wikipediaapi.Wikipedia('GenerateText (madesai@umich.edu)', 'en')
#page_py = wiki_wiki.page('Dennis Adams_(boxer)')


#birth_year = get_birth_year(page_py)
#death_year = get_death_year(page_py)

#print("birth year: {}, death year: {}".format(birth_year,death_year))


people_died_in_1931 = get_people_who_died_in_year(1930)
random_sample = get_random_sample(people_died_in_1931,10)
sample_dict = make_dictionary(random_sample, death_year=1930)
print(sample_dict)
#print(len(people_died_in_1931))


prompt = "{} was born in the year [MASK]."

