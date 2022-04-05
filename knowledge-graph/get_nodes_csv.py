import json
import csv

f = open('./data/node_vectors.json', 'r') # Get relationships with weights data (we just need the nodes)
nodes = json.load(f)

with open('data/nodes.csv', 'w', newline='') as csvfile:
    fieldnames = ['node', 'x', 'y', 'z']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for node_name, vector in nodes.items():
	    writer.writerow({'node': node_name, 'x': vector[0], 'y': vector[1], 'z': vector[2]})