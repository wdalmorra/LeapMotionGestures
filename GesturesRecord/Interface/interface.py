from Tkinter import *
import ttk
class Example(Frame):

	confidence = None
	content = None
	def __init__(self, master):
		Frame.__init__(self,master)

		self.parent = master
		self.initUI()
	
	def centerWindow(self):

		w = 1280
		h = 780

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()

		x = (sw - w)/2
		y = (sh - h)/2

		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

	def initUI(self):
		self.centerWindow()

		text = StringVar()
		text.set('Confidence = --%')
		self.content = ttk.Frame(self.parent, padding=(3,3,3,3))

		settings = ttk.Button(self.content, text="Settings")
		save = ttk.Button(self.content, text="Save")
		self.confidence = ttk.Label(self.content, text='Confidence = --%')

		self.content.grid(column=0, row=0, sticky=(N, S, E, W))

		self.confidence.grid(column=1, row=0, sticky=(N, E),pady=15)
		settings.grid(column=4,row=0, sticky=(N, E), pady=15, padx=15)
		save.grid(column=1, row=3, sticky=(N, E),pady=25)

		self.setConfidence(34)

		self.parent.columnconfigure(0, weight=1)
		self.parent.rowconfigure(0, weight=1)
		self.content.columnconfigure(0, weight=3)
		self.content.columnconfigure(1, weight=3)
		self.content.columnconfigure(2, weight=3)
		self.content.columnconfigure(3, weight=1)
		self.content.columnconfigure(4, weight=1)
		self.content.rowconfigure(1, weight=1)
		
	def setConfidence(self, conf):
		self.confidence['text'] = 'Confidence = '+ str(conf) + '%'
		# s =  ttk.Style()
		# s.configure('My.TFrame', background='blue')
		# self.content.config(style='My.TFrame')

def main():

	root = Tk()
	app = Example(root)
	root.mainloop()


if __name__ == '__main__':
	main()
