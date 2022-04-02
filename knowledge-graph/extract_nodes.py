import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

def getNodeWords(node): # Tokenize and remove stop words
	words = node.split('_')
	wordsCombined = ''
	for word in words:
		wordsCombined += word + ' '
	tokenizedWords = word_tokenize(wordsCombined)
	filtered_words = [word for word in tokenizedWords if not word in stop_words]
	return filtered_words

f = open('./data/relationships_with_weights.json', 'r') # Get relationships with weights data (we just need the nodes)
relationships_with_weights = json.load(f)

nodes = {}

for node, connected_nodes in relationships_with_weights.items(): # For the nodes and the nodes they are connected to
	if node not in nodes: # If the node has not been seen
		nodes[node] = getNodeWords(node) # Add it to the nodes dict and get the word list for the node name
		for connected_node in connected_nodes: # For all the connected nodes for this node
			if connected_node not in nodes: # If the connected node has not been seen
				nodes[connected_node] = getNodeWords(connected_node) # Add it to the nodes dict and get the word list for the node name

with open('./data/nodes.json','w') as f: # Write the data to a file
	f.write(json.dumps(nodes, indent = 6))


