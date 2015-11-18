import os, sys
src_dir = os.environ['LEAP_HOME']
lib_dir = 'lib/'
join_dir = os.path.join(src_dir, lib_dir)
sys.path.append(join_dir)
arch_dir = 'x64/' if sys.maxsize > 2**32 else 'x86/'
join_dir = os.path.join(join_dir, arch_dir)
sys.path.append(join_dir)

import threading
import capture
import Queue
import Leap

class SaveThread (threading.Thread):
	def __init__(self, threadID, name, confidence, db_name, col_name, queue):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.confidence = confidence
		self.db_name = db_name
		self.col_name = col_name
		self.queue = queue
		self.controller = Leap.Controller()
	def run(self):
		# print "Starting " + self.name
		# Get lock to synchronize threads
		# threadLock.acquire()
		success = capture.save_data(self.controller, self.name, self.confidence, self.db_name, self.col_name)
		self.queue.put(success)
		# Free lock to release next thread
		# threadLock.release()