import json
import random

f = open('./data/nodes_academic_disciplines.json', 'r') #Get the list of relationships
nodes = json.load(f) #And load as a dict

count = 0
modifier = 20000


for node, tokens in nodes.items():
	count += 1
	if random.randint(1,20000) == 432:
		print(node.replace("_"," "))
	

print(count,"nodes in dataset.")