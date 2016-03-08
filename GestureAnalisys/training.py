import sys
from pymongo import MongoClient
from sklearn import svm
# from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib


# clf = SGDClassifier()
clf = svm.SVC( kernel = 'linear', C = 1.0 )

samples = []
classification = []

training_percent = 0.6

def connect_to_mongo(db_name,col_name):
	try:
		client = MongoClient()
		db = client[db_name]
		collection = db[col_name]
		return collection
	except Exception, e:
		pass

	return None

def learning(collection, filename):

	n_elements = collection.count()

	gestures = collection.find()

	fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']

	for i in range(int(n_elements*training_percent)):
		tmp = []
		# classification = []
		for finger in fingers:
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['direction'][j])
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['bone_2']['prev_joint'][j])
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['bone_2']['next_joint'][j])

		# classification.append(gestures[i]['gesture'])
		# clf.partial_fit(tmp, classification, classes=['0','1','2','3','4','5','6','7','8','9'])

		samples.append(tmp)
		classification.append(gestures[i]['gesture'])

	clf.fit(samples,classification)

	joblib.dump(clf, filename, compress=1)

def main(argv):

	if len(argv) > 3:
		collection = connect_to_mongo(argv[0],argv[1])

		learning(collection, argv[2])

	else:
		print '\nusage: python2 training.py <db_name> <collection_name> <file_name>\n'


if __name__ == '__main__':
	main(sys.argv[1:])