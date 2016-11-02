#takes the passed filename from folder 'DATA/' as the original data source for parsing'

# for class level data selection : input 1
# for fold level data selection : input 2
# for superfamily level data selection : input 3
# for family level data selection : input 4


import sys
import random
import pickle
import numpy as np

def astral_split():
	version1 = 'astral-scope-95-2.05.fa'
	version2 = 'astral-scope-95-2.06.fa'

	data1 = parseSeq(version1)
	data2= parseSeq(version2)
	
	tot_count1 = [len(x) for x in data1.items()]
	tot_count2 = [len(x) for x in data2.items()]
	
	test = {}
	seq_count =0
	for label in data2:
		temp = data2[label]
		if label in data1:
			#print data2[label]
			#print
			#print data1[label]
			#raw_input()
			diff = list( set(data2[label]) - set(data1[label]))
			
			if len(diff)>0:
				test[label] = diff	
				seq_count+= len(diff)
				#print data2[label]
				#print
				#print data1[label]
				#raw_input()
			
				#print diff
				#print
		else:
			test[label] = temp
			seq_count+= len(temp)
	
	print 'train data set contains ',len(data1.keys()) , ' keys and ',sum(tot_count1),' sequences'
	print 'test data set contains ',len(test.keys()) , ' keys and ',seq_count,' sequences'
	print 'astral new data set contains ',len(data2.keys()) , ' keys and ',sum(tot_count2),' sequences'

	f=open('../Data/astral_test','wb')	#difference set between the two versions
	pickle.dump(test,f)
	f.close()

	f=open('../Data/astral_train','wb')	#version 2.05 of Astral
	pickle.dump(data1,f)
	f.close()

def loadTrain(option):
	version1 = 'astral-scope-95-2.05.fa'
	
	data1 = parseSeq(version1)	#data1 is a dict with key = family id (eg.g.1.1.1) and value = list of sequences
	
	X = []
	Y = []

	for key in data1:
		seq = data1[key]
		label = ''	
		if option == 1:
			label = key[0]
		elif option == 2:
			r = key.find('.',2);
			label = key[0:r]
		elif option == 3:
			r = key.rfind('.')
			label = key[0:r]
		elif option == 4 :
			label = key	
	
		for s in seq:
			X.append(s)
			Y.append(label)

	print 'train data set contains ',len(data1.keys()) , ' keys and ',len(X),' sequences'
	return np.array(X),np.array(Y)
	
	

def loadAstral(option):
	f=open('../Data/astral_test','rb')	#difference set between the two versions
	test = pickle.load(f)
	f.close()

	f=open('../Data/astral_train','rb')	#version 2.05 of Astral
	train = pickle.load(f)
	f.close()	
	
	corpus = {}

	for key in train:
		label = ''	
		if option == 1:
			label = key[0]
		elif option == 2:
			r = key.find('.',2);
			label = key[0:r]
		elif option == 3:
			r = key.rfind('.')
			label = key[0:r]
		elif option == 4 :
			label = key

		if label in corpus:
			text = ''.join(train[key])
			corpus[label] += text
		else:
			text = ''.join(train[key])
			corpus[label] = text
		
	return corpus,test

def parseSeq(fname):
	'''
		parses the given file ans returns a dictionary of (family id,sequence list) 
	'''
	f = open('../Data/'+fname,'r')
	data = f.readlines()
	label = ''

	parsedSeq = {}

	seq = ''
	for line in data:
		
    		if line[0]=='>':
			if seq != '':
				if label not in parsedSeq:
					parsedSeq[label] = [seq]
				else:
					parsedSeq[label].append(seq)
				seq = ''

        		words = line.split(' ')
			label = words[1]
		else:
			seq+= line.strip()
		
        return parsedSeq	



def writeData(train,test,option):
	"""
	This function stores the raw data in the form of binary files in Data/Folder 
	corresponding to the option given by user
	Format is list sequence of lists [[label,sequence],[label,sequence]...]
	-- train file is created separately for each label
	-- test file is created combining all labels 
	"""

	FOLDER = '../Data/'
	if option == 1:
		FOLDER+='Class/'
	elif option == 2:
		FOLDER+='Fold/'
	elif option == 3:
		FOLDER+='Superfamily/'
	elif option == 4:
		FOLDER+='Family/'

	
	testData = []
	
	for key in train.keys():
		trainData = []
		temp1 = train[key]
		temp2 = test[key]

		for line in temp1:
			trainData.append([key,line])
		for line in temp2:
			testData.append([key,line])
	
		f1=open(FOLDER+key+'_train','wb')
		pickle.dump(trainData,f1)
		f1.close()


	f2=open(FOLDER+'test','wb')	
	pickle.dump(testData,f2)
	f2.close()
	
	print 'Test/ Train data successfully written in binary files..'
	

if __name__ == '__main__':
	astral_split()
