from pymongo import MongoClient
from bson.objectid import ObjectId

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

def remove(oid, db_name, col_name):
	result = None

	try:
		client = MongoClient()
		db = client[db_name]
		col = db[col_name]

		result = col.remove({'_id': ObjectId(oid)})

	except Exception, e:
		pass

	if(result != None):
		return 'undo_success'
	else:
		return 'undo_fail'