import matplotlib.animation as animation 	# matplotlib animations, needed for the line 488
import matplotlib	# matplotlib inside Tkinter (look ideas.md -> links -> [1])
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style 				# better-looking matplotlib, line 8
from matplotlib import pyplot as plt 		# matplotlib plots tool
matplotlib.use("TkAgg")
style.use("ggplot")

import tkinter as tk
from tkinter import ttk 	# for modern widgets as buttons in line 235
from tkinter.filedialog import askopenfilename as tkOpenFile   

import pandas as pd
import numpy as np

import data as dt 	# my own python script data.py


# Initializing all names for the Radio Buttons on the panel of choosing data types and time periods 
CategoriesList = ['DBT', 'RH', 'HR', 'WS', 'WD', 'ITH', 'IDH', 'ISH', 'TSKY']
TimePeriodsDict = {	'all' 	: 'All',
					'day' 	: 'Day',
					'week' 	: 'Week',
					'month'	: 'Month',
					'season': 'Season'}
PlotTypesList = ['Autocorrelation','Correlation', 'Plot Data']

# Some colours, which are often used in my program
light_green = '#96f97b'
inactive_col = 'lightgrey'

# Correspond for the updating of the graph and statistics
UPDATE_FLAG = False		# It has to be false if the input file isn't preloaded
						# in the beginning of the program

# Predefined fonts for convenience
ULTRA_FONT = ("Verdana", 14, 'bold')
BOLD_FONT = ("Verdana", 12, 'bold')
LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

# Text written on the warning page
disclaimer = 'ALPHA Weather tracking application.\nUse at your own risk.\nThere is no promise of warranty.'
disclaimer+= '\n\nDo you agree and continue?'

# Defining a figure 'f' and it's axis 'a' (matplotlib packages) 
f = Figure()
a = f.add_subplot(1,1,1)

