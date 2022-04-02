import json
import os

#Get the results of the web scraper
f = open('../web-scraper/data/wikipedia.json', 'r')

#Load the data from it's JSON format as a dictionary
data = json.loads(f.read())

######### TODO: Create logic to not add relationships if connected nodes
#########		are the same node. e.g. ('apple', 1, 'apple')

with open('./data/relationships.json','w') as relationships: #writing to a new file
	relationships.write('[') #Start the list
	for element in data:
		for key, value in element.items():
			if len(value) > 2: 	#This sorts the relationship alphanumerically
								#so relationship objects are deterministic ('apple', 1, 'banana')
								#is the same as ('banana',1,'apple')
				temp = [value[2][0].lower(), value[2][2].lower()]
				temp.sort()
				value[2][0] = temp[0]
				value[2][2] = temp[1]
				relationships.write(json.dumps(value[2])) #After sorting, add the relationship
				relationships.write(', \n')
	relationships.seek(relationships.tell() - 3, os.SEEK_SET) #Clean up and finish the list
	relationships.truncate()
	relationships.write(']')