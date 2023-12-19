import file_handeling as fh 
import os
import random 
from numba import jit, cuda

#@jit(target_backend='cuda')
def open_files():
    directory = "/data/madesai/history-llm-data/wikipedia-json-files"

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        data = fh.read_json(f)
        print(random.sample(dict.items,10))

if __name__=="__main__":
    open_files()