class MeteorologyApp(tk.Tk):

	def __init__(self, *args, **kwargs):
		''' Initializing an object as a child of the Tkinter application class. '''
		tk.Tk.__init__(self, *args, **kwargs)

		# Initializing some Tkinter variables, which are used to dynamically change 
		# the text in the Tkinter widgets
		self._category = tk.StringVar()
		self._category.set('DBT')
		self._corr_category = tk.StringVar()
		self._corr_category.set('DBT')
		self._time_period = tk.StringVar()
		self._time_period.set('week')
		self._plot_type = tk.StringVar()
		self._plot_type.set('Autocorrelation')
		self._question = tk.StringVar()
		self._question.set('Specify the number\nof the week')
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

		# Setting the icon and the title of the application window
		tk.Tk.iconbitmap(self, default='icon.ico')
		tk.Tk.wm_title(self, " Meteorology")

		# Initializing the main frame of the application (maybe it is possible to live 
		container = tk.Frame(self)					# without it, but I found it easier)
		container.pack(side = "top", fill = "both", expand = True)
		container.grid_rowconfigure(0, weight = 1)	# The best explanation of the row/column configure 
		container.grid_columnconfigure(0, weight = 1)	# function can be found in ideas.md [2]

		# Creating a top menu and 2 buttons there
		menubar = tk.Menu(container)
		filemenu = tk.Menu(menubar, tearoff = 0)
		filemenu.add_command(label='Load...', 
			command = self.InitializeFile)
		filemenu.add_separator()
		filemenu.add_command(label = 'Exit', command = quit)
		menubar.add_cascade(label = 'File', menu = filemenu)
		tk.Tk.config(self, menu = menubar)

		# Creating a 'page flipper'
		self.frames = {}
		for Page in (WarningPage, MainPage):	# Page - a pointer to the class WarningPage, MainPage
			frame = Page(container, self)		# creating an object frame
			self.frames[Page] = frame 			# and adding it to the dictionary with the key of its class name
			frame.grid(row = 0, column = 0, sticky = 'nsew') # Positioning the frame in the container
		
		self.show_frame(WarningPage)  # Starting page



	def InitializeFile(self):
		''' Function which is called when the user wants to open a file '''
		self.path = tkOpenFile(initialdir = '.\\Data\\', title = 'Choose your database', 
			filetypes=(('Txt files', '*.txt'),('CSV files', '*.csv')))		# available types of files

		# Reading an input file if it was chosen
		if self.path!='':
			if self.path[-3:]=='txt':
				self.City = dt.WeatherData(path = self.path, filetype = 'txt')
			elif self.path[-3:]=='csv':
				self.City = dt.WeatherData(path = self.path, filetype = 'csv')

			# Starting refreshing the plot and the statistics page
			global UPDATE_FLAG
			UPDATE_FLAG = True



	def show_frame(self,cont):
		''' Pushes a frame 'cont' to the top layer ''' 
		frame = self.frames[cont]
		frame.tkraise()



	def update_stats(self, dFrame):
		''' Updates statistics  '''
		stats_list = [np.min, np.max, np.mean, np.median, np.std, np.var] 	# The list of functions
		stats = dFrame.agg(stats_list)			# which have to be aggregated on the DataFrame 'dFrame'

		# Updating captions on the Labels
		self.Min.set(round(stats['amin'], 3))
		self.Max.set(round(stats['amax'], 3))
		self.Mean.set(round(stats['mean'], 3))
		self.Median.set(round(stats['median'], 3))
		self.Std.set(round(stats['std'], 3))
		self.Var.set(round(stats['var'], 3))



	def update_plot(self,i=None):
		''' Updates plot when UPDATE_FLAG is turned on '''

		def numb_to_eng(numb):
			''' Inside function, which returns a normalized version of English numerals'''
			
			# Some English words used to name the axis on the graph accurately
			engdict = {	'1':'first',
						'2':'second',
						'3':'third'}

			if str(numb)[-1] in engdict.keys() and numb<10:
				return engdict[str(numb)[-1]] 
			elif str(numb)[-1] in engdict.keys() and str(numb)[-2:] not in ['11', '12', '13']:
				if str(numb)[-1] in ['2', '3']:
					return str(numb)+'d'
				else:
					return str(numb)+'st'
			else:
				return str(numb)+'th'
		
		# Default plot title
		plot_title = ''

		if UPDATE_FLAG:	
			# Reading the parameters set by the user in the Radio Buttons and Edit
			dCategory = self._category.get()
			tPeriod = self._time_period.get()
			tPeriod_numb = self.frames[MainPage].Edit_tPeriod_numb.get()
			# Excepting errors when user tries to enter a new value 
			try:							# or misspells something
				tPeriod_numb = int(tPeriod_numb) 
			except ValueError:
				tPeriod_numb = 1	

			plot_title += 'Graph of the '

			# Getting a DataFrame with the special time period and data type 
			# using proprietary python script data.py  
			dFrame = self.City.get_frame(
				d_type = dCategory, 
				t_interval = tPeriod,
				intr_number = tPeriod_numb)
			self.update_stats(dFrame) 		# Updating the statistics
			
			# Getting the information about which type of the plot is chosen
			plot_type = self._plot_type.get()
			# and running one of the following tasks with that information

			if plot_type == 'Autocorrelation':
				a.clear()	# Clearing the previous axes
				corr_list=[]
				plot_title += 'autocorrelation function'

				# Getting the number of lags chosen by the user
				max_lag = self.frames[MainPage].Edit_autoLag.get()
				# Excepting errors when user tries to enter a new value 
				try:							# or misspells something
					max_lag = int(max_lag)
				except ValueError:
					max_lag = 40
				for lag in range(max_lag):
					corr_list.append(dFrame.autocorr(lag))

				# same as in the Matlab language (linearly spaced vector)
				x_ax = np.linspace(1,max_lag,max_lag)
				a.set_xlabel('Lag')
				a.set_ylabel('{} autocorrelation'.format(dCategory))

				# Plotting the line on the 0 to improve graph readability
				a.eventplot([0], orientation='vertical',linewidths=2.0, lineoffsets=0, linelengths=2*(max_lag+10))
				a.scatter(x_ax, corr_list, s=25)
				a.vlines(x_ax, [0 for i in range(max_lag)], corr_list)
				a.set_xlim((-2,max_lag+2))

			elif plot_type == 'Correlation':
				a.clear()	# Clearing the previous axes

				# Getting a second DataFrame with the special data type 
				# but same time period
				tPeriod_numb2 = self.frames[MainPage].Edit_tPeriod2_numb.get()
				try:
					tPeriod_numb2 = int(tPeriod_numb2)
				except ValueError:
					tPeriod_numb2 = 1
				dCategory2 = self._corr_category.get()
				dFrame_second = self.City.get_frame(
					d_type = dCategory2, 
					t_interval = tPeriod,
					intr_number = tPeriod_numb2)

				# Clearing the Pandas Series from empty spaces (dropna)
				s_x = dFrame.diff().dropna() # and finding the difference between 
				s_y = dFrame_second.diff().dropna()	# neighbour numbers

				# Creating a label of the axis
				if tPeriod == 'all':
					a.set_xlabel('{} differences, whole year'.format(dCategory))
					a.set_ylabel('{} differences, whole year'.format(dCategory2))
				else:
					a.set_xlabel('{} differences, {} {}'.format(dCategory, numb_to_eng(tPeriod_numb), tPeriod))
					a.set_ylabel('{} differences, {} {}'.format(dCategory2, numb_to_eng(tPeriod_numb2), tPeriod))
				
				# Making sure that both series are equal (important for seasons and months comparison)
				# truncate method cuts the Pandas Series (ideas.md [3])
				if len(s_x)>len(s_y):
					s_x = s_x.truncate(s_x.index[0], s_x.index[len(s_y)-1]) 
				elif len(s_y)>len(s_x):
					s_y = s_y.truncate(s_y.index[0], s_y.index[len(s_x)-1])
				a.scatter(s_x, s_y, s = 5)

				# Removing date indexes from the series 
				# (otherwise if different months where chosen, it conflicts with Pandas .corr method)
				s_x.reset_index(level = 0, drop = True,inplace=True) 
				s_y.reset_index(level = 0, drop = True,inplace=True)
				corr_val = round(s_x.corr(s_y),2)
				plot_title += 'correlation function, ({})'.format(corr_val)
			
			elif plot_type == 'Plot Data':
				dFrame = dFrame.sort_index()
				a.clear()
				plot_title += 'data values'
				x_ax = np.linspace(1,len(dFrame),len(dFrame))
				a.set_xlabel('{}s'.format(TimePeriodsDict[tPeriod]))
				a.set_ylabel('{}'.format(dCategory))
				a.plot(dFrame.index, dFrame)
		a.set_title(plot_title)



