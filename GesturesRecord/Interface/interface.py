import sys, os
# src_dir = os.environ['LEAP_HOME']
# lib_dir = 'lib/'
# join_dir = os.path.join(src_dir, lib_dir)
# sys.path.append(join_dir)
# arch_dir = 'x64/' if sys.maxsize > 2**32 else 'x86/'
# join_dir = os.path.join(join_dir, arch_dir)
# sys.path.append(join_dir)

from Tkinter import *
import ttk
import Queue
import save_thread as st
# import capture
# import Leap

class Example(Frame):

	# things needed to be changed in specific methods, that's why they are attributes
	confidence_label = None			# Label updated everytime a frame is captured
	content = None					# Main frame
	sett = None						# Settings window - unique
	controller = None				# Leap Motion controller - unique as well
	name_entry = None				# Entry for a new name, used in the save method
	
	counter = 0						# Allows only one settings window at the time
	
	# Attributes updated by settings window
	confidence = None				# Minimum confidence
	n_frames = None					# # of frames/gesture
	db_name = None					# Database name
	collection_name = None			# Collection name
	queue = None

	def __init__(self, master):
		Frame.__init__(self,master)

		self.parent = master
		self.parent.protocol('WM_DELETE_WINDOW', self.close_window)
		self.parent.title("Gestures Recorder")
		
		self.init_ui()

		# self.controller = Leap.Controller()

		self.set_minimum_confidence(0.6)
		self.set_n_frames(1)
		self.set_db_name("test")
		self.set_collection_name("test1")
		self.queue = Queue.Queue()
	
	# Centers and sizes the window according to the size of the screen
	def center_window(self):

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		w = sw / 4;
		h = sh / 4;

		x = (sw - w)/2
		y = (sh - h)/2

		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

	# Create all the widgets and layouts
	def init_ui(self):
		self.center_window()

		text = StringVar()
		text.set('Confidence = --%')
		self.content = ttk.Frame(self.parent, padding=(3,3,3,3))

		settings = ttk.Button(self.content, text="Settings", command=self.open_settings)
		save = ttk.Button(self.content, text="Save", command=self.save_gesture)
		self.confidence_label = ttk.Label(self.content, text='Confidence = --%')

		name_label = ttk.Label(self.content, text='Name: ')

		self.name_entry = ttk.Entry(self.content)

		self.name_entry.insert(0,"Dumb")

		self.content.grid(column=0, row=0, sticky=(N, S, E, W))

		self.confidence_label.grid(column=1, row=0, sticky=(N, E),pady=15)
		settings.grid(column=4,row=0, sticky=(N, E), pady=15, padx=15)
		save.grid(column=1, row=3, sticky=(N, E),pady=25)
		name_label.grid(column=3, row=3, sticky=(N,E),pady=25, padx=5)
		self.name_entry.grid(column=4, row=3, sticky=(N,W),pady=25, padx=15)

		self.parent.columnconfigure(0, weight=1)
		self.parent.rowconfigure(0, weight=1)
		self.content.columnconfigure(0, weight=3)
		self.content.columnconfigure(1, weight=3)
		self.content.columnconfigure(2, weight=3)
		self.content.columnconfigure(3, weight=1)
		self.content.columnconfigure(4, weight=1)
		self.content.rowconfigure(1, weight=1)

	# Updates the confidence label when a new frame is captured
	def update_confidence_label(self, conf):
		self.confidence_label['text'] = 'Confidence = '+ str(conf) + '%'
		## Change the main frame color
		# s =  ttk.Style()
		# s.configure('My.TFrame', background='blue')
		# self.content.config(style='My.TFrame')

	# Responsable for closing the window
	def close_window(self):
		self.parent.destroy()

	# Creates a new window of just set focus to a window already open
	def open_settings(self):
		if self.counter == 0:
			self.sett = Tk()
			new_window = SettingsWindow(self.sett, self)
			self.counter = self.counter + 1
		else:
			self.sett.focus_force()
			self.sett.lift()

	# Saves the gesture capture in the database
	def save_gesture(self):
		name = self.name_entry.get()
		# n_frames
		# data = capture.get_data(self.controller, name, self.confidence)

		# success = capture.save_on_mongo(data, self.db_name, self.collection_name)
		t = st.(1, name, self.confidence, self.db_name, self.collection_name, self.queue)

		t.start()
		self.master.after(100, self.process_queue)
		# return success

	## Sequence of methods that save the settings from settings window
	## BEGIN
	def set_minimum_confidence(self, conf):
		self.confidence = conf;

	def set_n_frames(self, n_frames):
		self.n_frames = n_frames;

	def set_db_name(self,db_name):
		self.db_name = db_name

	def set_collection_name(self, c_name):
		self.collection_name = c_name
	## END

	def process_queue(self):
		try:
			msg = self.queue.get(0)
			# Do something
		except Queue.Empty:
			self.master.after(1000, self.process_queue)


