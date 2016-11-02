from select_data import *
from confmatrix import *
from classify import *
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.cross_validation import train_test_split

def get_input():
	print 'Enter the level in heirarchy (1: class, 2: fold, 3:superfamily, 4: family) : '
	option = int(raw_input())
		
	while option not in range(1,5):
		print 'Invalid input option : class 1 fold 2 superfamily 3 family 4 exit -1'
		print 'Enter value : '
		option = int(raw_input())
		if option == -1:
			return
	return option

		
if __name__ == '__main__':
	#astral_split()      #Run it once to get the astral difference set
	''' The following is to run the classifier on the astral difference set
	'''
	#option=get_input()
	#corpus,test =loadAstral(option)
	#testClassifier(corpus,test)
	#perfMeasures()

	'''The following is to do 10 fold cross validation on the training data to find alpha
	'''


	X,Y =loadTrain(2)	#option = 2 is passed to use fold id as label from key such as g.1.1.1
	kf = KFold(len(X),n_folds = 2)

	run =1
	for train,val in [(1,1)] : #0 kf:
		#x_train = X[train]
		#y_train = Y[train]

		#x_val = X[val]
		#y_val = Y[val]
		x_train, x_val, y_train, y_val = train_test_split(X, Y, test_size=0.2, random_state=42)
		corpus ={}
		test = []		
		for i in range(len(x_train)):
			label = y_train[i]
			if label in corpus:
				corpus[label]+= str(x_train[i])
			else:
				corpus[label] = str(x_train[i])

		for i in range(len(x_val)):
			label = y_val[i]
			test.append((label,x_val[i]))

		testClassifier(corpus,test,run)
		run+=1
