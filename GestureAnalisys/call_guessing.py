import threading
import training

class Call_Guessing (threading.Thread):
	def __init__(self, clf):
		threading.Thread.__init__(self)
		self._stop = threading.Event()
		self.clf = clf

	def run(self):
		self.clf.guessing(self)