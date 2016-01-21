import sys, os
src_dir = os.environ['LEAP_HOME']
lib_dir = 'lib/'
join_dir = os.path.join(src_dir, lib_dir)
sys.path.append(join_dir)
arch_dir = 'x64/' if sys.maxsize > 2**32 else 'x86/'
join_dir = os.path.join(join_dir, arch_dir)
sys.path.append(join_dir)

from Tkinter import *
# import tk
import ttk
import Queue
import save_thread as st
import capture
import Leap

class Example(Frame):

	# things needed to be changed in specific methods, that's why they are attributes
	confidence_label = None			# Label updated everytime a frame is captured
	message_label = None			# Label used to show messages about the stage of gesture saving
	content = None					# Main frame
	sett = None						# Settings window - unique
	name_entry = None				# Entry for a new name, used in the save method
	gesture_entry = None			# Entry for a new gesture, used in the save method

	counter = 0						# Allows only one settings window at the time

	queue = None					# Thread result
	active_thread = None			# Holds the active thread (if exists)
	controller = None				# Leap Motion controller - unique as well
	message_dict = {}				# Array of possible messages to be shown

	# Attributes updated by settings window
	confidence = None				# Minimum confidence
	n_frames = None					# # of frames/gesture
	db_name = None					# Database name
	collection_name = None			# Collection name

	# Attributes to UNDO
	last_oid = None
	last_db_name = None
	last_col_name = None


	def __init__(self, master):
		Frame.__init__(self,master)

		self.parent = master
		self.parent.protocol('WM_DELETE_WINDOW', self.close_window)
		self.parent.title("Gesture Recorder")
		

		self.init_dict()

		self.init_ui()

		self.set_minimum_confidence(0.75)
		self.set_n_frames(1)
		self.set_db_name("test")
		self.set_collection_name("test1")
		self.queue = Queue.Queue()
		self.active_thread = None
		self.controller = Leap.Controller()
		self.controller.set_policy(Leap.Controller.POLICY_IMAGES)

		self.last_oid = None
		self.last_db_name = None
		self.last_col_name = None
	
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
		self.undo_b = ttk.Button(self.content, text="Undo", command=self.undo, state=DISABLED)
		save = ttk.Button(self.content, text="Save", command=self.save_gesture)
		self.confidence_label = ttk.Label(self.content, text='Confidence = --%')

		self.message_label = ttk.Label(self.content)
		self.update_message_label('start')

		name_label = ttk.Label(self.content, text='Subject Name: ')
		gesture_label = ttk.Label(self.content, text='Gesture Name: ')

		self.name_entry = ttk.Entry(self.content)
		self.gesture_entry = ttk.Entry(self.content)

		self.name_entry.insert(0,"Dumb")
		self.gesture_entry.insert(0,"Testing Gesture")



		self.content.grid(column=0, row=0, sticky=(N, S, E, W))

		self.confidence_label.grid(column=1, row=0, sticky=W, padx=15, pady=15, columnspan=3)
		self.message_label.grid(column=2, row=1, columnspan=3)
		settings.grid(column=5,row=0, sticky=(N,E), pady=15, padx=15)
		self.undo_b.grid(column=1, row=3, sticky=E, padx=15)
		save.grid(column=1, row=4, sticky=E, padx=15)
		name_label.grid(column=3, row=3, sticky=E, padx=5)
		gesture_label.grid(column=3, row=4, sticky=E, padx=5)
		self.name_entry.grid(column=4, row=3, columnspan=2, sticky=W, padx=15)
		self.gesture_entry.grid(column=4, row=4, columnspan=2, sticky=W, padx=15)

		self.parent.columnconfigure(0, weight=1)
		self.parent.rowconfigure(0, weight=1)
		self.content.columnconfigure(0, weight=1)
		self.content.columnconfigure(1, weight=1)
		self.content.columnconfigure(2, weight=4)
		self.content.columnconfigure(3, weight=1)
		self.content.columnconfigure(4, weight=3)
		self.content.columnconfigure(5, weight=1)
		self.content.rowconfigure(1, weight=5)
		self.content.rowconfigure(2, weight=1)
		self.content.rowconfigure(3, weight=1)
		self.content.rowconfigure(4, weight=1)

	def init_dict(self):
		self.message_dict['start'] = "Press Save to Start!"
		self.message_dict['gesture'] = "Perform the gesture!"
		self.message_dict['success'] = "Success!"
		self.message_dict['fail_db'] = "Database problem!\nPlease start mongod."
		self.message_dict['no_device'] = "No device detected!\nPlease connect the Leap Motion."
		self.message_dict['undo_success'] = "Undo Successful!"
		self.message_dict['undo_fail'] = "Undo fail!\nPlease check the database."
		self.message_dict['exit'] = "Exiting..."


	# Updates the confidence label when a new frame is captured
	def update_confidence_label(self, conf):
		self.confidence_label['text'] = 'Confidence = '+ str(int(conf*100)) + '%'
		## Change the main frame color
		# s =  ttk.Style()
		# s.configure('My.TFrame', background='blue')
		# self.content.config(style='My.TFrame')

	# Updates the message label with the correct message
	def update_message_label(self,mens):
		self.message_label['text'] = self.message_dict[mens]

	# Responsable for closing the window
	def close_window(self):
		if(self.active_thread != None and self.active_thread.is_alive()):
			self.active_thread._stop.set()
		self.parent.destroy()

	# Creates a new window or just sets focus to a window already open
	def open_settings(self):
		if self.counter == 0:
			self.sett = Tk()
			new_window = SettingsWindow(self.sett, self)
			self.counter = self.counter + 1
		else:
			self.sett.focus_force()
			self.sett.lift()

	# Saves the captured gesture in the database
	def save_gesture(self):
		name = self.name_entry.get()
		gesture = self.gesture_entry.get()
		# n_frames

		self.update_message_label('gesture')
		t = st.SaveThread(1, name, gesture, self)
		t.start()

		self.active_thread = t
		self.master.after(100, self.process_queue)

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
			if(msg.startswith('success')):
				[msg, self.last_oid, self.last_db_name, self.last_col_name] = msg.split(' ')
				self.undo_b['state'] = 'normal'

			self.update_message_label(msg)
			
		except Queue.Empty:
			self.master.after(1000, self.process_queue)

	def undo(self):
		oid = self.last_oid
		db_name = self.last_db_name
		col_name = self.last_col_name

		ret = capture.undo_data(oid, db_name, col_name)

		self.update_message_label(ret)

		self.undo_b['state'] = 'disabled'


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
		self.confidence_entry.configure(state='disabled')

		dbname_label = ttk.Label(self.content, text='Database Name: ')
		self.dbname_entry = ttk.Entry(self.content)

		# Comment what a collection is!
		collection_name_label = ttk.Label(self.content, text='Collection Name: ')
		self.collection_name_entry = ttk.Entry(self.content)

		n_frames_label = ttk.Label(self.content, text='# of Frames/Gesture: ')
		self.n_frames_entry = ttk.Entry(self.content)
		self.n_frames_entry.configure(state='disabled')

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
		# self.father.set_n_frames(float(self.n_frames_entry.get()))
		# self.father.set_minimum_confidence(float(self.confidence_entry.get()))
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