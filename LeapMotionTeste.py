import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'LeapSDK/lib/x64' if sys.maxsize > 2**32 else 'LeapSDK/lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from sklearn import svm


clf = svm.SVC()

class SampleListener(Leap.Listener):
	
	def on_init(self, controller):
		print "Initizalized"

	def on_connect(self, controller):
		print "Connected"
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

	def on_frame(self,controller):
		pass
		# print "Frame available"
		# frame = controller.frame()



def main():

	# Create a sample listener and controller
	listener = SampleListener()
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)
	a = "D"

	# Keep this running until Enter is pressed
	while a != "E":
		try:
			a = raw_input('Press Enter to get a frame: ')
			if a == '':
				frame = controller.frame()
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
				print "Frame: %d\npalmPosition: %s\nThumb: %s\nForefinger: %s\nMiddle Finger: %s\nRing Finger: %s\nLittle Finger: %s\npalmDirection: %s\npalmNormal: %s\nthumbDirection: %s\nforefingerDirection: %s\nmiddleFingerDirection: %s\nringFingerDirection: %s\nlittleFingerDirection: %s " % (frame.id, palmPosition, thumb, forefinger, middleFinger, ringFinger, littleFinger, palmDirection, palmNormal, thumbDirection, forefingerDirection, middleFingerDirection, ringFingerDirection, littleFingerDirection)
			
		except KeyboardInterrupt:
			pass
		finally:
			# Remove the sample listener when done
			controller.remove_listener(listener)
		pass


if __name__ == '__main__':
	main()
	
	