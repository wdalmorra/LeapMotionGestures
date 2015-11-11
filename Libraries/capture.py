import os, sys, inspect, json
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'LeapSDK/lib/x64' if sys.maxsize > 2**32 else 'LeapSDK/lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import Finger

def get_data(controller, label):
	frame = controller.frame()

	hands = frame.hands

	d = {}
	d[label] = {}

	for hand in hands:
		if hand.is_valid:
			if hand.is_right:
				which_hand = 'right_hand'
			else:
				which_hand = 'left_hand'

			d[label][which_hand] = {}

			d[label][which_hand]['confidence'] = hand.confidence
			d[label][which_hand]['direction'] = hand.direction
			d[label][which_hand]['grab_strength'] = hand.grab_strength
			d[label][which_hand]['palm_normal'] = hand.palm_normal
			d[label][which_hand]['palm_position'] = hand.palm_position
			d[label][which_hand]['palm_velocity'] = hand.palm_velocity
			d[label][which_hand]['palm_width'] = hand.palm_width
			d[label][which_hand]['palm_strength'] = hand.palm_strength
			d[label][which_hand]['sphere_center'] = hand.sphere_center
			d[label][which_hand]['sphere_radius'] = hand.sphere_radius
			d[label][which_hand]['stabilized_palm_position'] = hand.stabilized_palm_position

			arm = hand.arm
			d[label][which_hand]['arm'] = {}

			d[label][which_hand]['arm']['direction'] = arm.direction
			d[label][which_hand]['arm']['elbow_position'] = arm.elbow_position
			d[label][which_hand]['arm']['wrist_position'] = arm.wrist_position

			fingers = hand.fingers

			for finger in fingers:
				if finger.type = Finger.TYPE_THUMB:
					which_finger = 'thumb'
				elif finger.type = Finger.TYPE_INDEX:
					which_finger = 'index'
				elif finger.type = Finger.TYPE_MIDDLE:
					which_finger = 'middle'
				elif finger.type = Finger.TYPE_RING:
					which_finger = 'ring'
				elif finger.type = Finger.TYPE_PINKY:
					which_finger = 'pinky'
				else:
					break

				d[label][which_hand][which_finger] = {}

				d[label][which_hand][which_finger]['direction'] = finger.direction
				d[label][which_hand][which_finger]['length'] = finger.length
				d[label][which_hand][which_finger]['stabilized_tip_position'] = finger.stabilized_tip_position
				d[label][which_hand][which_finger]['tip_position'] = finger.tip_position
				d[label][which_hand][which_finger]['tip_velocity'] = finger.tip_velocity
				d[label][which_hand][which_finger]['width'] = finger.width

				for i in range(4):
					bone = 'bone_' + str(i)

					d[label][which_hand][which_finger][bone] = {}

					d[label][which_hand][which_finger][bone]['center'] = finger.bone(i).center
					d[label][which_hand][which_finger][bone]['direction'] = finger.bone(i).direction
					d[label][which_hand][which_finger][bone]['length'] = finger.bone(i).length
					d[label][which_hand][which_finger][bone]['width'] = finger.bone(i).width
					d[label][which_hand][which_finger][bone]['next_joint'] = finger.bone(i).next_joint
					d[label][which_hand][which_finger][bone]['prev_joint'] = finger.bone(i).prev_joint

	return d



def main(argv):
	listener = SampleListener()
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)

	label = 'Thainan'
	result = get_data(controller, label)

	jsonarray = json.dumps(result)

	try:
		f = open('teste.json', 'w')

		f.write(jsonarray)

		f.close()

	except Exception, e:
		print e

	# print result

if __name__ == '__main__':
	main(sys.argv[1:])