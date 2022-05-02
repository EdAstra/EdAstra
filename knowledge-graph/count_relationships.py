import json

f = open('./data/relationships_academic_disciplines_with_weights.json', 'r') #Get the list of relationships
relationships = json.load(f) #And load as a dict

count = 0
tot_weight = 0
max_weight = 0
max_node = ""
max_rel = ""
weights = []

num_rels = []
node_count = 0
for node, rels in relationships.items():
	node_count += 1
	this_num_rel = 0
	for rel, weight in rels.items():
		this_num_rel += 1
		weights.append(weight)
		count += 1
		tot_weight += weight
		if weight > max_weight:
			max_weight = weight
			max_node = node
			max_rel = rel
	num_rels.append(this_num_rel)

num_rels.sort()
print("Median # of relationships is",num_rels[216339])

num_rels_dict = {}
mid_num_rels_count = 0
large_num_rels_count = 0
for num in num_rels:
	if num not in num_rels_dict:
		num_rels_dict[num] = 1
	else:
		num_rels_dict[num] += 1
	if num > 30:
		large_num_rels_count += 1
	elif num > 10:
		mid_num_rels_count += 1

print(num_rels_dict)
print(large_num_rels_count,"nodes with > 30 relationships.")
print(mid_num_rels_count,"nodes where 10 < n <= 30 relationships.")

avg_weight = tot_weight/count

print("Average weight of",avg_weight,"in",count,"relationships.")
print("Maximum weight is",max_weight,"between",max_node,"and",max_rel)

weights.sort()
print("Median weight is",weights[2253122])

weight_dict = {}
large_weight_count = 0
for weight in weights:
	if weight not in weight_dict:
		weight_dict[weight] = 1
	else:
		weight_dict[weight] += 1
	if weight > 10:
		large_weight_count += 1

print(weight_dict)
print(large_weight_count,"relationships with weight > 10.")