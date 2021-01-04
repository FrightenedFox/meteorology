def mean(mylist):
	''' doc '''
	return sum(mylist)/len(mylist)

def varience(mylist):
	mymean = mean(mylist)
	for i in range(len(mylist)):
		mylist[i] = pow(mylist[i]-mymean, 2)
	return mean(mylist)

def stand_dev(mylist):
	from math import sqrt
	return sqrt(varience(mylist))

def correlation(xList, yList):
	from math import sqrt
	xMean, yMean = mean(xList), mean(yList)
	aSum, bSum, abSum = 0, 0, 0
	for i in range(len(xList)):
		a, b = xList[i] - xMean, yList[i] - yMean
		aSum += pow(a, 2)
		bSum += pow(b, 2)
		abSum += a*b
	return abSum/sqrt(aSum*bSum)



# test = [600,470,170,430,300]
# test_1 = [5, 4, 1, 3, 2]
# test_2 = [1, 2, 5, 3, 4]
# x = [14.2,16.4,11.9,15.2,18.5,22.1,19.4,25.1,23.4,18.1,22.6,17.2]
# y = [215,325,185,332,406,522,412,614,544,421,445,408]
# print(correlation(test, test_2))