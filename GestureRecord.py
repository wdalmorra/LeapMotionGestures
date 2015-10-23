import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'LeapSDK/lib/x64' if sys.maxsize > 2**32 else 'LeapSDK/lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap

class SampleListener(Leap.Listener):
	
	def on_init(self, controller):
		print "Initizalized"

	def on_connect(self, controller):
		print "Connected"

	def on_frame(self,controller):
		pass

def main():

	# Create a sample listener and controller
	listener = SampleListener()
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)
	a = "D"

	while a != 'E':
		try:
			a = raw_input('Press Enter to get a frame or \'E\' to exit: ')
			if a == '':

				frame = controller.frame()
				hand = frame.hands[0]
				fingers = hand.fingers
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

				type_of_hand = -1;
				if len(frame.hands) == 2:
					type_of_hand = 2
				else:
					if len(frame.hands) != 0:
						if frame.hands[0].is_left:
							type_of_hand = 1
						else:
							type_of_hand = 0
				
				print "Frame: %d\ntypeOfHand: %d\npalmPosition: %s\nThumb: %s\nForefinger: %s\nMiddle Finger: %s\nRing Finger: %s\nLittle Finger: %s\npalmDirection: %s\npalmNormal: %s\nthumbDirection: %s\nforefingerDirection: %s\nmiddleFingerDirection: %s\nringFingerDirection: %s\nlittleFingerDirection: %s " % (frame.id, type_of_hand, palmPosition, thumb, forefinger, middleFinger, ringFinger, littleFinger, palmDirection, palmNormal, thumbDirection, forefingerDirection, middleFingerDirection, ringFingerDirection, littleFingerDirection)

		except KeyboardInterrupt:
			pass
		finally:
			# Remove the sample listener when done
			controller.remove_listener(listener)
		pass



if __name__ == '__main__':
	main()
	
	