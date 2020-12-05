import assistant as assist
class Hour(object):
	"""docstring for Hour"""
	def __init__(self, source_file):
		super(Hour, self).__init__()
		self.source_file = source_file
		self.mhours = assist.read_file(source_file)
		self.mdays = self.distribute_data(self.mhours, index=2)
		self.mmonths = self.distribute_data(self.mhours, index=1)

	def distribute_data(self, data, index):
		previous, result_mx = data[0][index], [[]]
		i = 0
		for record in data:
			if previous == record[index]:
				result_mx[i].append(record)
			else:
				result_mx.append([])
				i+=1
			previous = record[index]
		return result_mx


obj_1 = Hour('.\\Data\\bialystok.txt')
print(obj_1.mdays[0][21][12])
print(obj_1.mmonths[0][53][12])