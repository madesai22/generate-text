# import relevant stuff
from transformers import pipeline
#from transformers import BertTokenizer, BertModel

# preprocess prompt text 
#tokenizer = BertTokenizer.from_pretrained('bert-base-cased')


# get model 
#model = BertModel.from_pretrained("bert-base-cased")

#text = "Replace me by any text you'd like."
#encoded_input = tokenizer(text, return_tensors='pt')
#output = model(**encoded_input

#unmasker = pipeline('fill-mask', model='bert-base-cased')
#example = unmasker("Hello I'm a [MASK] model.")

generate = pipeline('text-generation', model='bert-base-cased',is_decoder=True)
gen_example = generate("When I went there it was")

print(gen_example)