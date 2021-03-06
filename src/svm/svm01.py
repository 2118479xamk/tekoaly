import pandas 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn import svm

#http://mreed.umtri.umich.edu/mreed/downloads.html
#Male dataset!
#We have preprocessed data set which does not contain missing values nor duplicates
filename1="../../../share/data/ANSUR2_2012/ANSUR II MALE Public.csv"
filename2="../../../share/data/ANSUR2_2012/ANSUR II FEMALE Public.csv"
train_fraction = 0.8
Y_column='Gender'

#Load data
data1=pandas.read_csv(filename1)
data2=pandas.read_csv(filename2)
data=pandas.concat([data1, data2])
del data1, data2
print("Read data shape = "+str(data.shape))
print()

#Remove index column and all text columns
for col in ["SubjectId","Date","Installation","Component","Branch","PrimaryMOS","SubjectsBirthLocation","SubjectNumericRace","Ethnicity","DODRace","WritingPreference","subjectid"]:
    print("Remove "+col)
    data.drop(col, axis=1, inplace=True)
print()

#Replace Male->0, Female->1
print("Convert gender to number")
data['Gender'].replace(['Female','Male'],[0,1],inplace=True)
print("data shape = "+str(data.shape))
print()

#Shufle data set
print("Shufle data")
data=shuffle(data)
print("data shape = "+str(data.shape))
print()

def splitXY(d):
    return d.drop(Y_column, axis=1), d[Y_column] 

print("Split training/test data set")
traindata, testdata = train_test_split(data, test_size=1-train_fraction)
trainX, trainY=splitXY(traindata)
testX, testY=splitXY(testdata)
print()

print("Standardize data")
stdev=trainX.std(axis=0)
mean=trainX.mean(axis=0)
trainX=(trainX-mean)/stdev
testX=(testX-mean)/stdev
print()

#Remove unused datasets
del data, testdata, traindata

print("trainX shape = "+str(trainX.shape))
print("trainY shape = "+str(trainY.shape))
print("testX shape = "+str(testX.shape))
print("testY shape = "+str(testY.shape))
print()

classifier = svm.SVC()
classifier.fit(trainX, trainY)

predY=classifier.predict(testX)

print("Faulty predictions:", (np.abs(testY)-np.abs(predY)).sum())