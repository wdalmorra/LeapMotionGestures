import os, sys, datetime, time
src_dir = os.environ['LEAP_HOME']
lib_dir = 'lib/'
join_dir = os.path.join(src_dir, lib_dir)
sys.path.append(join_dir)
arch_dir = 'x64/' if sys.maxsize > 2**32 else 'x86/'
join_dir = os.path.join(join_dir, arch_dir)
sys.path.append(join_dir)

from Leap import Finger
import mongodb as mongo

def save_data(params):
	name = params.name
	gesture = params.gesture
	display = params.display
	controller = display.controller

	devices = controller.devices
	if len(devices) == 0:
		return 'no_device'

	frame = controller.frame()

	while not frame.is_valid:
		if(params._stop.is_set()):
			return 'exit'

		frame = controller.frame()

	hands = frame.hands

	while len(hands) == 0:
		if(params._stop.is_set()):
			return 'exit'

		frame = controller.frame()
		hands = frame.hands

	time.sleep(1)

	while True:
		if(params._stop.is_set()):
			return 'exit'

		frame = controller.frame()
		hands = frame.hands

		if len(hands) > 0:
			if(params._stop.is_set()):
				return 'exit'

			confidence_now = hands[0].confidence

			display.update_confidence_label(confidence_now)

			if confidence_now >= display.confidence:
				break

	d = {}
	d['utc'] = str(datetime.datetime.utcnow())
	d['name'] = name
	d['gesture'] = gesture

	print 'Confidence: ' + str(confidence_now)

	for hand in hands:
		if hand.is_valid:
			print 'Valid hand'
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
			print 'Not a valid hand'

	return mongo.save(d, display.db_name, display.collection_name)