import sys

def get_points(points, f, last):
	for i in range(0, len(points)):
		point = points[i]
		point = point.replace('(', '')
		point = point.replace(',', '')
		point = point.replace(')', '')
		f.write(point)

		if (not last) or (i < len(points) - 1):
			f.write(' ')

def main(argv):
	first = True
	try:
		f = open(argv[0], 'r')
		lines = f.read().splitlines()
		f.close()
	except Exception, e:
		print e

	try:
		f = open(argv[1], 'w')

		for line in lines:
			if line.startswith('Frame'):
				if first:
					# f.write('[')
					first = False
				else:
					# f.write(']\n[')
					f.write('\n')
			elif line.startswith('typeOfHand'):
				line = line.split(':')
				line = line[1].split(' ')
				get_points(line[1:], f, False)
			elif line.startswith('Thumb'):
				line = line.split(':')
				line = line[1].split(' ')
				get_points(line[1:], f, False)
			elif line.startswith('Forefinger'):
				line = line.split(':')
				line = line[1].split(' ')
				get_points(line[1:], f, False)
			elif line.startswith('Middle'):
				line = line.split(':')
				line = line[1].split(' ')
				get_points(line[1:], f, False)
			elif line.startswith('Ring'):
				line = line.split(':')
				line = line[1].split(' ')
				get_points(line[1:], f, False)
			elif line.startswith('Little'):
				line = line.split(':')
				line = line[1].split(' ')
				get_points(line[1:], f, True)
			# elif line.startswith('palmPosition'):
			# 	continue
			# if line == 'Initialized':
			# 	continue
			# elif line == 'Connected':
			# 	continue
			# elif line.startswith('Press'):
			# 	continue
			# elif line == '':
			# 	continue
			else:
				continue

		# f.write(']\n')
		f.write('\n')

		f.close()


	except Exception, e1:
		print e1



if __name__ == '__main__':
	main(sys.argv[1:])