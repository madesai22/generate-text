from transformers import pipeline, set_seed


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
response = gpt_2_generate(prompt)
print(response)