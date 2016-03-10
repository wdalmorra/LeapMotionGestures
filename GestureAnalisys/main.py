import gui, sys, os
from Tkinter import *

def main(argv):

	root = Tk()
	app = gui.MainWindow(root)
	root.mainloop()

if __name__ == '__main__':
	main(sys.argv[1:])