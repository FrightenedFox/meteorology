import pandas as pd, numpy as np

class Data():
	names = ['M', 'D', 'H', 'DBT', 'RH', 'HR', 'WS', 'WD', 'ITH', 'IDH', 'ISH', 'TSKY', 'N_0', 
		'N_30', 'NE_30', 'E_30', 'SE_30', 'S_30', 'SW_30', 'W_30', 'NW_30',
		'N_45', 'NE_45', 'E_45', 'SE_45', 'S_45', 'SW_45', 'W_45', 'NW_45',
		'N_60', 'NE_60', 'E_60', 'SE_60', 'S_60', 'SW_60', 'W_60', 'NW_60',
		'N_90', 'NE_90', 'E_90', 'SE_90', 'S_90', 'SW_90', 'W_90', 'NW_90']

	def __init__(self, path):
		self.dFrame = pd.read_table(path,
			delimiter = ' ', names = self.names, skipinitialspace = True, index_col = 0)

	def day(self, number):
		n = 24
		tail, head = n*(number-1), n*number
		return self.dFrame.iloc[tail:head]

	def week(self, number):
		n = 168 	# 24 * 7 = 168
		tail, head = n*(number-1), n*number
		return self.dFrame.iloc[tail:head]

	def month(self, number):
		return self.dFrame[ self.dFrame['M'] == number ]

	def season(self, number):
		if type(number)==str:
			number = number.lower()
		season_dict = { 'winter':[12, 1, 2], 1:[12, 1, 2],
						'spring':[ 3, 4, 5], 2:[ 3, 4, 5],
						'summer':[ 6, 7, 8], 3:[ 6, 7, 8],
						'autumn':[ 9,10,11], 4:[ 9,10,11]}
		a, b, c = season_dict[number][0], season_dict[number][1], season_dict[number][2]
		key = np.logical_or(np.logical_or(self.dFrame['M'] == a,self.dFrame['M'] == b),self.dFrame['M'] == c)
		return self.dFrame[key]


def program_prototype(d_type, t_interval):
	
	pass

path = '.\\Data\\bialystok.txt'

bialystok = Data(path)
# print(bialystok.dFrame)
# print(bialystok.week(10))
# print(bialystok.month(10))
# print(bialystok.day(32))
print(bialystok.season(4))