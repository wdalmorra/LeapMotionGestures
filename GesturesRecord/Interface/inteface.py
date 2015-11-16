from Tkinter import *
import ttk

def centerWindow(master):

		w = 1280
		h = 780

		sw = master.winfo_screenwidth()
		sh = master.winfo_screenheight()

		x = (sw - w)/2
		y = (sh - h)/2

		master.geometry('%dx%d+%d+%d' % (w, h, x, y))

root = Tk()

centerWindow(root)

content = ttk.Frame(root, width=1280, height=780 ,padding=(3,3,3,3))

settings = ttk.Button(content, text="Settings")
save = ttk.Button(content, text="Save")
confiability = ttk.Label(content, text="Confiability = ")


content.grid(column=0, row=0, sticky=(N, S, E, W))

confiability.grid(column=1, row=0, sticky=(N, E),pady=15)
settings.grid(column=4,row=0, sticky=(N, E), pady=15, padx=15)
save.grid(column=1, row=3, sticky=(N, E),pady=25)


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

root.mainloop()