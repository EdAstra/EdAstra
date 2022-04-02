import json

f = open('./data/relationships.json', 'r')
relationships = json.load(f)

nodes = {}

for rel in relationships:
	if rel[0] not in nodes:
		nodes[rel[0]] = {rel[2]: rel[1]}
	elif rel[2] not in nodes[rel[0]]:
		nodes[rel[0]][rel[2]] = rel[1]
	else:
		nodes[rel[0]][rel[2]] += rel[1]

with open('./data/relationships_with_weights.json','w') as f:
	f.write(json.dumps(nodes, indent = 6))