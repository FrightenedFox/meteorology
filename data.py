def read_file(path):
	''' This function reads the given file line by line and returns an MxN matrix,
	where M - the number of lines and N - the number of columns in the file'''
	with open(path, mode='r') as file:
		data_matrix= []
		for line in file:
			data_row = []
			for record in line.split():
				data_row.append(float(record))
			data_matrix.append(data_row)
	return data_matrix


class Database(object):
	"""docstring for Database"""
	def __init__(self, source_file):
		super(Database, self).__init__()
		self.source_file = source_file
		self.mHours = read_file(source_file)
		self.season_dict = { 0:0, 1:0, 2:1, 3:1, 4:1, 5:2, 6:2, 7:2, 8:3, 9:3, 10:3, 11:0}
		self.distribute_data(self.mHours)


	def distribute_data(self, data, day_index=2, month_index=1):

		mDays, mWeeks, mMonths, mSeasons = [],[],[],[[] for i in range(4)]
		week_number, hour_in_week = -1, 168
		day_number, month_number = -1, -1
		previous_day, previous_month = None, None
		december_counter = 0

		for record in data:

			if record[day_index] == previous_day:
				mDays[day_number].append(record)
			else:
				previous_day = record[day_index]
				day_number += 1
				mDays.append([])
				mDays[day_number].append(record)


			if hour_in_week < 168:
				mWeeks[week_number].append(record)
				hour_in_week += 1
			else:
				hour_in_week = 1
				week_number += 1
				mWeeks.append([])
				mWeeks[week_number].append(record)


			if record[month_index] == previous_month:
				mMonths[month_number].append(record)
			else:
				previous_month = record[month_index]
				month_number +=1
				mMonths.append([])
				mMonths[month_number].append(record)


			if month_number == 11:
				mSeasons[0].insert(december_counter, record)
				december_counter += 1
			else:
				mSeasons[self.season_dict[month_number]].append(record)

		self.mDays, self.mWeeks, self.mMonths, self.mSeasons = mDays, mWeeks, mMonths, mSeasons



# o = Database('.\\Data\\bialystok.txt')
# for i in range(0, 4):
# 	for j in range(0, 24, 6):
# 		print(o.mSeasons[i][j][:4])