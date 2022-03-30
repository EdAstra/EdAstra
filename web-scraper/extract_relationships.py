import json
import os

f = open('./scrape_wikipedia/scrape_wikipedia/wikipedia.json', 'r')

data = json.loads(f.read())

with open('relationships.json','w') as relationships:
	relationships.write('[')
	for element in data:
		for key, value in element.items():
			if len(value) > 2:
				temp = [value[2][0].lower(), value[2][2].lower()]
				temp.sort()
				value[2][0] = temp[0]
				value[2][2] = temp[1]
				relationships.write(json.dumps(value[2]))
				relationships.write(', \n')
	relationships.seek(relationships.tell() - 3, os.SEEK_SET)
	relationships.truncate()
	relationships.write(']')