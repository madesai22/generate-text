from transformers import pipeline, set_seed
from transformers import T5Tokenizer, T5ForConditionalGeneration
import file_handeling as fh
import re

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

def main():
    # load data from json files
     data_path = "/data/madesai/history-llm-data/wikipedia-json-files/"
     data_files = ["confederate_states_army_officers.json"]
     df_dict = {'Name':[],'Summary':[],'Category':[],'True birth year': [], 'Predicted birth year':[], "Years off": [], "Full response": []}

     prompt_form = "What year was {} born?"
     model,tokenizer = initiate_flan5_text_to_text()

     for fname in data_files:
         file = data_path + fname
         data = fh.read_json(file)
         for name in data:
              print(name)
              print(data[name]['birth_year'])
             #prompt = make_prompt(prompt_form, name, clean=True)
             #response = flant5_text_to_text(prompt,model,tokenizer)
             



if __name__ == "__main__":
    main()

           

          

          