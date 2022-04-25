import json
import csv

def getNodeName(node): # This is mostly for aesthetics.
    name = node.replace('_',' ')
    return name

# Get relationships with weights data
# This contains nodes, the nodes they are connected to, 
# and the weights of the connections.
f = open('./data/relationships_academic_disciplines_with_weights.json', 'r') 
nodes = json.load(f)

# Create the csv of knowledge objects to import into Neo4J graph database
with open('data/neo4j_knowledge_objects.csv', 'w', newline='') as csvfile:
    fieldnames = ['koId', 'name']
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
            writer.writerow({'koId': koId, 'name': node_name}) # Write this node to the csv file
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
                this_relationship = [koId_dict[node],koId,weight]
                relationships_list.append(this_relationship) # Add this relationship to the list
                writer.writerow({'koId': koId, 'name': rel_node_name}) # Write this node to the csv file
            elif rel_node != node:
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