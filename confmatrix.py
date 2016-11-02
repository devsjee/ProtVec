import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support


def read_data(FNAME):
	y_test = []
	y_pred = []
	f = open(FNAME,'r')
	data = f.readlines()
	for i in range(1,len(data)):
		temp = data[i].strip().split('\t')
		if temp[1] =='U':
			continue
		y_test.append(temp[0])
		y_pred.append(temp[1])

	return y_test,y_pred

def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(4)
    plt.xticks(tick_marks, ['a','b','c','d'], rotation=45)
    plt.yticks(tick_marks,  ['a','b','c','d'])
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def perfMeasures():
	FOLDER = '../Data/OUTPUTS/predictions'

	# Compute confusion matrix
	y_test,y_pred = read_data(FOLDER)
	cm = confusion_matrix(y_test, y_pred)
	np.set_printoptions(precision=2)
	print('Confusion matrix, without normalization')
	print(cm)
	plt.figure()
	plot_confusion_matrix(cm)

	# Normalize the confusion matrix by row (i.e by the number of samples
	# in each class)
	cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
	print('Normalized confusion matrix')
	print(cm_normalized)
	plt.figure()
	plot_confusion_matrix(cm_normalized, title='Normalized confusion matrix')

	##### other measures ########
	correct = 0
	total = 0
	tp={}
	fp={}
	fn={}
	
	n = len(cm)

	for actual in range(n):
		for predicted in range(n):
			if actual == predicted:
				tp[actual] = cm[actual][predicted]
				correct+=tp[actual]
				total+=tp[actual]
			else:
				fn[actual] = fn.get(actual,0)+cm[actual][predicted]
				fp[predicted] = fp.get(predicted,0) + cm[actual][predicted]
				total+=cm[actual][predicted]
				


	#Accuracy#
	print 'Number of  correct classifications ', str(correct)
	print 'total number of classifications ', str(total)
	print 'Accuracy (%) ',str(correct*100.0/total)
	
	print 
	#print '####### Class Specific Precision and Recall #######'
	#for key in tp.keys():
	#	print key,'\t',str(tp[key]*100/(tp[key]+fp[key])),'\t',str(tp[key]*100/(tp[key]+fn[key]))
	
	#plt.show()		
	precision,recall,fscore,support = precision_recall_fscore_support(y_test, y_pred)
	print precision
	print 
	print recall
	print
	print fscore
	print
	print support

	print 'Total number of folds ',len(precision)

	prec1 = [x>=1 for x in precision]
	print 'Number of folds with precision =1 ', sum(prec1)

	rec1 = [x>=1 for x in recall]
	print 'Number of folds with recall =1 ', sum(rec1)
	
	fsc1 = [x>=1 for x in fscore]
	print 'Number of folds with fscore =1 ', sum(fsc1)


if __name__ == '__main__':
	perfMeasures()
