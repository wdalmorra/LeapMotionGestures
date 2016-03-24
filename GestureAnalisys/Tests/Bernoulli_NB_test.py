from pymongo import MongoClient
import sys
from sklearn import naive_bayes
from sklearn import preprocessing
from sklearn.cross_validation import cross_val_score, KFold, train_test_split
from sklearn import metrics
from scipy.stats import sem
import numpy as np
from random import randint

clf =  naive_bayes.BernoulliNB()

X_train = []
y_train = []
X_test = []
y_test = []

magic_random_number = randint(0,255)

# training_percent = 0.6

def connect_to_mongo(db_name,col_name):
	try:
		client = MongoClient()
		db = client[db_name]
		collection = db[col_name]
		return collection
	except Exception, e:
		pass

	return None

def evaluate_cross_validation(clf, X, y, K):
	# Create a k-fold cross validation iterator
	cv = KFold(len(y), K, shuffle=True, random_state=0)

	# by default the score used is the one returned by score method of the estimator (accuracy)
	scores = cross_val_score(clf, X, y, cv=cv)
	print scores
	print ("Mean score: {0:.3f} (+/-{1:.3f})").format(np.mean(scores), sem(scores))

def generate_data_target(collection):

	global X_train, X_test, y_train, y_test

	n_elements = collection.count()

	gestures = collection.find()

	fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
	
	samples = []
	classification = []

	for i in range(n_elements):
		tmp = []
		for finger in fingers:
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['direction'][j])
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['bone_2']['prev_joint'][j])
			for j in range(3):
				tmp.append(gestures[i]['right_hand'][finger]['bone_2']['next_joint'][j])
		tmp.append(gestures[i]['right_hand']['sphere_radius'])
		# tmp.append(gestures[i]['right_hand']['grab_strength'])
		# for j in xrange(3):
		# 	tmp.append(gestures[i]['right_hand']['palm_normal'][j])
		samples.append(tmp)
		classification.append(gestures[i]['gesture'])

	normalized_samples = preprocessing.normalize(samples, norm='l2')
	scaled_samples = preprocessing.scale(normalized_samples)

	X_train, X_test, y_train, y_test = train_test_split(scaled_samples, classification, test_size=0.40, random_state=magic_random_number)


def learning():

	evaluate_cross_validation(clf, X_train, y_train, 5)

	clf.fit(X_train, y_train)

	print "Accuracy on training set: "
	print clf.score(X_train, y_train)

def predict():

	print "Accuracy on testing set: "
	print clf.score(X_test, y_test)

	y_pred = clf.predict(X_test)

	print "Classification Report:"
	print metrics.classification_report(y_test, y_pred)
	print "Confusion Matrix:"
	print metrics.confusion_matrix(y_test, y_pred)

def main(argv):

	collection = connect_to_mongo(argv[0],argv[1])

	generate_data_target(collection)

	learning()

	predict()

if __name__ == '__main__':
	main(sys.argv[1:])