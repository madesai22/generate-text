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


def flant5_text_to_text(prompt):
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base", device_map="auto")
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
    outputs = model.generate(input_ids,return_dict_in_generate=True,output_scores=True)
    input_length = input_ids.shape[1]
    transition_scores = model.compute_transition_scores(outputs.sequences, outputs.scores, normalize_logits=True)
    generated_tokens = outputs.sequences[:, input_length:]
    print("input ids: {}".format(input_ids))
    print("output.sequences: {}".format(outputs.sequences))
    print("transition scores: {}".format(transition_scores))

    for tok, score in zip(generated_tokens[0], transition_scores[0]):
        # | token | token string | logits | probability
        print(f"| {tok:5d} | {tokenizer.decode(tok):8s} | {score.numpy():.4f} | {np.exp(score.numpy()):.2%}")
    return "done"

     
prompt = "Fill in the prompt. Theodore Roosevelet was born in the year <mask>."
prompt = """Fill in the prompt. Example: 

Input: Martin Luther King was born in the year <mask>.
Output: 1929

Input: Theodore Roosevelet was born in the year <mask>.
Output: 

"""

prompt = "What year was Theodore Roosevelt born?"
#prompt = "translate English to German: How old are you?"


response = flant5_text_to_text(prompt)
print(response)

prompt = "What is 9 times 30?"
response = flant5_text_to_text(prompt)
print(response)