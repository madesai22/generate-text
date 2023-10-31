import wikipediaapi
import requests
# only english language pages
#api = wikipediaapi.Wikipedia('en')

def WikiPageView(name):
    
    # Calling monthly page views of each species 
    address = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/" + name + "/monthly/2015010100/2020123100"

    # Personal username for identification for the Wikipedia API
    headers = {'User-Agent': 'GenerateText (madesai@umich.edu)'}
    
    resp = requests.get(address, headers=headers)
    details = resp.json()
    
    return details 

wiki_wiki = wikipediaapi.Wikipedia('GenerateText (madesai@umich.edu)', 'en')
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

for n in range(len(wikiurls)):
    title = wikiurls[n]['url'].removeprefix("https://en.wikipedia.org/wiki/")
    result = WikiPageView(title)
    print(result)