from pymongo import MongoClient
import sys
import pprint

def main(argv):
	try:
		client = MongoClient()
		db = client['project']
		collection = db['gestures']
		corrected = db['corrected']
		pp = pprint.PrettyPrinter(indent=4)

		cursor = collection.find()

		for gesture in cursor:
			edit = gesture

			fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
			bones = ['bone_0', 'bone_1', 'bone_2', 'bone_3']

			palm = gesture['right_hand']['palm_position']

			for finger in fingers:
				for i in range(3):
					edit['right_hand'][finger]['stabilized_tip_position'][i] = gesture['right_hand'][finger]['stabilized_tip_position'][i] - palm[i]
					edit['right_hand'][finger]['tip_position'][i] = gesture['right_hand'][finger]['tip_position'][i] - palm[i]

				for bone in bones:
					for i in range(3):
						edit['right_hand'][finger][bone]['center'][i] = gesture['right_hand'][finger][bone]['center'][i] - palm[i]
						edit['right_hand'][finger][bone]['next_joint'][i] = gesture['right_hand'][finger][bone]['next_joint'][i] - palm[i]
						edit['right_hand'][finger][bone]['prev_joint'][i] = gesture['right_hand'][finger][bone]['prev_joint'][i] - palm[i]

			for i in range(3):
				edit['right_hand']['arm']['wrist_position'][i] = gesture['right_hand']['arm']['wrist_position'][i] - palm[i]
				edit['right_hand']['arm']['elbow_position'][i] = gesture['right_hand']['arm']['elbow_position'][i] - palm[i]
				edit['right_hand']['stabilized_palm_position'][i] = gesture['right_hand']['stabilized_palm_position'][i] - palm[i]
				edit['right_hand']['palm_position'] = palm[i] - palm[i]

			oid = corrected.insert(edit)

			# pp.pprint(edit)
			# print palm
			# break

	except Exception, e:
		print e

if __name__ == '__main__':
	main(sys.argv[1:])