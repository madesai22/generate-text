import wikipediaapi
# only english language pages
#api = wikipediaapi.Wikipedia('en')

species = ["eschrichtius robustus"]

wikiurls = []
# loop through the unique species names
for name in species:
    # Spaces to be replaced with underscore for Wiki's API
    name = name.replace(" ", "_")
   # p = api.page(name)
    p = wiki_wiki.page(name)

    # Store the url retrieved and name we called with
    data = {'url': p.fullurl, 'scientific_name': name}
    # Append dictionary to list
    wikiurls.append(data)