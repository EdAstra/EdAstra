import json

f = open('relationships.json', 'r')
relationships = json.load(f)

node_dict = {}

for rel in relationships:
	if rel[0] not in node_dict:
		node_dict[rel[0]] = {rel[2]: rel[1]}
	elif rel[2] not in node_dict[rel[0]]:
		node_dict[rel[0]][rel[2]] = rel[1]
	else:
		node_dict[rel[0]][rel[2]] += rel[1]

with open('relationships_with_weights.json','w') as f:
	f.write(json.dumps(node_dict, indent = 6))