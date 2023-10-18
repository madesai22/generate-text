import wikipediaapi


def print_categories(page):
        categories = page.categories
        for title in sorted(categories.keys()):
            print("%s: %s" % (title, categories[title]))

def check_exists(page):
    print("Page - Exists: %s" % page.exists())

    
wiki_wiki = wikipediaapi.Wikipedia('GenerateText (madesai@umich.edu)', 'en')
page_py = wiki_wiki.page('Dennis Adams_(boxer)')

print_categories(page_py)



