from transformers import pipeline, set_seed
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
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

def initiate_gpt2(medium = False):
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    tokenizer.enable_padding()
    model = AutoModelForCausalLM.from_pretrained("gpt2", device_map="auto")
    if medium: 
        tokenizer = AutoTokenizer.from_pretrained("gpt2-medium")
        model = AutoModelForCausalLM.from_pretrained("gpt2-medium", device_map="auto")
    return model, tokenizer

def gpt2_text_to_text(prompt, model, tokenizer):
    if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
    input_ids = tokenizer(prompt, return_tensors='pt').input_ids.to("cuda")
    outputs = model.generate(input_ids, pad_token_id=tokenizer.pad_token_id, max_new_tokens=300)
    return (tokenizer.decode(outputs[0], skip_special_tokens=True))


def gpt_2_generate(prompt):
    generator = pipeline('text-generation', model='gpt2')
    set_seed(42)
    response = generator(prompt, max_length=300, num_return_sequences = 1)
    return response



def strip_repsonse(text):
    text = re.sub("<pad> ","",text)
    text = re.sub("</s>","",text)
    return text



def main():
    question_fname = ["HSUSFull.txt","HSWorld_clean.txt"]
    path_to_questions = "/home/madesai/generate-text/get-textbook-questions/"
    #model,tokenizer = initiate_flan5_text_to_text(xxl=True)
    model, tokenizer = initiate_gpt2()
    

    response_dict = {"Question":[],"Response":[]}

    test = 0 
    for qf in question_fname:
        outfile = open(qf[:-4]+"-gpt2-response.csv","w")
        question_file = open(path_to_questions+qf,"r")
        for prompt in question_file:
            #raw_response = gpt_2_generate(prompt)
            #response = raw_response[0]["generated_text"]
            response = gpt2_text_to_text(prompt,model,tokenizer)
            #response = flant5_text_to_text(prompt,model,tokenizer)
            response = strip_repsonse(response)
            response_dict["Question"].append(prompt)
            response_dict["Response"].append(response)
           
            df = pd.DataFrame(response_dict)
             
            df.to_csv(outfile,sep=";")
            test += 1
            if test %10 == 0:
                print(test, prompt, response)
        df = pd.DataFrame(response_dict)
        df.to_csv(outfile,sep=";")



if __name__ == "__main__":
    main()
