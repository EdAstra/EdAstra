import json
import fasttext
import fasttext.util

import numpy as np

def is_number(s):
    #https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
    return s.replace('.','',1).isdigit()

f = open('./data/nodes_academic_disciplines_beta.json', 'r') # Get relationships with weights data (we just need the nodes)
nodes = json.load(f)

print('Loading Fasttext model')
wiki_model = fasttext.load_model('./data/wiki.en.bin')
print('Finished loading Fasttext model')
print('Reducing model dimensions to 3')
fasttext.util.reduce_model(wiki_model, 3)
print('Finished dimension reduction to',wiki_model.get_dimension())

node_vectors = {}

print('Getting vectors for each node')
for node, node_tokens in nodes.items():
    node_vectors[node] =  np.zeros(3)
    for token in node_tokens:
        if token in ['(', ')', ',', '%'] or is_number(token):
            continue
        else:
            token_array = np.array(wiki_model[token])
            node_vectors[node] = np.add(node_vectors[node], token_array)
    node_vectors[node] = node_vectors[node].tolist()
print('Finished getting vectors')

print('Writing vectors to file')
with open('./data/node_vectors_academic_disciplines_beta.json','w') as nv: # Write the data to a file
    nv.write(json.dumps(node_vectors, indent = 6))
print('Finished writing vectors file')