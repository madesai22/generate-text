from transformers import pipeline, set_seed
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import pandas as pd
import re
from string import punctuation


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

def initiate_gpt2(medium = False, large = False):
    if medium: 
        model = GPT2LMHeadModel.from_pretrained("gpt2-medium",device_map="auto")
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2-medium")
    elif large:
        model = GPT2LMHeadModel.from_pretrained("gpt2-large",device_map="auto")
        tokenizer = GPT2Tokenizer.from_pretrained("gpt2-large")
    else:
       tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
       model = GPT2LMHeadModel.from_pretrained("gpt2",device_map="auto")    
    return model, tokenizer

def gpt2_text_to_text(prompt, model, tokenizer):
    input_ids = tokenizer(prompt, return_tensors='pt').input_ids.to("cuda")
   # outputs = model.generate(input_ids, pad_token_id=tokenizer.eos_token_id, max_new_tokens=200, do_sample = True) # do_sample = True, top_k=50)
    # contrastive search
    outputs = model.generate(input_ids, pad_token_id=tokenizer.eos_token_id, penalty_alpha=0.6, top_k=4, max_new_tokens=200)
    return (tokenizer.decode(outputs[0], skip_special_tokens=True))


def gpt_2_generate(prompt):
    generator = pipeline('text-generation', model='gpt2')
  #  generator = pipeline('question-answering', model='gpt2')
    set_seed(42)
    response = generator(prompt, max_new_tokens=300, num_return_sequences = 1)
    return response

def remove_prompt_from_response(prompt, response):
    len_prompt = len(prompt.split())
    if response.split()[:len_prompt] == prompt.split():
        response =  " ".join(response.split()[len_prompt:])
    return response

def strip_repsonse(text):
    text = re.sub("<pad> ","",text)
    text = re.sub("</s>","",text)
    return text

def main():
    
    prompt_fname = "Glencoe-US-section-questions-clean-prompts.txt"
    path_to_prompts = "/home/madesai/generate-text/prompt-textbook-questions/prompts/"
    prompt_file = open(path_to_prompts+prompt_fname, "r")
    outfile = open(prompt_fname[:-4]+"-gpt2-contrastive.csv","w")

    #model,tokenizer = initiate_flan5_text_to_text(xxl=True)
    model, tokenizer = initiate_gpt2(large=True)
    set_seed(42)

    response_dict = {"Question":[],"Response":[]}
    count = 0 
    for prompt in prompt_file:
        response = gpt2_text_to_text(prompt,model,tokenizer)
        response = strip_repsonse(response)
        response = remove_prompt_from_response(prompt,response)
        response_dict["Question"].append(prompt)
        response_dict["Response"].append(response)
        if count %10 == 0:
            print(prompt)
            print(response)
        count +=1
    
    df = pd.DataFrame(response_dict)
    df.to_csv(outfile,sep=";")



if __name__ == "__main__":
    main()
