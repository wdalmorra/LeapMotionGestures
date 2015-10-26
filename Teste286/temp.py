import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'LeapSDK/lib/x64' if sys.maxsize > 2**32 else 'LeapSDK/lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path.append('../Libraries/')

import Leap

def main():

	file1 = open('gestures_points_temp.csv','r')
	file2 = open('gestures_points.csv','w')

	for lines in file1:
		line = lines.split()
		classif = line[0]
		x = line[1]
		y = line[2]
		z = line[3]
		palm = Leap.Vector(float(x),float(y),float(z))
		file2.write(classif)
		for i in range(0,5):
			xf = line[4+(i*3)]
			yf = line[5+(i*3)]
			zf = line[6+(i*3)]
			finger = Leap.Vector(float(xf),float(yf),float(zf))
			file2.write(' ' + str(finger - palm))
			# print str(xf - x) + " " + str(yf - y) + " " + str(zf - z)
		file2.write('\n')

	file2.close()



if __name__ == '__main__':
	main()