import json

f = open('./data/relationships.json', 'r') #Get the list of relationships
relationships = json.load(f) #And load as a dict

nodes = {}

###
# This creates a dictionary with the keys being a node
# and the value being a dictionary of nodes this node is connected to
# and the weights of the connections.
# See example below:
# {
# 	'Node A': 
# 		{
# 			'Node B': 2, 
# 			'Node C': 3, 
# 			'Node D': 1
# 		}
# }

for rel in relationships:
	if rel[0] not in nodes: 				# If this node (the first node in the relationship) has not been seen
		nodes[rel[0]] = {rel[2]: rel[1]} 	#    Add the connected node and the initial weight (1)
	elif rel[2] not in nodes[rel[0]]: 		# If this connected node (the second node in the relationship) has not been seen 
		nodes[rel[0]][rel[2]] = rel[1] 		#    Add it to the dictionary which exists for the first node in the relationship
	else:									# If both nodes have already been seen
		nodes[rel[0]][rel[2]] += rel[1] 	#    increment the weight

with open('./data/relationships_with_weights.json','w') as f: # Write this data to a file
	f.write(json.dumps(nodes, indent = 6))