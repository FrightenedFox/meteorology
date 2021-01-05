import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf

class Data():
	names = ['M', 'D', 'H', 
		'DBT', 'RH', 'HR', 'WS', 'WD', 'ITH', 'IDH', 'ISH', 'TSKY', 'N_0', 
		'N_30', 'NE_30', 'E_30', 'SE_30', 'S_30', 'SW_30', 'W_30', 'NW_30',
		'N_45', 'NE_45', 'E_45', 'SE_45', 'S_45', 'SW_45', 'W_45', 'NW_45',
		'N_60', 'NE_60', 'E_60', 'SE_60', 'S_60', 'SW_60', 'W_60', 'NW_60',
		'N_90', 'NE_90', 'E_90', 'SE_90', 'S_90', 'SW_90', 'W_90', 'NW_90']

	def __init__(self, path, year = 2013):
		self.dFrame = pd.read_table(path,
			delimiter = ' ', names = self.names, skipinitialspace = True, index_col = 0)
		self.dFrame.insert(loc = 0, column ='Y', value = year)
		date = self.dFrame[['Y','M','D','H']].rename(columns={'Y': 'year', 'M':'month', 'D':'day','H':'hour'})
		self.dFrame.insert(loc = 0, column ='Date', value = pd.to_datetime(date))
		self.dFrame.set_index('Date', drop = True, inplace=True)
		del date

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
		return self.dFrame[self.dFrame['M'].isin(season_dict[number])]

	def get_frame(self, d_type = None, t_interval = 'all', intr_number = 365):
		types = {	'all' 	: self.dFrame,
					'day' 	: self.day(min(intr_number, 366)),
					'week' 	: self.week(min(intr_number, 53)),
					'month'	: self.month(min(intr_number, 12)),
					'season': self.season(min(intr_number, 4))}
		if d_type == None:
			return types[t_interval]
		else:
			return types[t_interval][d_type]

	def stats(self, d_type = 'DBT', t_interval = 'all', intr_number = 365):
		stats_list = [np.min, np.max, np.mean, np.median, np.std, np.var]
		return self.get_frame(d_type, t_interval, intr_number).agg(stats_list)

	def corr(self, x, y):
		s_x = self.dFrame[x].diff()
		s_y = self.dFrame[y].diff()
		plt.scatter(s_x, s_y, s = 2)
		plt.show()
		plt.close()

	def autocorr(self, x, max_lag = 40):
		corr_list=[]
		max_lag+=1
		for lag in range(max_lag):
			corr_list.append(self.dFrame[x].autocorr(lag))
		x_ax = np.linspace(1,max_lag,max_lag)
		plt.plot([-2, max_lag+2], [0,0])
		plt.xlim((-2,max_lag+2))
		plt.scatter(x_ax, corr_list, s=20)
		plot_acf(self.dFrame[x], lags = max_lag-1)
		plt.show()
		plt.close()


path = '.\\Data\\bialystok.txt'
bialystok = Data(path)
bialystok.autocorr('RH')
bialystok.corr('RH', 'DBT')