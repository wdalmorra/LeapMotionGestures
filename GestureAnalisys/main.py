import gui, sys, os
from PyQt5.QtWidgets import *

def main(argv):

    app = QApplication(sys.argv)
    ex = gui.Gui()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
	main(sys.argv[1:])