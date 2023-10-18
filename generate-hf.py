from transformers import pipeline, set_seed
from transformers import T5Tokenizer, T5ForConditionalGeneration



#prompt = "Theodore Roosevelet was born in the year [MASK]." # BERT uses these kinds of mask tokens
def bert_fill_mask(prompt):
     unmasker = pipeline('fill-mask', model='bert-base-cased')
     response = unmasker(prompt)
     return response

#prompt = "Theodore Roosevelet was born in the year <mask>."
def roberta_fill_mask(prompt):
    unmasker = pipeline('fill-mask', model='roberta-base')
    response = unmasker(prompt)
    return(response)

def gpt_2_generate(prompt):
    generator = pipeline('text-generation', model='gpt2')
    set_seed(42)
    response = generator(prompt, max_length=100, num_return_sequences = 3)
    return response


     
prompt = "Fill in the prompt. Theodore Roosevelet was born in the year <mask>."
prompt = """Fill in the prompt. Example: 

Input: Martin Luther King was born in the year <mask>.
Output: 1929

Input: Theodore Roosevelet was born in the year <mask>.
Output: 

"""

prompt = "What year was Theodore Roosevelt born?"
#prompt = "translate English to German: How old are you?"
def flant5_text_to_text(prompt):
    # text2text_generator = pipeline("text2text-generation",model ="google/flan-t5-base")
    # response = text2text_generator(prompt)

    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(input_ids)
    return(tokenizer.decode(outputs[0]))

response = flant5_text_to_text(prompt)
print(response)