class SettingsWindow(Frame):

	confidence_entry = None
	n_frames_entry = None
	collection_name_entry = None
	dbname_entry = None

	def __init__(self, master,father):
		Frame.__init__(self,master)
		self.parent = master
		self.father = father
		self.parent.protocol('WM_DELETE_WINDOW', self.close_window)
		self.parent.title("Settings")
		self.init_ui()

	def init_ui(self):

		self.content = ttk.Frame(self.parent, padding=(3,3,3,3))

		confidence_label = ttk.Label(self.content, text='Minimum Confidence: ')
		self.confidence_entry = ttk.Entry(self.content)

		dbname_label = ttk.Label(self.content, text='Database Name: ')
		self.dbname_entry = ttk.Entry(self.content)

		# Comment what a collection is!
		collection_name_label = ttk.Label(self.content, text='Collection Name: ')
		self.collection_name_entry = ttk.Entry(self.content)

		n_frames_label = ttk.Label(self.content, text='# of Frames/Gesture: ')
		self.n_frames_entry = ttk.Entry(self.content)

		save_button = ttk.Button(self.content, text="Save", command=self.save_settings)
		cancel_button = ttk.Button(self.content, text="Cancel", command=self.cancel)

		self.content.grid(column=0, row=0, sticky=(N, S, E, W))
		confidence_label.grid(column=0, row=0, pady=10, padx=15)
		self.confidence_entry.grid(column=1, row=0, pady=10, padx=15)
		n_frames_label.grid(column=0, row=1, pady=10, padx=15)
		self.n_frames_entry.grid(column=1, row=1, pady=10, padx=15)
		dbname_label.grid(column=2, row=0, pady=10,padx=15)
		self.dbname_entry.grid(column=3, row=0, pady=10,padx=15)
		collection_name_label.grid(column=2, row=1, pady=10,padx=15)
		self.collection_name_entry.grid(column=3, row=1, pady=10,padx=15)
		save_button.grid(column=1, row=2, pady=10, padx=15)
		cancel_button.grid(column=2, row=2, pady=10, padx=15)

		self.parent.columnconfigure(0, weight=1)
		self.parent.rowconfigure(0, weight=1)
		self.content.columnconfigure(0, weight=3)
		self.content.columnconfigure(1, weight=3)
		self.content.columnconfigure(2, weight=3)
		self.content.columnconfigure(3, weight=3)
		self.content.rowconfigure(1, weight=1)
		self.content.rowconfigure(2, weight=1)

		self.set_default_conf()
		self.set_default_fram()
		self.set_default_db_name()
		self.set_default_coll_name()

		self.center_window()

	def center_window(self):

		self.parent.update()

		w = self.parent.winfo_width()
		h = self.parent.winfo_height()

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw - w)/2
		y = (sh - h)/2

		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def save_settings(self):
		self.father.set_n_frames(self.n_frames_entry.get())
		self.father.set_minimum_confidence(self.confidence_entry.get())
		self.father.set_db_name(self.dbname_entry.get())
		self.father.set_collection_name(self.collection_name_entry.get())
		self.close_window()

	def cancel(self):
		self.close_window()

	def close_window(self):
		self.father.counter = self.father.counter - 1
		self.parent.destroy()

	def set_default_conf(self):
		self.confidence_entry.insert(0,self.father.confidence)

	def set_default_fram(self):
		self.n_frames_entry.insert(0,self.father.n_frames)
	
	def set_default_db_name(self):
		self.dbname_entry.insert(0,self.father.db_name)
	
	def set_default_coll_name(self):
		self.collection_name_entry.insert(0,self.father.collection_name)

def main():

	root = Tk()
	app = Example(root)
	root.mainloop()


if __name__ == '__main__':
	main()
