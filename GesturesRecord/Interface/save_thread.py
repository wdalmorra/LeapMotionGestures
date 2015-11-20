import threading
import capture

class SaveThread (threading.Thread):
	def __init__(self, threadID, name, display):
		threading.Thread.__init__(self)
		self._stop = threading.Event()
		self.threadID = threadID
		self.name = name
		self.display = display
		
	def run(self):
		success = capture.save_data(self)
		self.display.queue.put(success)
