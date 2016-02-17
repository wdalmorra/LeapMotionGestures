import json
import sys
import pprint

columns = []
numbers = []

def name_columns_rec(name, data,index):

	if type(data) is list:
		columns.append(name+'.'+'X')
		numbers[index].append(data[0])
		columns.append(name+'.'+'Y')
		numbers[index].append(data[1])
		columns.append(name+'.'+'Z')
		numbers[index].append(data[2])
	elif type(data) is not dict:
		columns.append(name)
		numbers[index].append(data)
	else:
		for n in data:
			name_columns_rec(name+'.'+n, data[n],index)

def name_columns(file):
	data = []
	with open(file) as json_file:
		for line in json_file:
			data.append(json.loads(line))
	# print len(data)

	for i in range (len(data)):
		for l in data[i]:
			numbers.append([])
			name_columns_rec(l,data[i][l],i)



def main(argv):
	
	name_columns(argv)

	for i in range(80):
		for j in range(len(numbers[i])):
			print columns[j] + ": " + str(numbers[i][j])
			# print numbers[i][j]

if __name__ == '__main__':
	main(sys.argv[1])