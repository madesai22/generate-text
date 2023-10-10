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

unmasker = pipeline('fill-mask', model='bert-base-cased')
example = unmasker("Hello I'm a [MASK] model.")
print(example)