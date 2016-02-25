from pymongo import MongoClient
import sys


clf = svm.SVC(kernel = 'linear', C = 1.0)

samples = []
classification = []

training_percent = 0.5
test_percent = 0.5

collection = None

def connect_to_mongo(db_name,col_name):
	try:
		client = MongoClient()
		db = client[db_name]
		collection = db[col_name]
	except Exception, e:
		pass

def learning():

	n_elements = collection.count()

	gestures = collection.find()

	fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']

	for i in range(n_elements*training_percent):
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

def predict():

	n_elements = collection.count()

	gestures = collection.find()

	fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']

	tests = []
	right_answers = []
	answers = []

	for i in range(((n_elements*training_percent)+1),n_elements):
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
	print "Answers:   " + answers
	print "Should be: "	+ right_answers

	acc = 0
	for i in range(len(answers)):
		if answers[i] == right_answers [i]:
			acc = acc + 1

	print "Percentage of hits: " + str(acc / len(answers))



def main(argv):

	connect_to_mongo(argv[0],argv[1])

	learning()

	predict()

	pass

if __name__ == '__main__':
	main(sys.argv[1:])