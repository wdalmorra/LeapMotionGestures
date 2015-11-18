import threading
import capture
import Queue

class SaveThread (threading.Thread):
	def __init__(self, threadID, name, confidence, db_name, col_name, queue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.confidence = confidence
		self.db_name = db_name
		self.col_name = col_name
		self.queue = queue
	def run(self):
		# print "Starting " + self.name
		# Get lock to synchronize threads
		# threadLock.acquire()
		success = capture.save_data(self.name, self.confidence, self.db_name, self.col_name)
		self.queue.put(success)
		# Free lock to release next thread
		# threadLock.release()