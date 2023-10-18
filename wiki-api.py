import wikipediaapi
    
wiki_wiki = wikipediaapi.Wikipedia('GenerateText (madesai@umich.edu)', 'en')
page_py = wiki_wiki.page('Python_(programming_language)')

page_py = wiki_wiki.page('Python_(programming_language)')
print("Page - Exists: %s" % page_py.exists())