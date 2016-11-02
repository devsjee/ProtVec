import pickle
import math
import copy
import os

FOLDER = ''



DLG_stored = []
freq_total = {}
freq = dict()
corpus = ''
corpus_total = {}
test = ''
X = 0
DL = 0

def load_freq(corpus):
	global freq_total 
	for family in corpus:
		
		data =  corpus[family]
		
		n = 1
		ngrams_dict = dict()
		for j in range(len(data) - n + 1):
        		temp = data[j:j + n]
			if temp in ngrams_dict:
				ngrams_dict[temp] +=1
			else:
				ngrams_dict[temp] =1

		freq_total[family] = ngrams_dict
	
		
def load_corpus(corpus):
	global corpus_total
	corpus_total= corpus	

def load_data(family,test):
	global freq,freq_total,corpus,corpus_total,X

	freq = freq_total[family]
	corpus = corpus_total[family]
	X = len(corpus)

def corpusDL():
    global freq

    total =0
    for key,value in freq.iteritems():
	total += value * (math.log(value,2) - math.log(X,2))
    total = -1*total
    return total


'''def occurrences(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count
'''

def occurrences(sentence,substring):
    return sentence.count(substring)

def DLG(s):
	global freq,corpus,X

	suffix = len(s)
	cs = occurrences(corpus,s)
	n = X - cs*suffix + cs + suffix + 1
	total =0
	for key,value in freq.iteritems():
		csx = occurrences(s,key)
   		#print '{} occurs {} times in {}'.format(key,csx,s)
		cx = value - cs*csx + csx
		#print 'cs '+str(cs)+ ' value ' +str(value)+' cx '+str(cx)+' csx '+str(csx)+' n '+str(n)
		total += cx * (math.log((cx/(1.0*n)),2))
		
	total += cs* (math.log(cs,2) - math.log(n,2))
	total = -1*total
    
	dlg = (DL - total)/cs
    	#print 'DLG of {} is {}'.format(s,dlg)
   
	return dlg  

def OpSeg(U):
	global corpus
	n = len(U)
	OS = []
	DLG_stored = []
	for k in range(0,n):
		if k>30:
			OS[k-30][:]=[]

		OS.append([])

		if k>0:
            		OS[k][:]= []
	    		OS[k] = copy.deepcopy(OS[k-1])
	    		OS[k].append(U[k])
		        DLG_stored.append(DLG_stored[k-1])
		else:
			OS[k][:]=[]
		 	OS[k].append(U[k])
	    		DLG_stored.append(0)


		'''print 'k value is ',k
		print 'OS is ', OS
		print 'DLG stored is ',DLG_stored'''

		for j in range(k,-1,-1):
			if j < k-25:
	        		break
			ngram = U[j:k+1]
            #print ngram
			if occurrences(corpus,ngram)<2:
            #print 'breaking\n'
				break
			if len(ngram) == 1 :
				dlgain = DLG_stored[j-1]
			if j>0:
				dlgain = DLG_stored[j-1] + DLG(ngram)
			else:
				dlgain = DLG(ngram)

			'''print DLG_stored
			print 'new DL', dlgain
	            	print 'DLG_stored is ',DLG_stored[k]'''
			if (dlgain >DLG_stored[k]) and j>0:
				OS[k][:] = []
				OS[k] = copy.deepcopy(OS[j-1])
				OS[k].append(ngram)
				#print 'OS[{}] is now assigned {}'.format(k,OS[k])
				DLG_stored[k] = copy.deepcopy(dlgain)
			elif (dlgain> DLG_stored[k]) and j==0:
				OS[k][:]=[]
				OS[k].append(ngram)
				DLG_stored[k] = copy.deepcopy(dlgain)
		                #print 'OS[{}] is now assigned {}'.format(k,OS[k])

	#print 'n =',str(n),'	len of DLG_STORED ',len(DLG_stored)		 
	return OS[n-1],DLG_stored[n-1]


  


def process_test(test):

	testData = []

	for key in test:
		for seq in test[key]:
			r = key.find('.',2);
			label = key[0:r]
			testData.append((label,seq))
			
	return testData


def testClassifier(corpus,test,run):
	global  DL, freq
	

	FOLDER = '../Data/OUTPUTS/Run'+str(run)


	load_freq(corpus)
	load_corpus(corpus)


	#test_list = process_test(test)
	test_list = test

	predictions = []
	print 'Length of test list is ',str(len(test_list))

	correct = 0
	total = 0
	pred_total = 0
	if not os.path.exists(FOLDER):
		os.mkdir(FOLDER)
	
	fout = open( FOLDER+'/output.txt','w') 
	feature = {} # open(FOLDER+'/feature','wb')
	

	#feature.write('True fold')
	#for family in corpus:
	#	feature.write(family+'\t')
	
	for item in test_list:
		test_case = item[0]
		test = item[1]
		#print test_case
		max_compression = -1000
		label = ''
		total +=1
		fout.write('\n'+test_case+'\t'+test)
		
		temp = []
		feature_vec ={} #'\n'+test_case+'\t'
		for family in corpus:
			
			load_data(family,test)
			
			#print 'len of corpus ',family,' ',str(X)
	
			DL = corpusDL()
			#print 'DL is ',str(DL)

			output,compression = OpSeg(test)
			#print output
			fout.write('\n'+family+' gives following output\n')
			for i in range(len(output)):
				#f.write("[")
				fout.write(output[i]+ ', ')
				#f.write("] ")
			fout.write('\nCompression '+str(compression))
			#print 'Class ',str(family),'  compression ',str(compression)
			if compression > max_compression:
				max_compression = compression
				label = family
			
	
			temp.append(compression)
			if compression >0.0:
				feature_vec[family] = compression
		#feature_vec+=label

		if temp.count(max_compression) > 1:
			label = 'U'
		else:
			pred_total+=1
		#print 'Predicted : '+str(label)+'	Actual : '+test_case
		print  total
		if test_case == label:
			correct+=1.0
		predictions.append([test_case,label])
		print 'Actual ',test_case, '  Predicted ',label

		feature[(test_case,test)]=feature_vec
	#feature.close()
	fout.close()	
	print 'Test Total: ',str(total),' Correct : ',str(correct),'Pred Total: ',str(pred_total),' Precision is ',str((correct/pred_total)*100)
	
	
	ff1 = open(FOLDER+'/predictions','w')
	ff1.write('Actual\t Predicted\n')
	for item in predictions:
		ff1.write(item[0]+'\t'+item[1]+'\n')
	ff1.close()
	
	f = open(FOLDER+'/features','wb')
	pickle.dump(feature,f)
	f.close()
#if __name__ == '__main__':
#	testClassifier(1,'r')


#unique.keys()[i]+ ' ' + unique.values()[i]+ '\n')



