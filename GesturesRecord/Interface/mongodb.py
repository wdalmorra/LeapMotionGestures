from pymongo import MongoClient

def save(data, db_name, col_name):
	oid = None

	try:
		client = MongoClient()
		db = client[db_name]
		collection = db[col_name]

		oid = collection.insert(data)

	except Exception, e:
		pass

	if(oid != None):
		return 'success ' + str(oid)
	else:
		return 'fail_db'
