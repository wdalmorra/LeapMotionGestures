import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'LeapSDK/lib/x64' if sys.maxsize > 2**32 else 'LeapSDK/lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import Finger

def distance_between_fingers(hand):
	if hand.is_valid:
		distance = []

		thumb = hand.fingers[Finger.TYPE_THUMB].tip_position
		index = hand.fingers[Finger.TYPE_INDEX].tip_position
		middle = hand.fingers[Finger.TYPE_MIDDLE].tip_position
		ring = hand.fingers[Finger.TYPE_RING].tip_position
		pinky = hand.fingers[Finger.TYPE_PINKY].tip_position

		# thumb = Leap.Vector(10, 0, 0)
		# index = Leap.Vector(0, 20, 0)
		# middle = Leap.Vector(10, 20, 0)
		# ring = Leap.Vector(10, 0, 30)
		# pinky = Leap.Vector(0, 0, 30)

		distance.append(thumb.distance_to(index))
		distance.append(index.distance_to(middle))
		distance.append(middle.distance_to(ring))
		distance.append(ring.distance_to(pinky))

		return distance

	return None


def main(argv):
	hand = Leap.Hand()

	d = distance_between_fingers(hand)

	print d



if __name__ == '__main__':
	main(sys.argv[1:])