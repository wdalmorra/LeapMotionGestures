import training
import call_guessing
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Example(QMainWindow):

    def __init__(self):
		super(Example, self).__init__()
		self.__initUI()

		self.clf = training.Classifier()
		self.clf.set_interface(self)
		self.clf.training()
		# self.cg = call_guessing.Call_Guessing(self.clf)
		# self.cg.start()

    def __initUI(self):

		self.gesture_label = QLabel("-", self)

		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(self.gesture_label)
		hbox.addStretch(1)

		vbox = QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(hbox)
		vbox.addStretch(1)

		self.setLayout(vbox)

		self.resize(800, 600)
		self.__center()

		self.setWindowTitle('Leap Motion')
		self.show()

    def __center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

	# Updates the message label with the correct message
	def update_gesture_label(self, gest):
		self.gesture_label.setText(gest)

	def closeEvent(self, event):

		print "Closing..."

		# if(self.cg != None and self.cg.is_alive()):
		# 	self.cg._stop.set()

		# event.accept()

# class MainWindow(Frame):

# 	gesture_label = None			# Label used to show the gesture predicted
# 	clf = None
# 	cg = None

# 	def __init__(self,master):
# 		Frame.__init__(self,master)

# 		self.parent = master
# 		self.parent.protocol('WM_DELETE_WINDOW', self.close_window)

# 		self.__init_ui()

# 		


# 	# Centers and sizes the window according to the size of the screen
# 	def __center_window(self):

# 		sw = self.parent.winfo_screenwidth()
# 		sh = self.parent.winfo_screenheight()

# 		w = sw / 4;
# 		h = sh / 4;

# 		x = (sw - w)/2
# 		y = (sh - h)/2

# 		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

# 	# Create all the widgets and layouts
# 	def __init_ui(self):
# 		self.__center_window()

# 		self.content = ttk.Frame(self.parent, padding=(3,3,3,3))

# 		self.gesture_label = ttk.Label(self.content, font="-weight bold")
# 		self.update_gesture_label('-')

# 		self.content.grid(column=0, row=0, sticky=(N, S, E, W))

# 		self.gesture_label.grid(column=3, row=3, padx=15, pady=15, sticky=(N, S, E, W))



# 	# Responsable for closing the window
# 	def close_window(self):
# 		
# 		self.parent.destroy()