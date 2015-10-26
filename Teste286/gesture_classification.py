import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = 'LeapSDK/lib/x64' if sys.maxsize > 2**32 else 'LeapSDK/lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

from sklearn import svm
from sklearn.metrics import accuracy_score

clf = svm.SVC(kernel = 'linear', C = 1.0)

X = []
Y = []

def read_file(file1):
	lines = file1.read().splitlines()
	for i in range(0,221):
		line = lines[i].split()
		tmp = []
		classif = line[0]
		for x in line[1:]:
			tmp.append(float(x))
		X.append(tmp)
		Y.append(classif)
			

def learning():

	# Defining samples and classifications
	gestures = open('gestures.csv','r')

	read_file(gestures)

	print "Fitting"
	clf.fit(X,Y)
	print "Fitting done"

def testing():

	Y_pred = []
	Y_true = []

	test_file = open('gestures.csv')

	lines = test_file.read().splitlines()

	for i in range(221,286):
		print i
		line = lines[i].split()
		tmp = []
		classif = line[0]
		for x in line[1:]:
			tmp.append(float(x))

		print "Predicted: " + str(clf.predict(tmp))
		print "Should be: " + classif

		Y_pred.append(clf.predict(tmp)[0])
		Y_true.append(classif)

	print accuracy_score(Y_true, Y_pred, normalize=False)



def main():

	learning()
	testing()



if __name__ == '__main__':
	main()
	
	