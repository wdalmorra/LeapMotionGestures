import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'LeapSDK/lib/x64' if sys.maxsize > 2**32 else 'LeapSDK/lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from sklearn import svm

clf = svm.SVC(kernel = 'linear', C = 1.0)

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
				hands = frame.hands[0]
				fingers = hands.fingers
				palmPosition = hands.palm_position - hands.palm_position
				thumb = fingers[0].tip_position - hands.palm_position
				forefinger = fingers[1].tip_position - hands.palm_position
				middleFinger = fingers[2].tip_position - hands.palm_position
				ringFinger = fingers[3].tip_position - hands.palm_position
				littleFinger = fingers[4].tip_position - hands.palm_position
				palmDirection = hands.direction
				palmNormal = hands.palm_normal
				thumbDirection = fingers[0].direction
				forefingerDirection = fingers[1].direction
				middleFingerDirection = fingers[2].direction
				ringFingerDirection = fingers[3].direction
				littleFingerDirection = fingers[4].direction

				sample = [[thumb.x, thumb.y, thumb.z, forefinger.x, forefinger.y, forefinger.z, middleFinger.x, middleFinger.y, middleFinger.z, ringFinger.x, ringFinger.y, ringFinger.z, littleFinger.x, littleFinger.y, littleFinger.z]]
				a = clf.predict(sample)
				if a[0] != last_gesture:
					print answers[a[0]]
					last_gesture = a[0]

def read_file(file1,classification):
	for line in file1:
		line = line.split(' ')
		tmp = []
		type_of_hand = line[0]
		for x in line[1:]:
			tmp.append(float(x))
		if type_of_hand == 0:
			X_right.append(tmp)
			Y_right.append(classification)
		elif type_of_hand == 1:
			X_left.append(tmp)
			Y_left.append(classification)
		else:
			X_two_hands.append(tmp)
			Y_two_hands.append(classification)

def learning():


	# Defining samples and classifications

	oh_file = open('Gestos Gravados/arquivo_mao_aberta','r')
	ch_file = open('Gestos Gravados/arquivo_mao_fechada','r')
	rs_file = open('Gestos Gravados/arquivo_rock','r')



	read_file(oh_file,OPEN_HAND)
	read_file(ch_file,CLOSED_HAND)
	read_file(rs_file,ROCK_SYMBOL)

	# print X
	# print Y

	clf.fit(X_right,Y_right)


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
	
	