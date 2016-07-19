from pymongo import MongoClient
import sys

def do_stuff(aux, k, ignore):
	if type(aux[k]) is dict:
		for key in sorted(aux[k].keys()):
			if key not in ignore:
				aux[k][key] = do_stuff(aux[k], key, ignore)

	elif type(aux[k]) is list:
		if k == 'direction' or k == 'palm_normal':
			for i in range(3):
				aux[k][i] = round(aux[k][i], 1)

		else:
			for i in range(3):
				aux[k][i] = (int(aux[k][i]) / 10) * 10


	else:
		if k == 'grab_strength':
			aux[k] = round(aux[k], 1)
		else:
			aux[k] = (int(aux[k]) / 10) * 10

	return aux[k]


def main(argv):
	try:
		client = MongoClient()
		db = client['project']
		corrected = db['corrected']
		discrete = db['discrete']

		ignore = ['_id', 'confidence', 'utc', 'name', 'gesture']

		cursor = corrected.find()

		for gesture in cursor:
			aux = gesture

			if type(aux) is dict:
				for key in sorted(aux.keys()):
					if key not in ignore:
						aux[key] = do_stuff(aux, key, ignore)
				oid = discrete.insert(aux)

	except Exception, e:
		print e

if __name__ == '__main__':
	main(sys.argv[1:])