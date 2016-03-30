#!/bin/bash

list='SVM_test.py Bernoulli_NB_test.py Decision_Tree_test.py Gaussian_NB_test.py KNeighbors_test.py OneVsOne_test.py OneVsRest_test.py'

echo "TEST SIZE: 40%"
for i in $list; do
	echo $i
    python $i project gestures
    echo ""
done