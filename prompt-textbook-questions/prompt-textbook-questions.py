from transformers import pipeline, set_seed
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import GPT2LMHeadModel, GPT2Tokenizer
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



def strip_repsonse(text):
    text = re.sub("<pad> ","",text)
    text = re.sub("</s>","",text)
    return text

def main():

    question_fname = ["Glencoe-US-section-questions-clean.txt"]
    path_to_questions = "/home/madesai/generate-text/get-textbook-questions/"
    #model,tokenizer = initiate_flan5_text_to_text(xxl=True)
    model, tokenizer = initiate_gpt2(large=True)
    set_seed(42)

    response_dict = {"Question":[],"Response":[]}

    test = 0 
    for qf in question_fname:
        outfile = open(qf[:-4]+"-gpt2-mcgraw-hill","w")
        question_file = open(path_to_questions+qf,"r")
        for prompt in question_file[10]:
            check_list_prompt = prompt.split(": ")
            # if check_list_prompt[0] == "Define":
            #     for item in check_list_prompt[1].split(", "): 
            #         prompt = "{} is".format(item)
            if check_list_prompt[0] == "Identify":
                for item in check_list_prompt[1].split(", "):
                    prompt = "{} was ".format(item)
                    response = gpt2_text_to_text(prompt,model,tokenizer)
                    #response = flant5_text_to_text(prompt,model,tokenizer)
                    response = strip_repsonse(response)
                    response_dict["Question"].append(prompt)
                    response_dict["Response"].append(response)
            else:
                response = gpt2_text_to_text(prompt,model,tokenizer)
                response = strip_repsonse(response)
                response_dict["Question"].append(prompt)
                response_dict["Response"].append(response)
            
            test += 1
            if test %10 == 0:
                print(test, prompt, response)
        df = pd.DataFrame(response_dict)
        df.to_csv(outfile,sep=";")



if __name__ == "__main__":
    main()
