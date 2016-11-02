
compute_measures(keys,tp,tn,fp,fn):
tpsum=0
tnsum=0
fpsum =0
fnsum=0

precision_count =0
recall_count =0
specif_count =0

macro_precision=0
macro_recall =0
macro_specificity =0

for key in keys:
	tp1 = tp.get(key,0)
	tn1 = tn.get(key,0)
	fp1 = fp.get(key,0)
	fn1 = fn.get(key,0)

	tpsum += tp1
	tnsum += tn1
	fpsum += fp1
	fnsum += fn1

	if tp1 >0 or fp1>0:
		macro_precision += (tp1*1.0)/(tp1+fp1)
		precision_count+=1
	if tp1 >0 or fn1> 0:
		macro_recall += (tp1*1.0)/(tp1+fn1)
		recall_count +=1
	if fp1>0 or tn1>0:
		macro_specificity += (tn1*1.0)/(fp1+tn1)
		specif_count +=1

print 'Micro MEasures are '
print 'Precision = ', tpsum*1.0/(tpsum+fpsum)
print 'Recall = ', tpsum*1.0/(tpsum+fnsum)
print 'Specificity = ', tnsum*1.0/(fpsum+tnsum)


print 'Macro MEasures are '
print 'Precision = ', macro_precision*1.0/precision_count
print 'Recall = ', macro_recall*1.0/recall_count
print 'Specificity = ', macro_specificity*1.0/specif_count