class WarningPage(tk.Frame):
	"""docstring for WarningPage"""
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = tk.Label(self, text=disclaimer, font=LARGE_FONT)
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
		self.defaultcolor = self.cget('bg')

		self.grid_rowconfigure(0, weight = 1)
		self.grid_rowconfigure(1, weight = 2)
		self.grid_rowconfigure(2, weight = 2)
		self.grid_columnconfigure(0, weight = 1)
		self.grid_columnconfigure(1, weight = 2)

		self.CategoryFrame = tk.LabelFrame(self, text = 'Data types')
		self.CategoryFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=5, pady = 5, rowspan=2)
		self.Category()

		self.TimePeriodFrame = tk.LabelFrame(self, text = 'Time periods')
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
		
		self.CategoryRadiobuttons = {}

		Label = tk.Label(self.CategoryFrame, text="Choose the data\nyou are interested in:", font=LARGE_FONT)
		Label.pack()

		for cType in CategoriesList:
			self.CategoryRadiobuttons[cType] = tk.Radiobutton(self.CategoryFrame, 
				text=cType, font = NORMAL_FONT,	variable=self.controller._category, value=cType,
				command = lambda:self.ActivateRadioButton(self.controller._category, self.CategoryRadiobuttons))

			self.CategoryRadiobuttons[cType].pack()

		self.CategoryRadiobuttons['DBT'].config(fg='green')

	def ActivateRadioButton(self, RBnameVar, RBdict):
		RBname = RBnameVar.get()
		for key, RBobject in RBdict.items():
			if key!=RBname:
				RBobject.config(fg='black')
			else:
				RBobject.config(fg='green')


	def TimePeriod(self):	

		self.TimePeriodsRadiobuttons = {}

		label = tk.Label(self.TimePeriodFrame, text="Choose the time period\nyou are interested in:", font=LARGE_FONT)
		label.pack(pady = 10, padx = 10)	

		for pType, pLabel in TimePeriodsDict.items():
			self.TimePeriodsRadiobuttons[pType] = tk.Radiobutton(self.TimePeriodFrame, 
				text=pLabel, font = NORMAL_FONT, variable=self.controller._time_period, value=pType,
				command = lambda: new_time_period(self.controller._time_period, self.TimePeriodsRadiobuttons))
			self.TimePeriodsRadiobuttons[pType].pack()
		self.TimePeriodsRadiobuttons['week'].config(fg = 'green')

		def new_time_period(RBnameVar, RBdict):
			self.controller._question.set("Specify the number\nof the {}".format(self.controller._time_period.get()))
			self.ActivateRadioButton(RBnameVar, RBdict)
		
		label2 = tk.Label(self.TimePeriodFrame, textvariable=self.controller._question, font=LARGE_FONT)
		label2.pack(pady = 10, padx = 10)	

		self.Edit_tPeriod_numb = tk.Entry(self.TimePeriodFrame, width = 3)
		self.Edit_tPeriod_numb.pack()
		self.Edit_tPeriod_numb.insert(0, "1")

	def Buttons(self):
		self.ButtonsFrame.grid_columnconfigure(0, weight=1)
		self.ButtonsFrame.grid_columnconfigure(1, weight=1)
		self.ButtonsFrame.grid_rowconfigure(0, weight=1)

		self.StatButton = tk.Button(self.ButtonsFrame, text = "Statistics", font = ULTRA_FONT,bg = light_green,
			command = lambda:self.BStatFunc())
		self.StatButton.grid(row = 0, column = 0, sticky = 'nsew', padx=5, pady = 5)

		self.PlotButton = tk.Button(self.ButtonsFrame, text = "Plot", font = ULTRA_FONT, bg = inactive_col,
			command = lambda:self.BPlotFunc())
		self.PlotButton.grid(row = 0, column = 1, sticky = 'nsew', padx=5, pady = 5)	

	def BStatFunc(self):
		self.StatisticsFrame.tkraise()
		self.StatButton.config(bg = light_green)
		self.PlotButton.config(bg = inactive_col)

	def BPlotFunc(self):
		self.PlotFrame.tkraise()
		self.PlotButton.config(bg = light_green)
		self.StatButton.config(bg = inactive_col)


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

		min_label = tk.Label(self.StatisticsFrame, text="Min: ", font=BOLD_FONT)
		min_label.grid(row = 0, column = 0, sticky = 'nse')
		min_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Min, font=LARGE_FONT)
		min_ans.grid(row = 0, column = 1, sticky = 'nsw')
		max_label = tk.Label(self.StatisticsFrame, text="Max: ", font=BOLD_FONT)
		max_label.grid(row = 0, column = 2, sticky = 'nse')
		max_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Max, font=LARGE_FONT)
		max_ans.grid(row = 0, column = 3, sticky = 'nsw')
		mean_label = tk.Label(self.StatisticsFrame, text="Mean: ", font=BOLD_FONT)
		mean_label.grid(row = 1, column = 0, sticky = 'nse')
		mean_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Mean, font=LARGE_FONT)
		mean_ans.grid(row = 1, column = 1, sticky = 'nsw')
		median_label = tk.Label(self.StatisticsFrame, text="Median: ", font=BOLD_FONT)
		median_label.grid(row = 1, column = 2, sticky = 'nse')
		median_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Median, font=LARGE_FONT)
		median_ans.grid(row = 1, column = 3, sticky = 'nsw')
		std_label = tk.Label(self.StatisticsFrame, text="Standart \ndeviation: ", font=BOLD_FONT)
		std_label.grid(row = 2, column = 0, sticky = 'nse')
		std_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Std, font=LARGE_FONT)
		std_ans.grid(row = 2, column = 1, sticky = 'nsw')
		varience_label = tk.Label(self.StatisticsFrame, text="Variance: ", font=BOLD_FONT)
		varience_label.grid(row = 2, column = 2, sticky = 'nse')
		varience_ans = tk.Label(self.StatisticsFrame, textvariable=self.controller.Var, font=LARGE_FONT)
		varience_ans.grid(row = 2, column = 3, sticky = 'nsw')

	def PlotOptions(self):
		self.PlotOptionsFrame.grid_rowconfigure(0, weight = 1)
		self.PlotOptionsFrame.grid_rowconfigure(1, weight = 1)
		self.PlotOptionsFrame.grid_columnconfigure(0, weight = 1)

	def PlotOptionsType(self):
		self.PlotTypeRadiobuttons = {}

		for pType in PlotTypesList:

			self.PlotTypeRadiobuttons[pType] = tk.Radiobutton(self.PlotOptionsTypeFrame, 
				text=pType, font = LARGE_FONT, variable=self.controller._plot_type, value=pType,
				command = lambda: PlotOptionsTypeCommand(self.controller._plot_type, self.PlotTypeRadiobuttons))

			self.PlotTypeRadiobuttons[pType].pack(side = "top", fill = "x")
		
		def PlotOptionsTypeCommand(RBnameVar, RBdict):
			self.TypesFrames[RBnameVar.get()].tkraise()
			self.ActivateRadioButton(RBnameVar, RBdict)
		
		self.PlotTypeRadiobuttons['Autocorrelation'].config(fg='green')
		

	def PlotOptionsAutocorr(self):
		l_text = "\nSpecify the number of the lags"
		label1 = tk.Label(self.PlotOptionsAutocorrFrame, text=l_text, font=LARGE_FONT)
		label1.pack(pady = 10, padx = 10)	

		self.Edit_autoLag = tk.Entry(self.PlotOptionsAutocorrFrame, width = 8)
		self.Edit_autoLag.pack()
		self.Edit_autoLag.insert(0, "40")

	def PlotOptionsCorr(self):
		self.CorrCategoryRadiobuttons = {}

		for cType in CategoriesList:
			self.CorrCategoryRadiobuttons[cType] = tk.Radiobutton(self.PlotOptionsCorrFrame, 
				text=cType, font = NORMAL_FONT,	variable=self.controller._corr_category, value=cType,
				command = lambda:self.ActivateRadioButton(self.controller._corr_category, self.CorrCategoryRadiobuttons))

			self.CorrCategoryRadiobuttons[cType].pack(side = "top", fill = "both")

		self.CorrCategoryRadiobuttons['DBT'].config(fg='green')

		label2 = tk.Label(self.PlotOptionsCorrFrame,textvariable=self.controller._question, font=LARGE_FONT)
		label2.pack(side = "top", fill = "both")

		self.Edit_tPeriod2_numb = tk.Entry(self.PlotOptionsCorrFrame, width = 4)
		self.Edit_tPeriod2_numb.pack(side = "top")
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
	app=MeteorologyApp()
	app.geometry("1280x720")
	ani = animation.FuncAnimation(f, app.update_plot, interval=1000)
	app.mainloop()


if __name__ == '__main__':
	main()
	