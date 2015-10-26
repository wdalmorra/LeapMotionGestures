import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'LeapSDK/lib/x64' if sys.maxsize > 2**32 else 'LeapSDK/lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from sklearn import svm
from sklearn.metrics import accuracy_score

clf_right = svm.SVC(kernel = 'linear', C = 1.0)
clf_left = svm.SVC(kernel = 'linear', C = 1.0)
clf_two_hands = svm.SVC(kernel = 'linear', C = 1.0)

OPEN_HAND = 0
CLOSED_HAND = 1
ROCK_SYMBOL = 2

X_right = []
Y_right = []
X_left = []
Y_left = []
X_two_hands = []
Y_two_hands = []

answers = ["OPEN HAND", "CLOSED HAND", "ROCK SYMBOL"]

last_gesture = -1

class SampleListener(Leap.Listener):

	def on_init(self, controller):
		learning()
		print "Initizalized"

	def on_connect(self, controller):
		print "Connected"

	def on_frame(self,controller):

		global last_gesture

		frame = controller.frame()
		if (frame.id % 100) == 0:
			if not frame.hands.is_empty:
				hand = frame.hands[0]
				fingers = hands.fingers
				palmPosition = hand.palm_position - hand.palm_position
				thumb = fingers[0].tip_position - hand.palm_position
				forefinger = fingers[1].tip_position - hand.palm_position
				middleFinger = fingers[2].tip_position - hand.palm_position
				ringFinger = fingers[3].tip_position - hand.palm_position
				littleFinger = fingers[4].tip_position - hand.palm_position
				palmDirection = hand.direction
				palmNormal = hand.palm_normal
				thumbDirection = fingers[0].direction
				forefingerDirection = fingers[1].direction
				middleFingerDirection = fingers[2].direction
				ringFingerDirection = fingers[3].direction
				littleFingerDirection = fingers[4].direction

				sample = [[thumb.x, thumb.y, thumb.z, forefinger.x, forefinger.y, forefinger.z, middleFinger.x, middleFinger.y, middleFinger.z, ringFinger.x, ringFinger.y, ringFinger.z, littleFinger.x, littleFinger.y, littleFinger.z]]
				
				a = []
				# acc = 0
				if len(frame.hands) == 2:
					pass
					# a = clf_two_hands.predict(sample)
					# acc = accuracy_score(Y_two_hands,a)
				else:
					if hands.is_left:
						a = clf_left.predict(sample)
						# acc = accuracy_score(Y_left,a)
					else:
						a = clf_right.predict(sample)
						# acc = accuracy_score(Y_right, a)
				if a[0] != last_gesture:
					print answers[a[0]]
					# print acc
					last_gesture = a[0]
			else:
				last_gesture = -1

def read_file(file1,classification):
	for line in file1:
		line = line.split(' ')
		tmp = []
		type_of_hand = line[0]
		for x in line[1:]:
			tmp.append(float(x))
		
		if type_of_hand == '0':
			X_right.append(tmp)
			Y_right.append(classification)
		elif type_of_hand == '1':
			X_left.append(tmp)
			Y_left.append(classification)
		else:
			X_two_hands.append(tmp)
			Y_two_hands.append(classification)

def learning():


	# Defining samples and classifications

	ohr_file = open('Gestos Gravados/arquivo_mao_aberta_direita','r')
	chr_file = open('Gestos Gravados/arquivo_mao_fechada_direita','r')
	rsr_file = open('Gestos Gravados/arquivo_rock_direita','r')

	ohl_file = open('Gestos Gravados/arquivo_mao_aberta_esquerda','r')
	chl_file = open('Gestos Gravados/arquivo_mao_fechada_esquerda','r')
	rsl_file = open('Gestos Gravados/arquivo_rock_esquerda','r')


	read_file(ohr_file,OPEN_HAND)
	read_file(chr_file,CLOSED_HAND)
	read_file(rsr_file,ROCK_SYMBOL)

	read_file(ohl_file,OPEN_HAND)
	read_file(chl_file,CLOSED_HAND)
	read_file(rsl_file,ROCK_SYMBOL)

	clf_right.fit(X_right,Y_right)
	clf_left.fit(X_left,Y_left)
	# clf_two_hands.fit(X_two_hands,Y_two_hands)

def main():

	# Create a sample listener and controller
	listener = SampleListener()
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)

	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		# Remove the sample listener when done
		controller.remove_listener(listener)
	pass



if __name__ == '__main__':
	main()
	
	