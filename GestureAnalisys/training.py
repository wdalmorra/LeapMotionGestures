import sys, os, json
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
	clf = svm.SVC( kernel = 'linear', C = 1.0, probability = True )

	samples = []
	classification = []
	collection = None
	gui = None
	db_name = "project"
	col_name = "gestures"
	database_file = "gestures90.json"
	trained_file = "training1.pkl"
	
	def __init__(self):
		pass

	def training(self):

		try:
			# If file exists then there is a model already trained
			self.clf = joblib.load(self.trained_file)
		except IOError, e:
			# Otherwise, train it!
		
			fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
			data = []
			with open(self.database_file) as json_file:
				for line in json_file:
					data.append(json.loads(line))

			for d in data:
				tmp = []
				# classification = []
				for finger in fingers:
					for j in range(3):
						tmp.append(d['right_hand'][finger]['direction'][j])
					for j in range(3):
						tmp.append(d['right_hand'][finger]['bone_2']['prev_joint'][j])
					for j in range(3):
						tmp.append(d['right_hand'][finger]['bone_2']['next_joint'][j])
				tmp.append(d['right_hand']['sphere_radius'])
				# classification.append(gestures[i]['gesture'])
				# self.clf.partial_fit(tmp, classification, classes=['0','1','2','3','4','5','6','7','8','9'])

				self.samples.append(tmp)
				self.classification.append(d['gesture'])

			self.clf.fit(self.samples,self.classification)

			joblib.dump(self.clf, self.trained_file, compress=1)

		print 'Finished training'

	def guessing(self,thread):

		controller = Leap.Controller()
		last_gesture = ""
		while True:
			if(thread._stop.is_set()):
				return 'exit'
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
						if self.clf.predict_proba(tmp)[0][int(answer[0])] > 0.5:
							self.gui.update_gesture_label(answer[0])
							last_gesture = answer[0]

				else:
					last_gesture = ""

	def set_interface(self, gui):
		self.gui = gui
