import sys
import json

columns = []
numbers = []

def name_columns_rec(name, data, index):

	if type(data) is list:
		columns.append(name+'.'+'X')
		numbers[index].append(data[0])
		columns.append(name+'.'+'Y')
		numbers[index].append(data[1])
		columns.append(name+'.'+'Z')
		numbers[index].append(data[2])
	elif type(data) is not dict:
		columns.append(name)
		numbers[index].append(data)
	else:
		for n in data:
			name_columns_rec(name+'.'+n, data[n],index)

def name_columns(file):
	data = []
	with open(file) as json_file:
		for line in json_file:
			data.append(json.loads(line))

	for i in range (len(data)):
		del columns[:]
		numbers.append([])
		for l in data[i]:
			name_columns_rec(l,data[i][l],i)

def main(argv):

	name_columns(argv[0])

	try:
		f = open(argv[0], 'r')
		lines = f.read().splitlines()
		f.close()
	except Exception, e:
		print e

	try:
		f = open(argv[1], 'w')

		first = True
		for column in columns:
			if first:
				first = False
			else:
				f.write(',')

			f.write(column)

		f.write('\n')

		for gesture in numbers:
			first = True

			for data in gesture:
				if first:
					first = False
				else:
					f.write(',')

				f.write(str(data))
			f.write('\n')

		f.close()

	except Exception, e1:
		print e1


if __name__ == '__main__':
	main(sys.argv[1:])



