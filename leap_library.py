import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'LeapSDK/lib/x64' if sys.maxsize > 2**32 else 'LeapSDK/lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import Finger

# @param: hand
# @return: list of distances (thumb -> index)
#							 (index -> middle)
#							 (middle -> ring)
#							 (ring -> pinky)
def distance_between_fingers(hand):
	if hand.is_valid:
	# if True:
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

# @param: hand
# @return: list of distances (palm -> thumb) 
#							 (palm -> index)
#							 (palm -> middle)
#							 (palm -> ring)
#							 (palm -> pinky)
def distance_to_fingertips(hand):
	if hand.is_valid:
	# if True:
		distance = []

		thumb = hand.fingers[Finger.TYPE_THUMB].tip_position
		index = hand.fingers[Finger.TYPE_INDEX].tip_position
		middle = hand.fingers[Finger.TYPE_MIDDLE].tip_position
		ring = hand.fingers[Finger.TYPE_RING].tip_position
		pinky = hand.fingers[Finger.TYPE_PINKY].tip_position

		palm = hand.palm_position

		# thumb = Leap.Vector(10, 0, 0)
		# index = Leap.Vector(0, 20, 0)
		# middle = Leap.Vector(10, 20, 0)
		# ring = Leap.Vector(10, 0, 30)
		# pinky = Leap.Vector(0, 0, 30)

		# palm = Leap.Vector(10, 20, 10)

		distance.append(palm.distance_to(thumb))
		distance.append(palm.distance_to(index))
		distance.append(palm.distance_to(middle))
		distance.append(palm.distance_to(ring))
		distance.append(palm.distance_to(pinky))

		return distance

	return None

# @param: hand
# @return: list of Leap.Vector (thumb, index, middle, ring, pinky) 
def translate_to_origin(hand):
	if hand.is_valid:
	# if True:
		fingers = []

		thumb = hand.fingers[Finger.TYPE_THUMB].tip_position
		index = hand.fingers[Finger.TYPE_INDEX].tip_position
		middle = hand.fingers[Finger.TYPE_MIDDLE].tip_position
		ring = hand.fingers[Finger.TYPE_RING].tip_position
		pinky = hand.fingers[Finger.TYPE_PINKY].tip_position

		palm = hand.palm_position

		# thumb = Leap.Vector(10, 0, 0)
		# index = Leap.Vector(0, 20, 0)
		# middle = Leap.Vector(10, 20, 0)
		# ring = Leap.Vector(10, 0, 30)
		# pinky = Leap.Vector(0, 0, 30)

		# palm = Leap.Vector(10, 20, 10)

		fingers.append(thumb - palm)
		fingers.append(index - palm)
		fingers.append(middle - palm)
		fingers.append(ring - palm)
		fingers.append(pinky - palm)

		return fingers

	return None


def main(argv):
	hand = Leap.Hand()

	a = translate_to_origin(hand)

	# for aa in a:
	# 	print aa


if __name__ == '__main__':
	main(sys.argv[1:])