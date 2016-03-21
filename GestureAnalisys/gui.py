import training
import call_guessing
import sys, os
import subprocess as sub
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Gui(QWidget):

	last_guesses = ['-','-','-','-','-','-','-','-','-','-']

	def __init__(self, parent=None):
		QWidget.__init__(self,parent)

		self.clf = training.Classifier()
		self.clf.set_interface(self)
		self.clf.training()

		self.__initUI()

		self.cg = call_guessing.Call_Guessing(self.clf)
		self.cg.start()


	def getPasswordFromUser(self):
		qid = QInputDialog()
		password, ok = qid.getText(self, 'Start Leap Motion', 'User password:', echo=QLineEdit.Password)

		if ok:
			p = os.system('echo %s|sudo -S %s' % (str(password), 'sudo leapd &'))
			# p = sub.Popen(['echo %s|sudo -S %s' % (str(password), 'sudo leapd &')],stdout=sub.PIPE,stderr=sub.PIPE)
			# output, errors = p.communicate()
			# print output
			print p

	def retrain(self):
		os.system("rm " + self.clf.trained_file)
		self.clf.training()
		self.trainSVM.setText("Retrain")

	def __initUI(self):

		self.gesture_label = QLabel("-", self)
		new_font = QFont("Times", 150, QFont.Bold)
		self.gesture_label.setFont(new_font)

		self.startLeap = QPushButton("Start Leap Motion",self)
		self.startLeap.clicked.connect(self.getPasswordFromUser)

		self.trainSVM = QPushButton(self)
		if os.path.isfile(self.clf.trained_file):
			self.trainSVM.setText("Retrain")
		else:
			self.trainSVM.setText("Train")
		self.trainSVM.clicked.connect(self.retrain)

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

		hbox3 = QHBoxLayout()
		hbox3.addWidget(self.trainSVM)
		hbox3.addStretch(1)
		hbox3.addWidget(self.startLeap)

		vbox = QVBoxLayout()
		vbox.addLayout(hbox3)
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
		self.last_guesses = self.last_guesses[1:]
		self.last_guesses.append(str(self.gesture_label.text()))

		self.gesture_label.setText(gest)

		tmp = ''
		for g in self.last_guesses:
			tmp = g + ' ' + tmp

		self.history_label.setText(tmp)



	def closeEvent(self, event):

		if(self.cg != None and self.cg.is_alive()):
			self.cg._stop.set()
		
		event.accept()