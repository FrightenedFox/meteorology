import matplotlib
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib import pyplot as plt
matplotlib.use("TkAgg")
style.use("ggplot")

import tkinter as tk
from tkinter import ttk

import pandas as pd
import numpy as np

import data as dt

CategoriesList = ['DBT', 'RH', 'HR', 'WS', 'WD', 'ITH', 'IDH', 'ISH', 'TSKY']

TimePeriodsDict = {	'all' 	: 'All',
					'day' 	: 'Day',
					'week' 	: 'Week',
					'month'	: 'Month',
					'season': 'Season'}

PlotTypesList = ['Autocorrelation','Correlation', 'Plot Data']

UPDATE_FLAG = True

LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

f = Figure()
a = f.add_subplot(1,1,1)

class MeteorologyApp(tk.Tk):
	"""docstring for MeteorologyApp"""
	def __init__(self, path = '.\\Data\\bialystok.txt', *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.City = dt.WeatherData(path)

		self._category = tk.StringVar()
		self._category.set('DBT')
		self._corr_category = tk.StringVar()
		self._corr_category.set('DBT')
		self._time_period = tk.StringVar()
		self._time_period.set('week')
		self._plot_type = tk.StringVar()
		self._plot_type.set('Autocorrelation')
		self.Min = tk.StringVar()
		self.Min.set('Init-value')
		self.Max = tk.StringVar()
		self.Max.set('Init-value')
		self.Mean = tk.StringVar()
		self.Mean.set('Init-value')
		self.Median = tk.StringVar()
		self.Median.set('Init-value')
		self.Std = tk.StringVar()
		self.Std.set('Init-value')
		self.Var = tk.StringVar()
		self.Var.set('Init-value')

		tk.Tk.iconbitmap(self, default='icon.ico')
		tk.Tk.wm_title(self, " Meteorology")

		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		menubar = tk.Menu(container)
		filemenu = tk.Menu(menubar, tearoff = 0)
		filemenu.add_command(label='Save settings', 
			command = lambda:tk.messagebox.showinfo(title = 'Title', message = 'Under the job.'))
		filemenu.add_separator()
		filemenu.add_command(label = 'Exit', command = quit)
		menubar.add_cascade(label = 'File', menu = filemenu)

		tk.Tk.config(self, menu = menubar)

		self.frames = {}
		for Page in (WarningPage, MainPage):
			frame = Page(container, self)
			self.frames[Page] = frame
			frame.grid(row = 0, column = 0, sticky = 'nsew')
		
		self.show_frame(MainPage)

	def show_frame(self,cont):
		frame = self.frames[cont]
		frame.tkraise()

	def update_stats(self, dFrame):
		stats_list = [np.min, np.max, np.mean, np.median, np.std, np.var]
		stats = dFrame.agg(stats_list)
		self.Min.set(stats['amin'])
		self.Max.set(stats['amax'])
		self.Mean.set(stats['mean'])
		self.Median.set(stats['median'])
		self.Std.set(stats['std'])
		self.Var.set(stats['var'])
		self.update()

	def update_plot(self,i=None):
		a.clear()
		
		dCategory = self._category.get()
		tPeriod = self._time_period.get()
		tPeriod_numb = self.frames[MainPage].Edit_tPeriod_numb.get()
		# Add try
		if tPeriod_numb == '':
			tPeriod_numb = 1
		else:
			tPeriod_numb = int(tPeriod_numb)

		dFrame_unsort = self.City.get_frame(
			d_type = dCategory, 
			t_interval = tPeriod,
			intr_number = tPeriod_numb)
		self.update_stats(dFrame_unsort)
		dFrame = dFrame_unsort.sort_index()
		
		plot_type = self._plot_type.get()
		if plot_type == 'Autocorrelation':
			corr_list=[]
			
			max_lag = self.frames[MainPage].Edit_autoLag.get()
			# Add try
			if max_lag == '':
				max_lag = 40
			else:
				max_lag = int(max_lag)
			for lag in range(max_lag):
				corr_list.append(dFrame.autocorr(lag))
			x_ax = np.linspace(1,max_lag,max_lag)
			a.plot([-2, max_lag+2], [0,0])
			a.scatter(x_ax, corr_list, s=20)

		elif plot_type == 'Correlation':
			tPeriod_numb2 = self.frames[MainPage].Edit_tPeriod2_numb.get()
			# Add try
			if tPeriod_numb2 == '':
				tPeriod_numb2 = 1
			else:
				tPeriod_numb2 = int(tPeriod_numb2)
			dFrame_second_uns = self.City.get_frame(
				d_type = self._corr_category.get(), 
				t_interval = tPeriod,
				intr_number = tPeriod_numb2)
			dFrame_second = dFrame_second_uns.sort_index()
			s_x = dFrame.diff()
			s_y = dFrame_second.diff()
			a.scatter(s_x, s_y, s = 5)
		elif plot_type == 'Plot Data':
			x_ax = np.linspace(1,len(dFrame),len(dFrame))
			a.plot(dFrame.index, dFrame)




class WarningPage(tk.Frame):
	"""docstring for WarningPage"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text="ALPHA version", font=LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		button1 = ttk.Button(self, text = "Agree", 
			command=lambda: controller.show_frame(MainPage))
		button1.pack()

		button2 = ttk.Button(self, text = "Disagree", 
			command=quit)
		button2.pack()

class MainPage(tk.Frame):
	"""docstring for PageOne"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		self.grid_rowconfigure(0, weight = 1)
		self.grid_rowconfigure(1, weight = 2)
		self.grid_rowconfigure(2, weight = 2)
		self.grid_columnconfigure(0, weight = 1)
		self.grid_columnconfigure(1, weight = 2)

		self.CategoryFrame = tk.LabelFrame(self, text = 'Data types')
		self.CategoryFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=5, pady = 5, rowspan=2)
		self.Category()

		self.TimePeriodFrame = tk.LabelFrame(self, text = 'Data types')
		self.TimePeriodFrame.grid(row = 2, column = 0, sticky = 'nsew', padx=5, pady = 5)
		self.TimePeriod()

		self.StatisticsFrame = tk.Frame(self)
		self.StatisticsFrame.grid(row = 1, column = 1, sticky = 'nsew', rowspan = 2)
		self.Statistics()

		self.ButtonsFrame = tk.Frame(self)
		self.ButtonsFrame.grid(row = 0, column = 1, sticky = 'nsew')
		self.Buttons()

		self.PlotFrame = tk.Frame(self)
		self.PlotFrame.grid(row = 1, column = 1, sticky = 'nsew', rowspan = 2)
		self.Plot()

		self.PlotOptionsFrame = tk.LabelFrame(self.PlotFrame, text = 'Options')
		self.PlotOptionsFrame.grid(row = 0, column = 0, sticky = 'nsew')
		self.PlotOptions()

		self.PlotOptionsTypeFrame = tk.Frame(self.PlotOptionsFrame)
		self.PlotOptionsTypeFrame.grid(row = 0, column = 0, sticky = 'nsew')
		self.PlotOptionsType()

		self.PlotOptionsAutocorrFrame = tk.Frame(self.PlotOptionsFrame)
		self.PlotOptionsAutocorrFrame.grid(row = 1, column = 0, sticky = 'nsew')
		self.PlotOptionsAutocorr()

		self.PlotOptionsCorrFrame = tk.Frame(self.PlotOptionsFrame)
		self.PlotOptionsCorrFrame.grid(row = 1, column = 0, sticky = 'nsew')
		self.PlotOptionsCorr()

		self.PlotOptionsBlancFrame = tk.Frame(self.PlotOptionsFrame)
		self.PlotOptionsBlancFrame.grid(row = 1, column = 0, sticky = 'nsew')
		self.PlotOptionsBlanc()

		self.PlotGraphFrame = tk.Frame(self.PlotFrame)
		self.PlotGraphFrame.grid(row = 0, column = 1, sticky = 'nsew')
		self.PlotGraph()

		self.TypesFrames = {'Autocorrelation'	:self.PlotOptionsAutocorrFrame,
							'Correlation'		:self.PlotOptionsCorrFrame,
							'Plot Data'			:self.PlotOptionsBlancFrame}

		self.PlotOptionsAutocorrFrame.tkraise()
		self.StatisticsFrame.tkraise()


	def Category(self):
		Label = tk.Label(self.CategoryFrame, text="Choose the data\nyou are interested in:", font=LARGE_FONT)
		Label.pack(pady = 10, padx = 10)

		for cType in CategoriesList:
			tk.Radiobutton(self.CategoryFrame, text=cType, font = NORMAL_FONT,
				variable=self.controller._category, value=cType).pack()

	def TimePeriod(self):	
		label = tk.Label(self.TimePeriodFrame, text="Choose the time period\nyou are interested in:", font=LARGE_FONT)
		label.pack(pady = 10, padx = 10)	

		for pType, pLabel in TimePeriodsDict.items():
			tk.Radiobutton(self.TimePeriodFrame, text=pLabel, font = NORMAL_FONT,
				variable=self.controller._time_period, value=pType).pack()

		# Improve
		l_text = "\nSpecify the number of the {}".format(self.controller._time_period.get())
		label2 = tk.Label(self.TimePeriodFrame, text=l_text, font=LARGE_FONT)
		label2.pack(pady = 10, padx = 10)	

		self.Edit_tPeriod_numb = tk.Entry(self.TimePeriodFrame, width = 3)
		self.Edit_tPeriod_numb.pack()
		self.Edit_tPeriod_numb.insert(0, "1")

	def Buttons(self):
		self.ButtonsFrame.grid_columnconfigure(0, weight=1)
		self.ButtonsFrame.grid_columnconfigure(1, weight=1)
		self.ButtonsFrame.grid_rowconfigure(0, weight=1)

		StatButton = tk.Button(self.ButtonsFrame, text = "Statistics", font = LARGE_FONT,
			command = lambda:self.StatisticsFrame.tkraise())
		StatButton.grid(row = 0, column = 0, sticky = 'nsew', padx=5, pady = 5)

		PlotButton = tk.Button(self.ButtonsFrame, text = "Plot", font = LARGE_FONT,
			command = lambda:self.PlotFrame.tkraise())
		PlotButton.grid(row = 0, column = 1, sticky = 'nsew', padx=5, pady = 5)	

	def Plot(self):
		self.PlotFrame.grid_rowconfigure(0, weight = 1)
		self.PlotFrame.grid_columnconfigure(0, weight = 1)
		self.PlotFrame.grid_columnconfigure(1, weight = 2)

	def Statistics(self):
		self.StatisticsFrame.grid_columnconfigure(0, weight = 1)
		self.StatisticsFrame.grid_columnconfigure(1, weight = 1)
		self.StatisticsFrame.grid_columnconfigure(2, weight = 1)
		self.StatisticsFrame.grid_columnconfigure(3, weight = 1)

		self.StatisticsFrame.grid_rowconfigure(0, weight = 1)
		self.StatisticsFrame.grid_rowconfigure(1, weight = 1)
		self.StatisticsFrame.grid_rowconfigure(2, weight = 1)

		min_label = tk.Label(self.StatisticsFrame, text="Min: ", font=LARGE_FONT)
		min_label.grid(row = 0, column = 0, sticky = 'nsew')
		min_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Min, font=LARGE_FONT)
		min_ans.grid(row = 0, column = 1, sticky = 'nsew')
		max_label = tk.Label(self.StatisticsFrame, text="Max: ", font=LARGE_FONT)
		max_label.grid(row = 0, column = 2, sticky = 'nsew')
		max_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Max, font=LARGE_FONT)
		max_ans.grid(row = 0, column = 3, sticky = 'nsew')
		mean_label = tk.Label(self.StatisticsFrame, text="Mean: ", font=LARGE_FONT)
		mean_label.grid(row = 1, column = 0, sticky = 'nsew')
		mean_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Mean, font=LARGE_FONT)
		mean_ans.grid(row = 1, column = 1, sticky = 'nsew')
		median_label = tk.Label(self.StatisticsFrame, text="Median: ", font=LARGE_FONT)
		median_label.grid(row = 1, column = 2, sticky = 'nsew')
		median_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Median, font=LARGE_FONT)
		median_ans.grid(row = 1, column = 3, sticky = 'nsew')
		std_label = tk.Label(self.StatisticsFrame, text="Standart deviation: ", font=LARGE_FONT)
		std_label.grid(row = 2, column = 0, sticky = 'nsew')
		std_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Std, font=LARGE_FONT)
		std_ans.grid(row = 2, column = 1, sticky = 'nsew')
		varience_label = tk.Label(self.StatisticsFrame, text="Variance: ", font=LARGE_FONT)
		varience_label.grid(row = 2, column = 2, sticky = 'nsew')
		varience_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Var, font=LARGE_FONT)
		varience_ans.grid(row = 2, column = 3, sticky = 'nsew')

	def PlotOptions(self):
		self.PlotOptionsFrame.grid_rowconfigure(0, weight = 1)
		self.PlotOptionsFrame.grid_rowconfigure(1, weight = 1)
		self.PlotOptionsFrame.grid_columnconfigure(0, weight = 1)

	def PlotOptionsType(self):
		self.PlotOptionsTypeFrame.grid_rowconfigure(0, weight = 1)
		self.PlotOptionsTypeFrame.grid_rowconfigure(1, weight = 1)
		self.PlotOptionsTypeFrame.grid_rowconfigure(2, weight = 1)
		self.PlotOptionsTypeFrame.grid_columnconfigure(0, weight = 1)
		
		for index, pType in enumerate(PlotTypesList):
			tk.Radiobutton(self.PlotOptionsTypeFrame, text=pType, font = LARGE_FONT,
				variable=self.controller._plot_type, value=pType,
				command = lambda:	self.TypesFrames[self.controller._plot_type.get()].tkraise()
				).grid(row = index, column = 0, 
				sticky = 'nsew', padx=5, pady = 5)

	def PlotOptionsAutocorr(self):
		l_text = "\nSpecify the number of the lags"
		label1 = tk.Label(self.PlotOptionsAutocorrFrame, text=l_text, font=LARGE_FONT)
		label1.pack(pady = 10, padx = 10)	

		self.Edit_autoLag = tk.Entry(self.PlotOptionsAutocorrFrame, width = 8)
		self.Edit_autoLag.pack()
		self.Edit_autoLag.insert(0, "40")

	def PlotOptionsCorr(self):
		for index, cType in enumerate(CategoriesList):
			tk.Radiobutton(self.PlotOptionsCorrFrame, text=cType, font = NORMAL_FONT,
				variable=self.controller._corr_category, value=cType).grid(row = index, column = 0, 
				sticky = 'nsew', padx=5, pady = 5)

		# improve update
		l_text2 = "\nSpecify the number of the periods {}".format(self.controller._time_period.get())
		label2 = tk.Label(self.PlotOptionsCorrFrame, text=l_text2, font=LARGE_FONT)
		label2.grid(row = len(CategoriesList), column = 0, sticky = 'nsew', padx=5, pady = 5)

		self.Edit_tPeriod2_numb = tk.Entry(self.PlotOptionsCorrFrame, width = 4)
		self.Edit_tPeriod2_numb.grid(row = len(CategoriesList)+1, column = 0, sticky = 'nsew', padx=5, pady = 5)
		self.Edit_tPeriod2_numb.insert(0, "1")

	def PlotOptionsBlanc(self):
		pass

	def PlotGraph(self):
		canvas = FigureCanvasTkAgg(f, self.PlotGraphFrame)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady = 5)

		toolbar = NavigationToolbar2Tk(canvas,self.PlotGraphFrame)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def main():
	app=MeteorologyApp(path = '.\\Data\\bialystok.txt')
	app.geometry("1280x720")
	if UPDATE_FLAG:
		ani = animation.FuncAnimation(f, app.update_plot, interval=1000)
	app.mainloop()


if __name__ == '__main__':
	main()
	