import file_handeling as fh 
import os
import random 
from numba import jit, cuda

#@jit(target_backend='cuda')
def open_files():
    directory = "/data/madesai/history-llm-data/wikipedia-json-files/"
    filename = "all_wiki.json"
    #for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    data = fh.read_json(f)
    print(len(data))

def open_seen_keys():
    dir = "/data/madesai/history-llm-data/seen_keys.pkl"
    key_list = fh.unpickle_data(dir)
    print("list n: {}".format(len(key_list)))

    key_set = list(set(key_list))
    print("set n: {}".format(len(key_set)))
    fh.pickle_data(set(key_list),dir)

if __name__=="__main__":
    open_seen_keys()