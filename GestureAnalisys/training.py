import sys, os
from pymongo import MongoClient
from sklearn import svm
# from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib

src_dir = os.environ['LEAP_HOME']
lib_dir = 'lib/'
join_dir = os.path.join(src_dir, lib_dir)
sys.path.append(join_dir)
arch_dir = 'x64/' if sys.maxsize > 2**32 else 'x86/'
join_dir = os.path.join(join_dir, arch_dir)
sys.path.append(join_dir)

import Leap

class Classifier(object):
	
	# clf = SGDClassifier()
	clf = svm.SVC( kernel = 'linear', C = 1.0 )

	samples = []
	classification = []
	collection = None
	training_percent = 0.6
	db_name = ""
	col_name = ""
	filename = "training1.pkl"
	
	def __init__(self, db_name, col_name):
		self.db_name = db_name
		self.col_name = col_name


	def __connect_to_mongo(self):
		try:
			client = MongoClient()
			db = client[self.db_name]
			self.collection = db[self.col_name]
		except Exception, e:
			pass

	def training(self):

		self.__connect_to_mongo()

		n_elements = self.collection.count()

		gestures = self.collection.find()

		fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']

		for i in range(int(n_elements*self.training_percent)):
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
			# self.clf.partial_fit(tmp, classification, classes=['0','1','2','3','4','5','6','7','8','9'])

			self.samples.append(tmp)
			self.classification.append(gestures[i]['gesture'])

		self.clf.fit(self.samples,self.classification)

		joblib.dump(self.clf, self.filename, compress=1)

		print 'finished training'

	def guessing(self):

		controller = Leap.Controller()
		last_gesture = ""
		while True:
			frame = controller.frame()
			if (frame.id % 100) == 0:
				if not frame.hands.is_empty:
					
					hand_palm_position = frame.hands[0].palm_position

					tmp = []

					for i in range(5):
						for j in range(3):
							tmp.append(frame.hands[0].fingers[i].direction[j])

						vec_translated = frame.hands[0].fingers[i].bone(2).prev_joint - hand_palm_position
						for j in range(3):
							tmp.append(vec_translated[j])

						vec_translated = frame.hands[0].fingers[i].bone(2).next_joint - hand_palm_position
						for j in range(3):
							tmp.append(vec_translated[j])
					
					answer = self.clf.predict(tmp)
					if answer[0] != last_gesture:
						print answer[0]
						last_gesture = answer[0]

				else:
					last_gesture = ""
						

def main(argv):


	if len(argv) >= 3:
		c = Classifier(argv[0],argv[1])
		c.training()
		c.guessing()
	else:
		print '\nusage: python2 training.py <db_name> <collection_name> <file_name>\n'


if __name__ == '__main__':
	main(sys.argv[1:])