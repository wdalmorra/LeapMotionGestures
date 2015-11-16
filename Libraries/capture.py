import os, sys, inspect, json, datetime
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'LeapSDK/lib/x64' if sys.maxsize > 2**32 else 'LeapSDK/lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import Finger
import pprint
from pymongo import MongoClient

MODE_PRINT = 0
MODE_FILE = 1
MODE_MONGO = 2

def get_data(controller, name):
	frame = controller.frame()

	while not frame.is_valid:
		frame = controller.frame()

	hands = frame.hands

	d = {}
	d['utc'] = str(datetime.datetime.utcnow())
	d['name'] = name

	print len(hands)

	for hand in hands:
		print 'hand'
		if hand.is_valid:
			print 'valid'
			if hand.is_right:
				which_hand = 'right_hand'
			else:
				which_hand = 'left_hand'

			d[which_hand] = {}

			d[which_hand]['confidence'] = hand.confidence
			d[which_hand]['direction'] = hand.direction.to_tuple()
			d[which_hand]['grab_strength'] = hand.grab_strength
			d[which_hand]['palm_normal'] = hand.palm_normal.to_tuple()
			d[which_hand]['palm_position'] = hand.palm_position.to_tuple()
			d[which_hand]['palm_velocity'] = hand.palm_velocity.to_tuple()
			d[which_hand]['palm_width'] = hand.palm_width
			d[which_hand]['sphere_center'] = hand.sphere_center.to_tuple()
			d[which_hand]['sphere_radius'] = hand.sphere_radius
			d[which_hand]['stabilized_palm_position'] = hand.stabilized_palm_position.to_tuple()

			arm = hand.arm
			d[which_hand]['arm'] = {}

			d[which_hand]['arm']['direction'] = arm.direction.to_tuple()
			d[which_hand]['arm']['elbow_position'] = arm.elbow_position.to_tuple()
			d[which_hand]['arm']['wrist_position'] = arm.wrist_position.to_tuple()

			fingers = hand.fingers

			for finger in fingers:
				if finger.type == Finger.TYPE_THUMB:
					which_finger = 'thumb'
				elif finger.type == Finger.TYPE_INDEX:
					which_finger = 'index'
				elif finger.type == Finger.TYPE_MIDDLE:
					which_finger = 'middle'
				elif finger.type == Finger.TYPE_RING:
					which_finger = 'ring'
				elif finger.type == Finger.TYPE_PINKY:
					which_finger = 'pinky'
				else:
					break

				d[which_hand][which_finger] = {}

				d[which_hand][which_finger]['direction'] = finger.direction.to_tuple()
				d[which_hand][which_finger]['length'] = finger.length
				d[which_hand][which_finger]['stabilized_tip_position'] = finger.stabilized_tip_position.to_tuple()
				d[which_hand][which_finger]['tip_position'] = finger.tip_position.to_tuple()
				d[which_hand][which_finger]['tip_velocity'] = finger.tip_velocity.to_tuple()
				d[which_hand][which_finger]['width'] = finger.width

				for i in range(4):
					bone = 'bone_' + str(i)

					d[which_hand][which_finger][bone] = {}

					d[which_hand][which_finger][bone]['center'] = finger.bone(i).center.to_tuple()
					d[which_hand][which_finger][bone]['direction'] = finger.bone(i).direction.to_tuple()
					d[which_hand][which_finger][bone]['length'] = finger.bone(i).length
					d[which_hand][which_finger][bone]['width'] = finger.bone(i).width
					d[which_hand][which_finger][bone]['next_joint'] = finger.bone(i).next_joint.to_tuple()
					d[which_hand][which_finger][bone]['prev_joint'] = finger.bone(i).prev_joint.to_tuple()

		else:
			print 'not valid'

	return d



def main(argv):
	mode = MODE_MONGO

	controller = Leap.Controller()
	if mode == MODE_PRINT:
		pp = pprint.PrettyPrinter(indent=4)

	if mode == MODE_MONGO:
		client = MongoClient()
		db = client.test
		collection = db.test_col

	name = 'Thainan'
	result = get_data(controller, name)

	if mode == MODE_FILE:
		jsonarray = json.dumps(result)

	try:
		if mode == MODE_MONGO:
			postid = collection.insert(result)
			print("Inserted with id " + str(postid))

		if mode == MODE_FILE:
			f = open('teste.json', 'w')

			f.write(jsonarray)

			f.close()

	except Exception, e:
		print e

	if mode == MODE_PRINT:
		pp.pprint(result)

	

if __name__ == '__main__':
	main(sys.argv[1:])