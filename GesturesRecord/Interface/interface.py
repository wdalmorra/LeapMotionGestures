from Tkinter import *
import ttk
import Tkinter as tk
class Example(Frame):

	confidence = None
	content = None
	sett = None
	counter = 0

	def __init__(self, master):
		Frame.__init__(self,master)

		self.parent = master
		self.parent.protocol('WM_DELETE_WINDOW', self.close_window)
		
		self.init_ui()
	
	def center_window(self):

		w = 1280
		h = 780

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw - w)/2
		y = (sh - h)/2

		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def init_ui(self):
		self.center_window()

		text = StringVar()
		text.set('Confidence = --%')
		self.content = ttk.Frame(self.parent, padding=(3,3,3,3))

		settings = ttk.Button(self.content, text="Settings", command=self.open_settings)
		save = ttk.Button(self.content, text="Save", command=self.save_gesture)
		self.confidence = ttk.Label(self.content, text='Confidence = --%')

		self.content.grid(column=0, row=0, sticky=(N, S, E, W))

		self.confidence.grid(column=1, row=0, sticky=(N, E),pady=15)
		settings.grid(column=4,row=0, sticky=(N, E), pady=15, padx=15)
		save.grid(column=1, row=3, sticky=(N, E),pady=25)

		# self.setConfidence(34)

		self.parent.columnconfigure(0, weight=1)
		self.parent.rowconfigure(0, weight=1)
		self.content.columnconfigure(0, weight=3)
		self.content.columnconfigure(1, weight=3)
		self.content.columnconfigure(2, weight=3)
		self.content.columnconfigure(3, weight=1)
		self.content.columnconfigure(4, weight=1)
		self.content.rowconfigure(1, weight=1)
		
	def set_confidence(self, conf):
		self.confidence['text'] = 'Confidence = '+ str(conf) + '%'
		# Modificar a cor do frame principal
		# s =  ttk.Style()
		# s.configure('My.TFrame', background='blue')
		# self.content.config(style='My.TFrame')

	def close_window(self):
		self.parent.destroy()

	def open_settings(self):
		if self.counter == 0:
			self.sett = Tk()
			new_window = SettingsWindow(self.sett, self)
			self.counter = self.counter + 1
		else:
			self.sett.focus_force()
			self.sett.lift()

	def save_gesture(self):
		pass


class SettingsWindow(Frame):
	def __init__(self, master,father):
		Frame.__init__(self,master)
		self.parent = master
		self.father = father
		self.parent.protocol('WM_DELETE_WINDOW', self.close_window)
		self.init_ui()

	def init_ui(self):


		self.content = ttk.Frame(self.parent, padding=(3,3,3,3))

		confidence_label = ttk.Label(self.content, text='Minimum Confidence: ')
		confidence_entry = ttk.Entry(self.content)

		n_frames_label = ttk.Label(self.content, text='# of Frames/Gesture: ')
		n_frames_entry = ttk.Entry(self.content)

		save_button = ttk.Button(self.content, text="Save", command=self.save_settings)
		cancel_button = ttk.Button(self.content, text="Cancel", command=self.cancel)

		self.content.grid(column=0, row=0, sticky=(N, S, E, W))
		confidence_label.grid(column=0, row=0, pady=15, padx=15)
		confidence_entry.grid(column=1, row=0, pady=15, padx=15)
		n_frames_label.grid(column=0, row=1, pady=15, padx=15)
		n_frames_entry.grid(column=1, row=1, pady=15, padx=15)
		save_button.grid(column=0, row=2, pady=15, padx=15)
		cancel_button.grid(column=1, row=2, pady=15, padx=15)

		self.parent.columnconfigure(0, weight=1)
		self.parent.rowconfigure(0, weight=1)
		self.content.columnconfigure(0, weight=3)
		self.content.columnconfigure(1, weight=3)
		self.content.rowconfigure(1, weight=1)
		self.content.rowconfigure(2, weight=1)
		
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
		pass

	def cancel(self):
		pass

	def close_window(self):
		self.father.counter = self.father.counter - 1
		self.parent.destroy()

def main():

	root = Tk()
	app = Example(root)
	root.mainloop()


if __name__ == '__main__':
	main()
