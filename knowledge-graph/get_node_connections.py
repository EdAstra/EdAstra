import json

# Open the file containing nodes and their connected nodes
# with the weight of the connection.
# What is being created here is very similar to this original file.
# The difference being, in the original file, node A connected to node B
# will only show up in node A's list of connections.
# In the new file created here, the connection will show up in both lists.
f = open('./data/relationships_academic_disciplines_with_weights.json', 'r') #Get the list of relationships
relationships = json.load(f) #And load as a dict

nodes_with_connected_nodes = {}

for node, connected_nodes in relationships.items():
	if node not in nodes_with_connected_nodes: # Initialize the dict
		if node=="": # Edge case handling
			continue
		nodes_with_connected_nodes[node] = {}
	for cn, weight in connected_nodes.items():
		if cn=="" or cn==node: #Edge case handling
			continue
		if cn not in nodes_with_connected_nodes: # Initialize the dict
			nodes_with_connected_nodes[cn] = {node: weight}
		else:
			nodes_with_connected_nodes[cn][node] = weight # Add this connection
		nodes_with_connected_nodes[node][cn] = weight # Add this connection


with open('./data/nodes_and_connected_nodes_academic_disciplines.json','w') as f: # Write this data to a file
	f.write(json.dumps(nodes_with_connected_nodes, indent = 6))