from transformers import pipeline, set_seed
from transformers import T5Tokenizer, T5ForConditionalGeneration
import file_handeling as fh
import re
import numpy as np
import random
import pandas as pd


# load models
def initiate_flan5_text_to_text(xxl = False):
    if xxl: 
         tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xxl")
         model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xxl", device_map="auto")
    else:
         tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
         model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base", device_map="auto") 
    return model, tokenizer

def flant5_text_to_text(prompt, model,tokenizer):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
    outputs = model.generate(input_ids)
    return(tokenizer.decode(outputs[0]))

def make_prompt(prompt_form, name, clean = False):
     if clean:
          name = re.sub(r'\([^)]*\)', '', name)
     return prompt_form.format(name)

def bin_data_by_pageview(data):
    # go through data once to get spread:
    pageviews_list = [] 
    for name in data:
        pageviews_list.append(data[name]['page_views'])

    




def main():
     outfile = "birth_year_predict.csv"
    # load data from json files
     data_path = "/data/madesai/history-llm-data/wikipedia-json-files/"
     data_files = ["confederate_states_army_officers.json","american_civil_war_nurses.json","african_americans_in_the_american_civil_war.json"]
     df_dict = {'Name':[],'Summary':[],'Category':[],'True birth year': [], 'Pageviews':[],'Predicted birth year':[], "Years off": [], "Full response": []}

     prompt_form = "What year was {} born?"
     model,tokenizer = initiate_flan5_text_to_text()

     for fname in data_files:
         file = data_path + fname
         data = fh.read_json(file)
         random.shuffle(data)
         
         for name in data:
            birth_year = data[name]['birth_year']
            summary = data[name]['summary']
            category = data[name]['category']
            true_birth_year = data[name]['birth_year']
            page_views = data[name]['page_views']

            prompt = make_prompt(prompt_form, name, clean=True)
            response = flant5_text_to_text(prompt,model,tokenizer)

            prediction_year = re.findall("\d{4}",response)
            if prediction_year:
                response_year = int(prediction_year[0])
                difference = abs(true_birth_year-response_year)
                
            else: 
                response_year = "no prediction"
                difference = "n/a"
            df_dict['Name'].append(name)
            df_dict['Summary'].append(summary)
            df_dict['Category'].append(category)
            df_dict['True birth year'].append(true_birth_year)
            df_dict['Pageviews'].append(page_views)
            df_dict['Predicted birth year'].append(response_year)
            df_dict['Years off'].append(difference)
            df_dict['Full response'].append(response)
            
     df = pd.DataFrame(df_dict)
     df.to_csv(outfile,sep=";")



         
             



if __name__ == "__main__":
    main()

           

          

          