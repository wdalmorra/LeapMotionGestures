import os, sys, json, datetime, getopt, time
src_dir = os.environ['LEAP_HOME']
lib_dir = 'lib/'
join_dir = os.path.join(src_dir, lib_dir)
sys.path.append(join_dir)
arch_dir = 'x64/' if sys.maxsize > 2**32 else 'x86/'
join_dir = os.path.join(join_dir, arch_dir)
sys.path.append(join_dir)

import Leap
from Leap import Finger
from pymongo import MongoClient
# import pprint

# MODE_PRINT = 0
# MODE_FILE = 1
# MODE_MONGO = 2

def save_data(controller, name, confidence, db_name, col_name):
	frame = controller.frame()

	while not frame.is_valid:
		frame = controller.frame()

	hands = frame.hands

	while len(hands) == 0:
		frame = controller.frame()
		hands = frame.hands

	time.sleep(1)

	while True:
		frame = controller.frame()
		hands = frame.hands
		if len(hands) > 0:
			confidence_now = hands[0].confidence

		if confidence_now >= confidence:
			break

	d = {}
	d['utc'] = str(datetime.datetime.utcnow())
	d['name'] = name

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

	return save_on_mongo(d, db_name, col_name)

def save_on_mongo(data, db_name, col_name):
	client = MongoClient()
	db = client[db_name]
	collection = db[col_name]

	oid = collection.insert(data)

	if(oid != None):
		return True
	else:
		return False

# def main(argv):
# 	mode = MODE_MONGO
# 	db_name = 'test'
# 	collection_name = 'test_col'

# 	try:
# 		opts, args = getopt.getopt(argv,'hpm:f:')
# 	except getopt.GetoptError:
# 		print('usage: python2 capture.py <opt> <name>')
# 		print('<opt>: -h -p -m -f')
# 		print('<name>: <filename> or <collectionname> in case of <opt> -f or -m')
# 		print('Type python2 capture.py -h for help')
# 		sys.exit(2)
# 	if(opts == []):
# 		opts.append(('-h', ''))
# 	for opt, arg in opts:
# 		if opt == '-h':
# 			print('usage: python2 capture.py <opt> <name>')
# 			print('-h, Help')
# 			print('-p, Print debug information')
# 			print('-m, Upload info to <collectionname> in MongoDB')
# 			print('-f, Put JSON information in a file named <filename>')
# 			sys.exit()
# 		elif opt in ('-p'):
# 			mode = MODE_PRINT
# 		elif opt in ('-m'):
# 			mode = MODE_MONGO
# 			collection_name = arg
# 		elif opt in ('-f'):
# 			mode = MODE_FILE
# 			filename = arg

# 	controller = Leap.Controller()
# 	if mode == MODE_PRINT:
# 		pp = pprint.PrettyPrinter(indent=4)

# 	if mode == MODE_MONGO:
# 		client = MongoClient()
# 		db = client[db_name]
# 		collection = db[collection_name]

# 	name = 'Thainan'
# 	confidence = 0.5
# 	result = get_data(controller, name, confidence)

# 	if mode == MODE_FILE:
# 		jsonarray = json.dumps(result)

# 	try:
# 		if mode == MODE_MONGO:
# 			postid = collection.insert(result)
# 			print("Inserted with id " + str(postid))

# 		if mode == MODE_FILE:
# 			f = open(filename, 'w')

# 			f.write(jsonarray)

# 			f.close()

# 	except Exception, e:
# 		print e

# 	if mode == MODE_PRINT:
# 		pp.pprint(result)

	

# if __name__ == '__main__':
# 	main(sys.argv[1:])