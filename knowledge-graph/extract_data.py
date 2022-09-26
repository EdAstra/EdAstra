import json
import os

'''

#####################################################
############### GETTING RELATIONSHIPS ###############
#####################################################

print('STEP 1: Parsing Scrapy data to get relationships.')
#Get the results of the web scraper
f = open('../web-scraper/data/wikipedia_academic_disciplines.json', 'r')

#Load the data from it's JSON format as a dictionary
data = json.loads(f.read())

###
#
# This gets relationships in the form
# ('science', 1, chemistry')
# 
# The second element is always one (because it represents one link)
# This first element is the parent node (the page that was being scraped)
# The third element is the child node (a link on the page being scraped)
#
###

#Extract the relationships from the data
with open('./data/relationships.json','w') as relationships: #writing to a new file
	relationships.write('[') #Start the list
	for element in data:
		for key, value in element.items():
			if len(value) > 2: 	#Skip the data from the initial URL, which has no parent node
				#This sorts the relationship alphanumerically
				#so relationship objects are deterministic ('apple', 1, 'banana')
				#is the same as ('banana',1,'apple')
				if value[2][0].lower() == value[2][2].lower():
					continue 	#Skip if this relationship connects a node to itself
				temp = [value[2][0].lower(), value[2][2].lower()]
				temp.sort()
				value[2][0] = temp[0]
				value[2][2] = temp[1]
				relationships.write(json.dumps(value[2])) #After sorting, add the relationship
				relationships.write(', \n')
	relationships.seek(relationships.tell() - 3, os.SEEK_SET) #Clean up and finish the list
	relationships.truncate()
	relationships.write(']')

print('STEP 1 COMPLETE')

#####################################################
################## GETTING WEIGHTS ##################
#####################################################

###
#
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
#
###

print('STEP 2: Calculating relationship weights.')

f = open('./data/relationships.json', 'r') #Get the list of relationships
relationships = json.load(f) #And load as a dict

nodes = {}

for rel in relationships:
	if rel[0] not in nodes: 				# If this node (the first node in the relationship) has not been seen
		nodes[rel[0]] = {rel[2]: rel[1]} 	#    Add the connected node and the initial weight (1)
	elif rel[2] not in nodes[rel[0]]: 		# If this connected node (the second node in the relationship) has not been seen 
		nodes[rel[0]][rel[2]] = rel[1] 		#    Add it to the dictionary which exists for the first node in the relationship
	else:									# If both nodes have already been seen
		nodes[rel[0]][rel[2]] += rel[1] 	#    increment the weight

with open('./data/relationships_with_weights.json','w') as f: # Write this data to a file
	f.write(json.dumps(nodes, indent = 6))

print('STEP 2 COMPLETE')

#####################################################
############ GETTING NODES AND NODEWORDS ############
#####################################################

###
#
# This gets a dictionary with nodes as keys
# and the tokens comprising the nodes as elements
# in the array that is the associated value:
#
# {
#	"scientific_method": [
#            "scientific",
#            "method"
#      ]
# }
#
# Getting this list of node words/tokens helps
# us when getting the node vectors later on.
#
###

print('STEP 3: Getting a list of nodes and tokenizing.')

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

print('STEP 3 COMPLETE')

#####################################################
############### GETTING NODE VECTORS ################
#####################################################

###
#
# This gets fastText vectors for each node.
# These vectors will be used in plotting the nodes
# in a 3D knowledge graph, as well as providing
# an understanding of their meaning.
# 
# Currently, the node vectors are retrieved and then
# reduced to three dimensions for plotting purposes. 
# TODO: It may be preferable to keep another copy of 
# node vectors in 300 dimensions to have more accurate
# semantic understanding.
#
###

print('STEP 4: Getting node vectors.')

import json
import fasttext
import fasttext.util

import numpy as np

def is_number(s):
    #https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
    return s.replace('.','',1).isdigit()

f = open('./data/nodes.json', 'r') # Get relationships with weights data (we just need the nodes)
nodes = json.load(f)

print('Loading fastText model')
wiki_model = fasttext.load_model('./data/wiki.en.bin')
print('Finished loading fastText model')
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
with open('./data/node_vectors.json','w') as nv: # Write the data to a file
    nv.write(json.dumps(node_vectors, indent = 6))
print('Finished writing vectors file')

print('STEP 4 COMPLETE')



#####################################################
################# GETTING NODE URLS #################
#####################################################


print('STEP 5: Parsing Scrapy data to get node URLs')
#Get the results of the web scraper
f = open('../web-scraper/data/wikipedia_academic_disciplines.json', 'r')

#Load the data from it's JSON format as a dictionary
data = json.loads(f.read())

###
#
# This gets relationships in the form
# ('science', 1, chemistry')
# 
# The second element is always one (because it represents one link)
# This first element is the parent node (the page that was being scraped)
# The third element is the child node (a link on the page being scraped)
#
###

#Extract the node urls from the data
with open('./data/node_urls.json','w') as node_urls: #writing to a new file
    node_urls = {}
    for element in data:
        for key, value in element.items():
            node_ = value[0].lower()
            url_ = value[1]
            node_urls[node_] = url_

with open('./data/node_urls.json','w') as nv: # Write the data to a file
    nv.write(json.dumps(node_urls, indent = 6))

print('STEP 5 COMPLETE')

#####################################################
############ CONVERTING TO CSV FOR NEO4J ############
#####################################################

###
#
# This translates the data into csv according
# to the format expected by Neo4j.
# 
# This generates two csv files:
#    	(1) A list of nodes with the properties:
#        	- koId (the Knowledge Object ID given in this script)
#		 	- name (the full name of the node)
#        	- x, y, & z (the node vector)
#    	(2) A list of connections between nodes with the properties:
#			- weight (the weight of the edge)
#
###
'''

