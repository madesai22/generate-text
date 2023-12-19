import file_handeling as fh 
import os
import random 

directory = "/data/madesai/history-llm-data/wikipedia-json-files"

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    data = fh.read_jsonlist(f)
    print(random.sample(dict.items,10))