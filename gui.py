import matplotlib
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import ttk

import pandas as pd
import numpy as np

import data as dt

data_types = ['DBT', 'RH', 'HR', 'WS', 'WD', 'ITH', 'IDH', 'ISH', 'TSKY']

vector_types = {'all' 	: 'All',
				'day' 	: 'Day',
				'week' 	: 'Week',
				'month'	: 'Month',
				'season': 'Season'}

plot_types = ['Autocorrelation','Correlation', 'Plot Data']


matplotlib.use("TkAgg")
style.use("ggplot")

LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

f = Figure()
a = f.add_subplot(1,1,1)


class MeteorologyApp(tk.Tk):
	"""docstring for MeteorologyApp"""
	def __init__(self, path = '.\\Data\\bialystok.txt', *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.path = path

		self.currType = tk.StringVar()
		self.currType.set('DBT')
		self.currCorrType = tk.StringVar()
		self.currCorrType.set('DBT')
		self.currVector = tk.StringVar()
		self.currVector.set('week')
		self.currPlotType = tk.StringVar()
		self.currPlotType.set('Autocorrelation')
		self.Min = tk.StringVar()
		self.Max = tk.StringVar()
		self.Mean = tk.StringVar()
		self.Median = tk.StringVar()
		self.Std = tk.StringVar()
		self.Var = tk.StringVar()
		self.Min.set('Hi_ok')
		self.Max.set('Hi_ok')
		self.Mean.set('Hi_ok')
		self.Median.set('Hi_ok')
		self.Std.set('Hi_ok')
		self.Var.set('Hi_ok')

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
		
		self.show_frame(WarningPage)

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

		city = dt.WeatherData(self.path) 
		
		d_type = self.currType.get()
		t_interval = self.currVector.get()
		intr_number = self.frames[MainPage].Edit.get()
		# Add try
		if intr_number == '':
			intr_number = 1
		else:
			intr_number = int(intr_number)

		dFrame_uns = city.get_frame(
			d_type = d_type, 
			t_interval = t_interval,
			intr_number = intr_number)
		self.update_stats(dFrame_uns)
		dFrame = dFrame_uns.sort_index()
		
		plot_type = self.currPlotType.get()
		if plot_type == 'Autocorrelation':
			corr_list=[]
			
			max_lag = self.frames[MainPage].p_frames[PlotPage].Edit.get()
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
			intr_number2 = self.frames[MainPage].p_frames[PlotPage].Edit2.get()
			# Add try
			if intr_number2 == '':
				intr_number2 = 1
			else:
				intr_number2 = int(intr_number2)
			dFrame_second_uns = city.get_frame(
				d_type = self.currCorrType.get(), 
				t_interval = t_interval,
				intr_number = intr_number2)
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
		self.grid_columnconfigure(0, weight = 0)
		self.grid_columnconfigure(1, weight = 1)
		#self.grid_columnconfigure(2, weight = 2)

		self.fOptions = tk.Frame(self)
		self.fOptions.grid(row = 0, column = 0, sticky = 'nsw')
		self.fOptions.grid_rowconfigure(0, weight = 1)
		self.fOptions.grid_rowconfigure(1, weight = 1)
		self.fOptions.grid_columnconfigure(0, weight = 1)


		self.DataTypes()
		self.TimeVector()
		self.Plot()

	def DataTypes(self):
		fDataTypes = tk.LabelFrame(self.fOptions, text = 'Data types')
		fDataTypes.grid(row = 0, column = 0, sticky = 'nsew', padx=5, pady = 5)

		label = tk.Label(fDataTypes, text="Choose the data\nyou are interested in:", font=LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		for dType in data_types:
			tk.Radiobutton(fDataTypes, text=dType, font = NORMAL_FONT,
				variable=self.controller.currType, value=dType).pack()


	def TimeVector(self):	
		fTimeVector = tk.LabelFrame(self.fOptions, text = 'Time periods',font = NORMAL_FONT)
		fTimeVector.grid(row = 1, column = 0, sticky = 'nsew', padx=5, pady = 5)

		label = tk.Label(fTimeVector, text="Choose the time period\nyou are interested in:", font=LARGE_FONT)
		label.pack(pady = 10, padx = 10)	

		for vType, vLabel in vector_types.items():
			tk.Radiobutton(fTimeVector, text=vLabel, font = NORMAL_FONT,
				variable=self.controller.currVector, value=vType).pack()

		# Improve
		l_text = "\nSpecify the number of the {}".format(self.controller.currVector.get())
		label2 = tk.Label(fTimeVector, text=l_text, font=LARGE_FONT)
		label2.pack(pady = 10, padx = 10)	

		self.Edit = tk.Entry(fTimeVector, width = 3)
		self.Edit.pack()
		self.Edit.insert(0, "1")

	def show_frame(self,cont):
		frame = self.p_frames[cont]
		frame.tkraise()

	def Plot(self):
		fPlot = tk.LabelFrame(self, text = 'Results',font = NORMAL_FONT)
		fPlot.grid(row = 0, column = 1, sticky = 'nsew', padx=5)

		fPlot.grid_rowconfigure(0, weight = 1)
		fPlot.grid_rowconfigure(1, weight = 10)
		fPlot.grid_columnconfigure(0, weight = 1)
		fPlot.grid_columnconfigure(1, weight = 1)

		button1 = tk.Button(fPlot, text = "Statistics", font = LARGE_FONT,
			command=lambda: self.show_frame(StatisticsPage))
		button1.grid(row = 0, column = 0, sticky = 'nsew', padx=5, pady = 5)

		button2 = tk.Button(fPlot, text = "Plot", font = LARGE_FONT,
			command=lambda: self.show_frame(PlotPage))
		button2.grid(row = 0, column = 1, sticky = 'nsew', padx=5, pady = 5)	

		self.p_frames = {}
		for Page in (PlotPage, StatisticsPage):
			frame = Page(fPlot, self, self.controller)
			self.p_frames[Page] = frame
			frame.grid(row = 1, column = 0, sticky = 'nsew', columnspan = 2)	

class StatisticsPage(tk.Frame):
	"""docstring for PageOne"""
	def __init__(self, parent, controller, master):
		tk.Frame.__init__(self, parent)

		self.grid_columnconfigure(0, weight = 1)
		self.grid_columnconfigure(1, weight = 1)
		self.grid_columnconfigure(2, weight = 1)
		self.grid_columnconfigure(3, weight = 1)

		self.grid_rowconfigure(0, weight = 1)
		self.grid_rowconfigure(1, weight = 1)
		self.grid_rowconfigure(2, weight = 1)

		self.min_label = tk.Label(self, text="Min: ", font=LARGE_FONT)
		self.min_label.grid(row = 0, column = 0, sticky = 'nsew')
		self.min_ans = tk.Label(self, textvariable=master.Min, font=LARGE_FONT)
		self.min_ans.grid(row = 0, column = 1, sticky = 'nsew')
		self.max_label = tk.Label(self, text="Max: ", font=LARGE_FONT)
		self.max_label.grid(row = 0, column = 2, sticky = 'nsew')
		self.max_ans = tk.Label(self, textvariable=master.Max, font=LARGE_FONT)
		self.max_ans.grid(row = 0, column = 3, sticky = 'nsew')
		self.mean_label = tk.Label(self, text="Mean: ", font=LARGE_FONT)
		self.mean_label.grid(row = 1, column = 0, sticky = 'nsew')
		self.mean_ans = tk.Label(self, textvariable=master.Mean, font=LARGE_FONT)
		self.mean_ans.grid(row = 1, column = 1, sticky = 'nsew')
		self.median_label = tk.Label(self, text="Median: ", font=LARGE_FONT)
		self.median_label.grid(row = 1, column = 2, sticky = 'nsew')
		self.median_ans = tk.Label(self, textvariable=master.Median, font=LARGE_FONT)
		self.median_ans.grid(row = 1, column = 3, sticky = 'nsew')
		self.std_label = tk.Label(self, text="Standart deviation: ", font=LARGE_FONT)
		self.std_label.grid(row = 2, column = 0, sticky = 'nsew')
		self.std_ans = tk.Label(self, textvariable=master.Std, font=LARGE_FONT)
		self.std_ans.grid(row = 2, column = 1, sticky = 'nsew')
		self.varience_label = tk.Label(self, text="Variance: ", font=LARGE_FONT)
		self.varience_label.grid(row = 2, column = 2, sticky = 'nsew')
		self.varience_ans = tk.Label(self, textvariable=master.Var, font=LARGE_FONT)
		self.varience_ans.grid(row = 2, column = 3, sticky = 'nsew')

class PlotPage(tk.Frame):
	"""docstring for PageOne"""
	def __init__(self, parent, controller, master):
		tk.Frame.__init__(self, parent)
		self.master = master

		self.grid_rowconfigure(0, weight = 1)
		self.grid_columnconfigure(0, weight = 0)
		self.grid_columnconfigure(1, weight = 1)

		self.PlotFrame()
		self.CorrFrame()

	def PlotFrame(self):
		fPlotFrame = tk.LabelFrame(self, text = 'Plot',font = NORMAL_FONT)
		fPlotFrame.grid(row = 0, column = 1, sticky = 'nsew', padx=5, pady = 5)

		canvas = FigureCanvasTkAgg(f, fPlotFrame)
		canvas.draw()
		canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady = 5)

		toolbar = NavigationToolbar2Tk(canvas,fPlotFrame)
		toolbar.update()
		canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

	def CorrFrame(self):
		fShooseFrame = tk.LabelFrame(self, text = 'Plot options',font = NORMAL_FONT)
		fShooseFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=5, pady = 5)

		fShooseFrame.grid_rowconfigure(0, weight = 1)
		fShooseFrame.grid_rowconfigure(1, weight = 1)
		fShooseFrame.grid_rowconfigure(2, weight = 1)
		fShooseFrame.grid_rowconfigure(3, weight = 4)
		fShooseFrame.grid_columnconfigure(0, weight = 1)


		fCorrFrame = tk.Frame(fShooseFrame)
		fCorrFrame.grid(row = 3, column = 0, sticky = 'nsew', padx=5, pady = 5)
		fBlankFrame = tk.Frame(fShooseFrame)
		fBlankFrame.grid(row = 3, column = 0, sticky = 'nsew', padx=5, pady = 5)
		fAutocorrFrame = tk.Frame(fShooseFrame)
		fAutocorrFrame.grid(row = 3, column = 0, sticky = 'nsew', padx=5, pady = 5)

		corr_frames = {'Autocorrelation':fAutocorrFrame,'Correlation':fCorrFrame,'Plot Data':fBlankFrame}
		
		for index, pType in enumerate(plot_types):
			tk.Radiobutton(fShooseFrame, text=pType, font = LARGE_FONT,
				variable=self.master.currPlotType, value=pType,
				command = lambda:	corr_frames[self.master.currPlotType.get()].tkraise()
				).grid(row = index, column = 0, 
				sticky = 'nsew', padx=5, pady = 5)

		for index, dType in enumerate(data_types):
			tk.Radiobutton(fCorrFrame, text=dType, font = NORMAL_FONT,
				variable=self.master.currCorrType, value=dType).grid(row = index, column = 0, 
				sticky = 'nsew', padx=5, pady = 5)

		# improve update
		l_text2 = "\nSpecify the number of the periods {}".format(self.master.currVector.get())
		label2 = tk.Label(fCorrFrame, text=l_text2, font=LARGE_FONT)
		label2.grid(row = len(data_types), column = 0, sticky = 'nsew', padx=5, pady = 5)

		self.Edit2 = tk.Entry(fCorrFrame, width = 4)
		self.Edit2.grid(row = len(data_types)+1, column = 0, sticky = 'nsew', padx=5, pady = 5)
		self.Edit2.insert(0, "1")

		l_text = "\nSpecify the number of the lags"
		label1 = tk.Label(fAutocorrFrame, text=l_text, font=LARGE_FONT)
		label1.pack(pady = 10, padx = 10)	

		self.Edit = tk.Entry(fAutocorrFrame, width = 8)
		self.Edit.pack()
		self.Edit.insert(0, "40")


def main():
	app=MeteorologyApp(path = '.\\Data\\bialystok.txt')
	app.geometry("1280x720")
	ani = animation.FuncAnimation(f, app.update_plot, interval=1000)
	app.mainloop()


if __name__ == '__main__':
	main()
	