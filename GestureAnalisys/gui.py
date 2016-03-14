import training
import call_guessing
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Example(QWidget):

	def __init__(self, parent=None):
		QWidget.__init__(self,parent)
		self.__initUI()

		self.clf = training.Classifier()
		self.clf.set_interface(self)
		self.clf.training()
		self.cg = call_guessing.Call_Guessing(self.clf)
		self.cg.start()


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

		if(self.cg != None and self.cg.is_alive()):
			self.cg._stop.set()
		
		event.accept()