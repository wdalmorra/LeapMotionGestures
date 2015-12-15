import interface, sys, os
from Tkinter import *

def main(argv):
	directory = os.path.join(os.getcwd(), 'images')
	if(not os.path.exists(directory)):
		os.makedirs(directory)

	root = Tk()
	app = interface.Example(root)
	root.mainloop()

if __name__ == '__main__':
	main(sys.argv[1:])