import interface, sys
from Tkinter import *

def main(argv):
	root = Tk()
	app = interface.Example(root)
	root.mainloop()

if __name__ == '__main__':
	main(sys.argv[1:])