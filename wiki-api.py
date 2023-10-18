import wikipediaapi


def print_categories(page):
        categories = page.categories
        for title in sorted(categories.keys()):
            print(title)
            print("%s: %s" % (title, categories[title]))

def check_exists(page):
    print("Page - Exists: %s" % page.exists())

def print_categorymembers(categorymembers, level=0, max_level=1):
        for c in categorymembers.values():
            print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
            if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
                print_categorymembers(c.categorymembers, level=level + 1, max_level=max_level)
#def get_birth_year(page):
#    categories = page.categories
#    if 

    
wiki_wiki = wikipediaapi.Wikipedia('GenerateText (madesai@umich.edu)', 'en')
page_py = wiki_wiki.page('Dennis Adams_(boxer)')

print_categories(page_py)



