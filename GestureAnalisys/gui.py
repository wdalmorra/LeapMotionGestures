from Tkinter import *
import ttk
import training
import call_guessing

class MainWindow(Frame):

	gesture_label = None			# Label used to show the gesture predicted
	clf = None
	cg = None

	def __init__(self,master):
		Frame.__init__(self,master)

		self.parent = master
		self.parent.protocol('WM_DELETE_WINDOW', self.close_window)

		self.__init_ui()

		self.clf = training.Classifier()
		self.clf.set_interface(self)
		self.clf.training()
		self.cg = call_guessing.Call_Guessing(self.clf)
		self.cg.start()


	# Centers and sizes the window according to the size of the screen
	def __center_window(self):

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		w = sw / 4;
		h = sh / 4;

		x = (sw - w)/2
		y = (sh - h)/2

		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

	# Create all the widgets and layouts
	def __init_ui(self):
		self.__center_window()

		self.content = ttk.Frame(self.parent, padding=(3,3,3,3))

		self.gesture_label = ttk.Label(self.content, font="-weight bold")
		self.update_gesture_label('-')

		self.content.grid(column=0, row=0, sticky=(N, S, E, W))

		self.gesture_label.grid(column=3, row=3, padx=15, pady=15, sticky=(N, S, E, W))


	# Updates the message label with the correct message
	def update_gesture_label(self, gest):
		self.gesture_label['text'] = gest

	# Responsable for closing the window
	def close_window(self):
		if(self.cg != None and self.cg.is_alive()):
			self.cg._stop.set()
		self.parent.destroy()