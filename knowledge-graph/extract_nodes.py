import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))

def getNodeWords(node):
	words = node.split('_')
	wordsCombined = ''
	for word in words:
		wordsCombined += word + ' '
	tokenizedWords = word_tokenize(wordsCombined)
	filtered_words = [word for word in tokenizedWords if not word in stop_words]
	return filtered_words


f = open('./data/relationships_with_weights.json', 'r')
relationships_with_weights = json.load(f)

nodes = {}

for node, connected_nodes in relationships_with_weights.items():
	if node not in nodes:
		nodes[node] = getNodeWords(node)
		for connected_node in connected_nodes:
			if connected_node not in nodes:
				nodes[connected_node] = getNodeWords(connected_node)

with open('./data/nodes.json','w') as f:
	f.write(json.dumps(nodes, indent = 6))


