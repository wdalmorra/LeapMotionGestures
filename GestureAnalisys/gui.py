import training
import call_guessing
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Example(QWidget):

	last_guesses = ['1','2','3','4','5','6','7','8','9','10']

	def __init__(self, parent=None):
		QWidget.__init__(self,parent)
		self.__initUI()

		self.clf = training.Classifier()
		self.clf.set_interface(self)
		self.clf.training()
		self.cg = call_guessing.Call_Guessing(self.clf)
		self.cg.start()


	def __initUI(self):

		self.gesture_label = QLabel("3", self)
		new_font = QFont("Times", 150, QFont.Bold)
		self.gesture_label.setFont(new_font)

		tmp = ''
		for g in self.last_guesses:
			tmp = g + " " + tmp
		
		self.history_label = QLabel(tmp,self)
		new_font2 = QFont("Times", 20, QFont.Bold)
		self.history_label.setFont(new_font2)



		hbox = QHBoxLayout()
		hbox.addStretch(1)
		hbox.addWidget(self.gesture_label)
		hbox.addStretch(1)

		hbox2 = QHBoxLayout()
		hbox2.addStretch(1)
		hbox2.addWidget(self.history_label)

		vbox = QVBoxLayout()
		vbox.addStretch(1)
		vbox.addLayout(hbox)
		vbox.addStretch(1)
		vbox.addLayout(hbox2)

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

		self.last_guesses = self.last_guesses[1:]
		self.last_guesses.append(gest)k

		tmp = ''
		for g in self.last_guesses:
			tmp = g + " " + tmp
		
		self.history_label = QLabel(tmp,self)
		new_font = QFont("Times", 30, QFont.Bold)
		self.gesture_label.setFont(new_font)





	def closeEvent(self, event):

		if(self.cg != None and self.cg.is_alive()):
			self.cg._stop.set()
		
		event.accept()