# 	columns = "_id.$oid,right_hand.index.direction.x,\
# right_hand.index.direction.y,right_hand.index.direction.z,right_hand.index.bone_1.direction.x,\
# right_hand.index.bone_1.direction.y,right_hand.index.bone_1.direction.z,right_hand.index.bone_1.center.x,\
# right_hand.index.bone_1.center.y,right_hand.index.bone_1.center.z,right_hand.index.bone_1.next_joint.x,\
# right_hand.index.bone_1.next_joint.y,right_hand.index.bone_1.next_joint.z,right_hand.index.bone_1.width,\
# right_hand.index.bone_1.length,right_hand.index.bone_1.prev_joint.x,right_hand.index.bone_1.prev_joint.y,\
# right_hand.index.bone_1.prev_joint.z,right_hand.index.bone_0.direction.x,\
# right_hand.index.bone_0.direction.y,right_hand.index.bone_0.direction.z,right_hand.index.bone_0.center.x,\
# right_hand.index.bone_0.center.y,right_hand.index.bone_0.center.z,right_hand.index.bone_0.next_joint.x,\
# right_hand.index.bone_0.next_joint.y,right_hand.index.bone_0.next_joint.z,right_hand.index.bone_0.width,\
# right_hand.index.bone_0.length,right_hand.index.bone_0.prev_joint.x,right_hand.index.bone_0.prev_joint.y,\
# right_hand.index.bone_0.prev_joint.z,right_hand.index.bone_3.direction.x,\
# right_hand.index.bone_3.direction.y,right_hand.index.bone_3.direction.z,right_hand.index.bone_3.center.x,\
# right_hand.index.bone_3.center.y,right_hand.index.bone_3.center.z,right_hand.index.bone_3.next_joint.x,\
# right_hand.index.bone_3.next_joint.y,right_hand.index.bone_3.next_joint.z,right_hand.index.bone_3.width,\
# right_hand.index.bone_3.length,right_hand.index.bone_3.prev_joint.x,right_hand.index.bone_3.prev_joint.y,\
# right_hand.index.bone_3.prev_joint.z,right_hand.index.bone_2.direction.x,\
# right_hand.index.bone_2.direction.y,right_hand.index.bone_2.direction.z,right_hand.index.bone_2.center.x,\
# right_hand.index.bone_2.center.y,right_hand.index.bone_2.center.z,right_hand.index.bone_2.next_joint.x,\
# right_hand.index.bone_2.next_joint.y,right_hand.index.bone_2.next_joint.z,right_hand.index.bone_2.width,\
# right_hand.index.bone_2.length,right_hand.index.bone_2.prev_joint.x,right_hand.index.bone_2.prev_joint.y,\
# right_hand.index.bone_2.prev_joint.z,right_hand.index.stabilized_tip_position.x,\
# right_hand.index.stabilized_tip_position.y,right_hand.index.stabilized_tip_position.z,\
# right_hand.index.width,right_hand.index.length,right_hand.index.tip_position.x,\
# right_hand.index.tip_position.y,right_hand.index.tip_position.z,right_hand.index.tip_velocity.x,\
# right_hand.index.tip_velocity.y,right_hand.index.tip_velocity.z,right_hand.confidence,\
# right_hand.thumb.direction.x,\
# right_hand.thumb.direction.y,right_hand.thumb.direction.z,right_hand.thumb.bone_1.direction.x,\
# right_hand.thumb.bone_1.direction.y,right_hand.thumb.bone_1.direction.z,right_hand.thumb.bone_1.center.x,\
# right_hand.thumb.bone_1.center.y,right_hand.thumb.bone_1.center.z,right_hand.thumb.bone_1.next_joint.x,\
# right_hand.thumb.bone_1.next_joint.y,right_hand.thumb.bone_1.next_joint.z,right_hand.thumb.bone_1.width,\
# right_hand.thumb.bone_1.length,right_hand.thumb.bone_1.prev_joint.x,right_hand.thumb.bone_1.prev_joint.y,\
# right_hand.thumb.bone_1.prev_joint.z,right_hand.thumb.bone_0.direction.x,\
# right_hand.thumb.bone_0.direction.y,right_hand.thumb.bone_0.direction.z,right_hand.thumb.bone_0.center.x,\
# right_hand.thumb.bone_0.center.y,right_hand.thumb.bone_0.center.z,right_hand.thumb.bone_0.next_joint.x,\
# right_hand.thumb.bone_0.next_joint.y,right_hand.thumb.bone_0.next_joint.z,right_hand.thumb.bone_0.width,\
# right_hand.thumb.bone_0.length,right_hand.thumb.bone_0.prev_joint.x,right_hand.thumb.bone_0.prev_joint.y,\
# right_hand.thumb.bone_0.prev_joint.z,right_hand.thumb.bone_3.direction.x,\
# right_hand.thumb.bone_3.direction.y,right_hand.thumb.bone_3.direction.z,right_hand.thumb.bone_3.center.x,\
# right_hand.thumb.bone_3.center.y,right_hand.thumb.bone_3.center.z,right_hand.thumb.bone_3.next_joint.x,\
# right_hand.thumb.bone_3.next_joint.y,right_hand.thumb.bone_3.next_joint.z,right_hand.thumb.bone_3.width,\
# right_hand.thumb.bone_3.length,right_hand.thumb.bone_3.prev_joint.x,right_hand.thumb.bone_3.prev_joint.y,\
# right_hand.thumb.bone_3.prev_joint.z,right_hand.thumb.bone_2.direction.x,\
# right_hand.thumb.bone_2.direction.y,right_hand.thumb.bone_2.direction.z,right_hand.thumb.bone_2.center.x,\
# right_hand.thumb.bone_2.center.y,right_hand.thumb.bone_2.center.z,right_hand.thumb.bone_2.next_joint.x,\
# right_hand.thumb.bone_2.next_joint.y,right_hand.thumb.bone_2.next_joint.z,right_hand.thumb.bone_2.width,\
# right_hand.thumb.bone_2.length,right_hand.thumb.bone_2.prev_joint.x,right_hand.thumb.bone_2.prev_joint.y,\
# right_hand.thumb.bone_2.prev_joint.z,right_hand.thumb.stabilized_tip_position.x,\
# right_hand.thumb.stabilized_tip_position.y,right_hand.thumb.stabilized_tip_position.z,\
# right_hand.thumb.width,right_hand.thumb.length,right_hand.thumb.tip_position.x,\
# right_hand.thumb.tip_position.y,right_hand.thumb.tip_position.z,right_hand.thumb.tip_velocity.x,\
# right_hand.thumb.tip_velocity.y,right_hand.thumb.tip_velocity.z,right_hand.sphere_radius,\
# right_hand.palm_position.x,right_hand.palm_position.y,right_hand.palm_position.z,right_hand.direction.x,\
# right_hand.direction.y,right_hand.direction.z,right_hand.stabilized_palm_position.x,\
# right_hand.stabilized_palm_position.y,right_hand.stabilized_palm_position.z,right_hand.arm.direction.x,\
# right_hand.arm.direction.y,right_hand.arm.direction.z,right_hand.arm.wrist_position.x,\
# right_hand.arm.wrist_position.y,right_hand.arm.wrist_position.z,right_hand.arm.elbow_position.x,\
# right_hand.arm.elbow_position.y,right_hand.arm.elbow_position.z,right_hand.pinky.direction.x,\
# right_hand.pinky.direction.y,right_hand.pinky.direction.z,right_hand.pinky.bone_1.direction.x,\
# right_hand.pinky.bone_1.direction.y,right_hand.pinky.bone_1.direction.z,right_hand.pinky.bone_1.center.x,\
# right_hand.pinky.bone_1.center.y,right_hand.pinky.bone_1.center.z,right_hand.pinky.bone_1.next_joint.x,\
# right_hand.pinky.bone_1.next_joint.y,right_hand.pinky.bone_1.next_joint.z,right_hand.pinky.bone_1.width,\
# right_hand.pinky.bone_1.length,right_hand.pinky.bone_1.prev_joint.x,right_hand.pinky.bone_1.prev_joint.y,\
# right_hand.pinky.bone_1.prev_joint.z,right_hand.pinky.bone_0.direction.x,\
# right_hand.pinky.bone_0.direction.y,right_hand.pinky.bone_0.direction.z,right_hand.pinky.bone_0.center.x,\
# right_hand.pinky.bone_0.center.y,right_hand.pinky.bone_0.center.z,right_hand.pinky.bone_0.next_joint.x,\
# right_hand.pinky.bone_0.next_joint.y,right_hand.pinky.bone_0.next_joint.z,right_hand.pinky.bone_0.width,\
# right_hand.pinky.bone_0.length,right_hand.pinky.bone_0.prev_joint.x,right_hand.pinky.bone_0.prev_joint.y,\
# right_hand.pinky.bone_0.prev_joint.z,right_hand.pinky.bone_3.direction.x,\
# right_hand.pinky.bone_3.direction.y,right_hand.pinky.bone_3.direction.z,right_hand.pinky.bone_3.center.x,\
# right_hand.pinky.bone_3.center.y,right_hand.pinky.bone_3.center.z,right_hand.pinky.bone_3.next_joint.x,\
# right_hand.pinky.bone_3.next_joint.y,right_hand.pinky.bone_3.next_joint.z,right_hand.pinky.bone_3.width,\
# right_hand.pinky.bone_3.length,right_hand.pinky.bone_3.prev_joint.x,right_hand.pinky.bone_3.prev_joint.y,\
# right_hand.pinky.bone_3.prev_joint.z,right_hand.pinky.bone_2.direction.x,\
# right_hand.pinky.bone_2.direction.y,right_hand.pinky.bone_2.direction.z,right_hand.pinky.bone_2.center.x,\
# right_hand.pinky.bone_2.center.y,right_hand.pinky.bone_2.center.z,right_hand.pinky.bone_2.next_joint.x,\
# right_hand.pinky.bone_2.next_joint.y,right_hand.pinky.bone_2.next_joint.z,right_hand.pinky.bone_2.width,\
# right_hand.pinky.bone_2.length,right_hand.pinky.bone_2.prev_joint.x,right_hand.pinky.bone_2.prev_joint.y,\
# right_hand.pinky.bone_2.prev_joint.z,right_hand.pinky.stabilized_tip_position.x,\
# right_hand.pinky.stabilized_tip_position.y,right_hand.pinky.stabilized_tip_position.z,\
# right_hand.pinky.width,right_hand.pinky.length,right_hand.pinky.tip_position.x,\
# right_hand.pinky.tip_position.y,right_hand.pinky.tip_position.z,right_hand.pinky.tip_velocity.x,\
# right_hand.pinky.tip_velocity.y,right_hand.pinky.tip_velocity.z,right_hand.middle.direction.x,\
# right_hand.middle.direction.y,right_hand.middle.direction.z,right_hand.middle.bone_1.direction.x,\
# right_hand.middle.bone_1.direction.y,right_hand.middle.bone_1.direction.z,right_hand.middle.bone_1.center.x,\
# right_hand.middle.bone_1.center.y,right_hand.middle.bone_1.center.z,right_hand.middle.bone_1.next_joint.x,\
# right_hand.middle.bone_1.next_joint.y,right_hand.middle.bone_1.next_joint.z,right_hand.middle.bone_1.width,\
# right_hand.middle.bone_1.length,right_hand.middle.bone_1.prev_joint.x,right_hand.middle.bone_1.prev_joint.y,\
# right_hand.middle.bone_1.prev_joint.z,right_hand.middle.bone_0.direction.x,\
# right_hand.middle.bone_0.direction.y,right_hand.middle.bone_0.direction.z,right_hand.middle.bone_0.center.x,\
# right_hand.middle.bone_0.center.y,right_hand.middle.bone_0.center.z,right_hand.middle.bone_0.next_joint.x,\
# right_hand.middle.bone_0.next_joint.y,right_hand.middle.bone_0.next_joint.z,right_hand.middle.bone_0.width,\
# right_hand.middle.bone_0.length,right_hand.middle.bone_0.prev_joint.x,right_hand.middle.bone_0.prev_joint.y,\
# right_hand.middle.bone_0.prev_joint.z,right_hand.middle.bone_3.direction.x,\
# right_hand.middle.bone_3.direction.y,right_hand.middle.bone_3.direction.z,right_hand.middle.bone_3.center.x,\
# right_hand.middle.bone_3.center.y,right_hand.middle.bone_3.center.z,right_hand.middle.bone_3.next_joint.x,\
# right_hand.middle.bone_3.next_joint.y,right_hand.middle.bone_3.next_joint.z,right_hand.middle.bone_3.width,\
# right_hand.middle.bone_3.length,right_hand.middle.bone_3.prev_joint.x,right_hand.middle.bone_3.prev_joint.y,\
# right_hand.middle.bone_3.prev_joint.z,right_hand.middle.bone_2.direction.x,\
# right_hand.middle.bone_2.direction.y,right_hand.middle.bone_2.direction.z,right_hand.middle.bone_2.center.x,\
# right_hand.middle.bone_2.center.y,right_hand.middle.bone_2.center.z,right_hand.middle.bone_2.next_joint.x,\
# right_hand.middle.bone_2.next_joint.y,right_hand.middle.bone_2.next_joint.z,right_hand.middle.bone_2.width,\
# right_hand.middle.bone_2.length,right_hand.middle.bone_2.prev_joint.x,right_hand.middle.bone_2.prev_joint.y,\
# right_hand.middle.bone_2.prev_joint.z,right_hand.middle.stabilized_tip_position.x,\
# right_hand.middle.stabilized_tip_position.y,right_hand.middle.stabilized_tip_position.z,\
# right_hand.middle.width,right_hand.middle.length,right_hand.middle.tip_position.x,\
# right_hand.middle.tip_position.y,right_hand.middle.tip_position.z,right_hand.middle.tip_velocity.x,\
# right_hand.middle.tip_velocity.y,right_hand.middle.tip_velocity.z,right_hand.grab_strength,right_hand.palm_normal.x,\
# right_hand.palm_normal.y,right_hand.palm_normal.z,right_hand.palm_width,right_hand.palm_velocity.x,\
# right_hand.palm_velocity.y,right_hand.palm_velocity.z,right_hand.sphere_center.x,\
# right_hand.sphere_center.y,right_hand.sphere_center.z,right_hand.ring.direction.x,\
# right_hand.ring.direction.y,right_hand.ring.direction.z,right_hand.ring.bone_1.direction.x,\
# right_hand.ring.bone_1.direction.y,right_hand.ring.bone_1.direction.z,right_hand.ring.bone_1.center.x,\
# right_hand.ring.bone_1.center.y,right_hand.ring.bone_1.center.z,right_hand.ring.bone_1.next_joint.x,\
# right_hand.ring.bone_1.next_joint.y,right_hand.ring.bone_1.next_joint.z,right_hand.ring.bone_1.width,\
# right_hand.ring.bone_1.length,right_hand.ring.bone_1.prev_joint.x,right_hand.ring.bone_1.prev_joint.y,\
# right_hand.ring.bone_1.prev_joint.z,right_hand.ring.bone_0.direction.x,\
# right_hand.ring.bone_0.direction.y,right_hand.ring.bone_0.direction.z,right_hand.ring.bone_0.center.x,\
# right_hand.ring.bone_0.center.y,right_hand.ring.bone_0.center.z,right_hand.ring.bone_0.next_joint.x,\
# right_hand.ring.bone_0.next_joint.y,right_hand.ring.bone_0.next_joint.z,right_hand.ring.bone_0.width,\
# right_hand.ring.bone_0.length,right_hand.ring.bone_0.prev_joint.x,right_hand.ring.bone_0.prev_joint.y,\
# right_hand.ring.bone_0.prev_joint.z,right_hand.ring.bone_3.direction.x,\
# right_hand.ring.bone_3.direction.y,right_hand.ring.bone_3.direction.z,right_hand.ring.bone_3.center.x,\
# right_hand.ring.bone_3.center.y,right_hand.ring.bone_3.center.z,right_hand.ring.bone_3.next_joint.x,\
# right_hand.ring.bone_3.next_joint.y,right_hand.ring.bone_3.next_joint.z,right_hand.ring.bone_3.width,\
# right_hand.ring.bone_3.length,right_hand.ring.bone_3.prev_joint.x,right_hand.ring.bone_3.prev_joint.y,\
# right_hand.ring.bone_3.prev_joint.z,right_hand.ring.bone_2.direction.x,\
# right_hand.ring.bone_2.direction.y,right_hand.ring.bone_2.direction.z,right_hand.ring.bone_2.center.x,\
# right_hand.ring.bone_2.center.y,right_hand.ring.bone_2.center.z,right_hand.ring.bone_2.next_joint.x,\
# right_hand.ring.bone_2.next_joint.y,right_hand.ring.bone_2.next_joint.z,right_hand.ring.bone_2.width,\
# right_hand.ring.bone_2.length,right_hand.ring.bone_2.prev_joint.x,right_hand.ring.bone_2.prev_joint.y,\
# right_hand.ring.bone_2.prev_joint.z,right_hand.ring.stabilized_tip_position.x,\
# right_hand.ring.stabilized_tip_position.y,right_hand.ring.stabilized_tip_position.z,\
# right_hand.ring.width,right_hand.ring.length,right_hand.ring.tip_position.x,\
# right_hand.ring.tip_position.y,right_hand.ring.tip_position.z,right_hand.ring.tip_velocity.x,\
# right_hand.ring.tip_velocity.y,right_hand.ring.tip_velocity.z,utc,name,gesture\n"


	# for line in lines:
	# 	first = True
	# 	aux = ''
	# 	i = 1
	# 	while i < len(line):
	# 		if line[i] == ':':
	# 			i += 1
	# 			if line[i] == '\"':
	# 				aux += line[i]
	# 				i += 1
	# 				while line[i] != '\"':
	# 					aux += line[i]
	# 					i += 1
	# 				aux += line[i]
	# 				if first:
	# 					first = False
	# 				else:
	# 					f.write(',')
	# 				f.write(aux)
	# 				aux = ''
	# 			elif line[i] == '[':
	# 				i += 1
	# 				while line[i] != ',':
	# 					aux += line[i]
	# 					i += 1
	# 				if first:
	# 					first = False
	# 				else:
	# 					f.write(',')
	# 				f.write(aux)
	# 				aux = ''
	# 				i += 1
	# 				while line[i] != ',':
	# 					aux += line[i]
	# 					i += 1
	# 				f.write(',')
	# 				f.write(aux)
	# 				aux = ''
	# 				i += 1
	# 				while line[i] != ']':
	# 					aux += line[i]
	# 					i += 1
	# 				f.write(',')
	# 				f.write(aux)
	# 				aux = ''
	# 			elif line[i] == '{':
	# 				pass
	# 			else:
	# 				while line[i] != ',' and line[i] != '}':
	# 					aux += line[i]
	# 					i += 1
	# 				if first:
	# 					first = False
	# 				else:
	# 					f.write(',')
	# 				f.write(aux)
	# 				aux = ''
	# 		i += 1
	# 	f.write('\n')