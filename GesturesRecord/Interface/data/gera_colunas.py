import json
import sys
import pprint

columns = []

def name_columns_rec(name, data):

	if type(data) is list:
		columns.append(name+'.'+'X')
		columns.append(name+'.'+'Y')
		columns.append(name+'.'+'Z')
	elif type(data) is not dict:
		columns.append(name)
	else:
		for n in data:
			name_columns_rec(name+'.'+n, data[n])

def name_columns(file):
	data = []
	with open(file) as json_file:
		for line in json_file:
			data.append(json.loads(line))

	for l in data[0]:
		name_columns_rec(l,data[0][l])



def main(argv):
	
	name_columns(argv)

	for i in columns:
		print i

if __name__ == '__main__':
	main(sys.argv[1])