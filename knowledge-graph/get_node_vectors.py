import json
import fasttext

import numpy as np

def is_number(s):
    #https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
    return s.replace('.','',1).isdigit()

#import fasttext vectors

#for each node
    #get vector for node
    #add node (key) and vector (value) to dictionary
#write dictionary to file

f = open('./data/nodes.json', 'r') # Get relationships with weights data (we just need the nodes)
nodes = json.load(f)

print('Loading Fasttext model')
wiki_model = fasttext.load_model('./data/wiki.en.bin')
print('Finished loading Fasttext model')

node_vectors = {}

print('Getting vectors for each node')
for node, node_tokens in nodes.items():
    node_vectors[node] =  np.zeros(300)
    for token in node_tokens:
        if token in ['(', ')', ',', '%'] or is_number(token):
            continue
        else:
            token_array = np.array(wiki_model[token])
            node_vectors[node] = np.add(node_vectors[node], token_array)
    node_vectors[node] = node_vectors[node].tolist()
print('Finished getting vectors')

print('Writing vectors to file')
with open('./data/node_vectors.json','w') as nv: # Write the data to a file
    nv.write(json.dumps(node_vectors))
print('Finished writing vectors file')