print('STEP 6: Converting data to csv for Neo4j database.')

import csv

def getNodeName(node): # This is mostly for aesthetics.
    return node.replace('_',' ')
    
# Get relationships with weights data
# This contains nodes, the nodes they are connected to, 
# and the weights of the connections.
f = open('./data/relationships_with_weights.json', 'r') 
nodes = json.load(f)

# Get node vectors
f = open('./data/node_vectors.json', 'r') # Get relationships with weights data (we just need the nodes)
node_vectors = json.load(f)

# Get node urls
f = open('./data/node_urls.json', 'r') # Get relationships with weights data (we just need the nodes)
node_urls = json.load(f)

# Create the csv of knowledge objects to import into Neo4J graph database
with open('data/neo4j_knowledge_objects_with_vectors.csv', 'w', newline='') as csvfile:
    fieldnames = ['koId', 'name', 'x', 'y', 'z', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    node_list = []
    relationships_list = []
    koId_dict = {}
    koId = 0

    for node, relationships in nodes.items():
        if koId > 49000: # 50,000 is the limit for Aura free version
            break
        if node not in node_list: # Add the node if it's not already in the list
            koId += 1
            node_list.append(node)
            node_name = getNodeName(node)
            koId_dict[node] = koId
            x,y,z = node_vectors[node]
            node_url = node_urls[node]
            writer.writerow({'koId':koId, 'name':node_name, 'x':x, 'y':y, 'z':z, 'url':node_url}) # Write this node to the csv file
        for rel_node, weight in relationships.items(): # Look through the list of connected nodes
            if koId > 49000:
                break
            if weight < 2: # Skip the weakest connections (where weight == 1)
                continue
            if rel_node not in node_list: # Add the node if it's not already in the list
                rel_node_name = getNodeName(rel_node)
                koId += 1
                node_list.append(rel_node)
                koId_dict[rel_node] = koId
                x,y,z = node_vectors[rel_node]
                node_url = node_urls[rel_node]
                this_relationship = [koId_dict[node],koId,weight]
                relationships_list.append(this_relationship) # Add this relationship to the list
                writer.writerow({'koId': koId, 'name': rel_node_name, 'x':x, 'y':y, 'z':z, 'url':node_url}) # Write this node to the csv file
            elif rel_node != node: # This conditional is error handling. rel_node should never be the same as node.
                this_relationship = [koId_dict[rel_node],koId_dict[node],weight]
                if this_relationship not in relationships_list:
                    # This relationship is new only if this node is connected to a node that is 
                    # connected to a node that was previously visited in the outer loop
                    # Example: (a)->(b), (a)->(c), (b)->(c)
                    # this would be the (b)->(c) relationship
                    relationships_list.append(this_relationship)

with open('data/neo4j_connections.csv', 'w', newline='') as csvfile: # Write the relationships to the csv file
    fieldnames = ['koId_a', 'koId_b', 'weight']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for relationhip in relationships_list:
        #koId_a and koId_b are arbitrary column names, the relationships are bidirectional
        writer.writerow({'koId_a': relationhip[0], 'koId_b': relationhip[1], 'weight': relationhip[2]})

print('STEP 6 COMPLETE')