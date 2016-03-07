import sys
from pymongo import MongoClient
from sklearn import svm
from sklearn.externals import joblib


clf = svm.SVC(kernel = 'linear', C = 1.0)

samples = []
classification = []

training_percent = 0.5

def connect_to_mongo(db_name,col_name):
	try:
		client = MongoClient()
		db = client[db_name]
		collection = db[col_name]
		return collection
	except Exception, e:
		pass

	return None

def learning(collection):

	n_elements = collection.count()

	gestures = collection.find()

	fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']

	for i in range(int(n_elements*training_percent)):
		tmp = []
		for finger in fingers:
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['direction'][j])
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['bone_2']['prev_joint'][j])
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['bone_2']['next_joint'][j])
		samples.append(tmp)
		classification.append(gestures[i]['gesture'])

	clf.fit(samples,classification)

	joblib.dump(clf, 'training1.pkl', compress=1)

def predict(collection):

	n_elements = collection.count()

	gestures = collection.find()

	fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']

	tests = []
	right_answers = []
	answers = []

	for i in range(int((n_elements*training_percent)),n_elements):
		tmp = []
		for finger in fingers:
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['direction'][j])
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['bone_2']['prev_joint'][j])
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['bone_2']['next_joint'][j])
		tests.append(tmp)
		right_answers.append(gestures[i]['gesture'])

	answers = clf.predict(tests)
	for i in range(len(answers)):
		print "Answer: " + str(answers[i]) + '    ' + "Should be: "	+ str(right_answers[i])

	acc = 0
	for i in range(len(answers)):
		if answers[i] == right_answers [i]:
			acc = acc + 1.0

	print "Percentage of hits: " + str(acc / len(answers))
	print len(answers)


def main(argv):

	collection = connect_to_mongo(argv[0],argv[1])

	learning(collection)

	predict(collection)

	pass

if __name__ == '__main__':
	main(sys.argv[1:])