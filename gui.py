import matplotlib
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib import pyplot as plt

import tkinter as tk
from tkinter import ttk

data_types = ['DBT', 'RH', 'HR', 'WS', 'WD', 'ITH', 'IDH', 'ISH', 'TSKY']

vector_types = {'all' 	: 'All',
				'day' 	: 'Day',
				'week' 	: 'Week',
				'month'	: 'Month',
				'season': 'Season'}


matplotlib.use("TkAgg")
style.use("ggplot")

LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

f = Figure()
a = f.add_subplot(1,1,1)

def animate(i=None):
	pullData = open("SampleData.txt", "r").read()
	dataList = pullData.split('\n')
	xList, yList = [], []
	for line in dataList:
		if len(line)>1:
			x,y = line.split(',')
			xList.append(int(x))
			yList.append(int(y))
	a.clear()
	a.plot(xList, yList)



class MeteorologyApp(tk.Tk):
	"""docstring for MeteorologyApp"""
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		self.currType = tk.StringVar()
		self.currType.set('DBT')
		self.currCorrType = tk.StringVar()
		self.currCorrType.set('DBT')
		self.currVector = tk.StringVar()
		self.currVector.set('day')
		self.currCorrVector = tk.StringVar()
		self.currCorrVector.set('day')
		
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

		Edit = tk.Entry(fTimeVector, width = 3)
		Edit.pack()
		Edit.insert(0, "1")

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

		min_label = tk.Label(self, text="Min: ", font=LARGE_FONT)
		min_label.grid(row = 0, column = 0, sticky = 'nsew')

		max_label = tk.Label(self, text="Max: ", font=LARGE_FONT)
		max_label.grid(row = 0, column = 2, sticky = 'nsew')

		mean_label = tk.Label(self, text="Mean: ", font=LARGE_FONT)
		mean_label.grid(row = 1, column = 0, sticky = 'nsew')

		median_label = tk.Label(self, text="Median: ", font=LARGE_FONT)
		median_label.grid(row = 1, column = 2, sticky = 'nsew')

		std_label = tk.Label(self, text="Standart deviation: ", font=LARGE_FONT)
		std_label.grid(row = 2, column = 0, sticky = 'nsew')

		varience_label = tk.Label(self, text="Varience: ", font=LARGE_FONT)
		varience_label.grid(row = 2, column = 2, sticky = 'nsew')

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
		fCorrFrame = tk.Frame(self)
		fCorrFrame.grid(row = 0, column = 0, sticky = 'nsew', padx=5, pady = 5)
		for index, dType in enumerate(data_types):
			tk.Radiobutton(fCorrFrame, text=dType, font = NORMAL_FONT,
				variable=self.master.currCorrType, value=dType).grid(row = index, column = 0, 
				sticky = 'nsew', padx=5, pady = 5)

		index = 0
		for vType, vLabel in vector_types.items():
			tk.Radiobutton(fCorrFrame, text=vLabel, font = NORMAL_FONT,
				variable=self.master.currCorrVector, value=vType).grid(row = index, column = 1, 
				sticky = 'nsew', padx=5, pady = 5)
			index+=1

app=MeteorologyApp()
app.geometry("1280x720")
ani = animation.FuncAnimation(f, animate, interval=5000)
app.mainloop()
