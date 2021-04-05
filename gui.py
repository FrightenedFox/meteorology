import sys

import matplotlib.animation as animation  # matplotlib animations, needed for the line 653
import matplotlib  # matplotlib inside Tkinter (look ideas.md -> links -> [1])
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style  # better-looking matplotlib, line 8
import tkinter as tk
from tkinter import ttk  # for modern widgets such as buttons in line 343
from tkinter.filedialog import askopenfilename as tk_open_file
import numpy as np

import data as dt  # my own python script data.py

matplotlib.use("TkAgg")
style.use("ggplot")

# Initializing all names for the Radio Buttons on the panel for choosing data types and time periods
CategoriesList = ["DBT", "RH", "HR", "WS", "WD", "ITH", "IDH", "ISH", "TSKY"]
TimePeriodsDict = {
    "all": "All",
    "day": "Day",
    "week": "Week",
    "month": "Month",
    "season": "Season",
}
PlotTypesList = ["Autocorrelation", "Correlation", "Plot Data"]

# Some colours, which are often used in my program
light_green = "#96f97b"
inactive_col = "lightgrey"

# Corresponds for the updating of the graph and statistics
UPDATE_FLAG = False  # It has to be false if the input file isn't preloaded
NEW_FILE = False  # at the beginning of the program


# Predefined fonts for convenience
ULTRA_FONT = ("Verdana", 14, "bold")
BOLD_FONT = ("Verdana", 12, "bold")
LARGE_FONT = ("Verdana", 12)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

# Text written on the warning page
disclaimer = "ALPHA Weather tracking application.\nUse at your own risk.\nThere is no promise of warranty."
disclaimer += "\n\nDo you agree and continue?"

# Defining a figure 'f' and its axis 'a' (matplotlib packages)
f = Figure()
a = f.add_subplot(1, 1, 1)


class MeteorologyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        """ Initializing an object as a child of the Tkinter application class. """
        tk.Tk.__init__(self, *args, **kwargs)

        # Initializing some Tkinter variables, which are used to change dynamically
        # the text in the Tkinter widgets
        self._category = tk.StringVar()
        self._category.set("DBT")
        self._corr_category = tk.StringVar()
        self._corr_category.set("DBT")
        self._time_period = tk.StringVar()
        self._time_period.set("week")
        self._plot_type = tk.StringVar()
        self._plot_type.set("Autocorrelation")
        self._question = tk.StringVar()
        self._question.set("Specify the number\nof the week")
        self.Min = tk.StringVar()
        self.Min.set("Init-value")
        self.Max = tk.StringVar()
        self.Max.set("Init-value")
        self.Mean = tk.StringVar()
        self.Mean.set("Init-value")
        self.Median = tk.StringVar()
        self.Median.set("Init-value")
        self.Std = tk.StringVar()
        self.Std.set("Init-value")
        self.Var = tk.StringVar()
        self.Var.set("Init-value")

        # Setting the icon and the title of the application window
        if sys.platform.startswith("win"):
            tk.Tk.iconbitmap(self, default="Images/icon.ico")  # Works only for windows
        else:
            logo = tk.PhotoImage(file="Images/icon.gif")  # Works only for Linux
            self.call("wm", "iconphoto", self._w, logo)
        tk.Tk.wm_title(self, " Meteorology")

        # Initializing the main frame of the application (maybe it is possible to live
        container = tk.Frame(self)  # without it, but I found it easier)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(
            0, weight=1
        )  # The best explanation of the row/column configure
        container.grid_columnconfigure(
            0, weight=1
        )  # function can be found in ideas.md [2]

        # Creating the top menu and 2 buttons there
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Load...", command=self.initialize_file)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)

        # Creating a 'page flipper'
        self.frames = {}
        for Page in (
            WarningPage,
            MainPage,
        ):  # Page - a pointer to the class WarningPage, MainPage
            frame = Page(container, self)  # creating an object frame
            self.frames[
                Page
            ] = frame  # and adding it to the dictionary with the key of its class name
            frame.grid(
                row=0, column=0, sticky="nsew"
            )  # Positioning the frame in the container

        # Saving default values of settings
        self.old_dCategory = self._category.get()
        self.old_tPeriod = self._time_period.get()
        self.old_tPeriod_numb = self.frames[MainPage].Edit_tPeriod_numb.get()
        self.old_dCategory2 = self._corr_category.get()
        self.old_tPeriod_numb2 = self.frames[MainPage].Edit_tPeriod2_numb.get()
        self.old_plot_type = self._plot_type.get()
        self.old_max_lag = self.frames[MainPage].Edit_autoLag.get()

        self.show_frame(WarningPage)  # Starting page

    def initialize_file(self):
        """ Function which is called when the user wants to open a file """
        self.path = tk_open_file(
            initialdir="./Data/",
            title="Choose your database",
            filetypes=(("Txt files", "*.txt"), ("CSV files", "*.csv")),
        )  # available types of files

        # Reading an input file if it was chosen
        if self.path != "":
            if self.path[-3:] == "txt":
                self.City = dt.WeatherData(path=self.path, filetype="txt")
            elif self.path[-3:] == "csv":
                self.City = dt.WeatherData(path=self.path, filetype="csv")

            # Starting refreshing the plot and the statistics page
            global UPDATE_FLAG, NEW_FILE
            UPDATE_FLAG = True
            NEW_FILE = True

    def show_frame(self, cont):
        """ Pushes a frame 'cont' to the top layer """
        frame = self.frames[cont]
        frame.tkraise()

    def update_stats(self, d_frame):
        """ Updates statistics  """
        stats_list = [
            np.min,
            np.max,
            np.mean,
            np.median,
            np.std,
            np.var,
        ]  # The list of functions
        stats = d_frame.agg(
            stats_list
        )  # which have to be aggregated on the DataFrame 'dFrame'

        # Updating captions on the Labels
        self.Min.set(round(stats["amin"], 3))
        self.Max.set(round(stats["amax"], 3))
        self.Mean.set(round(stats["mean"], 3))
        self.Median.set(round(stats["median"], 3))
        self.Std.set(round(stats["std"], 3))
        self.Var.set(round(stats["var"], 3))

    def update_corr(self, d_frame, dFrame_second):
        """ Updates correlation graph """

        def numb_to_eng(numb):
            """ Inside function, which returns a normalized version of English numerals"""

            # Some English words used to name the axis on the graph accurately
            engdict = {"1": "first", "2": "second", "3": "third"}

            if str(numb)[-1] in engdict.keys() and numb < 10:
                return engdict[str(numb)[-1]]
            elif str(numb)[-1] in engdict.keys() and str(numb)[-2:] not in [
                "11",
                "12",
                "13",
            ]:
                if str(numb)[-1] in ["2", "3"]:
                    return str(numb) + "d"
                else:
                    return str(numb) + "st"
            else:
                return str(numb) + "th"

        # Clearing the Pandas Series from empty spaces (dropna)
        s_x = d_frame.diff().dropna()  # and finding the difference between
        s_y = dFrame_second.diff().dropna()  # neighbouring numbers

        # Creating a label of the axis
        if self.tPeriod == "all":
            a.set_xlabel("{} differences, whole year".format(self.dCategory))
            a.set_ylabel("{} differences, whole year".format(self.dCategory2))
        else:
            a.set_xlabel(
                "{} differences, {} {}".format(
                    self.dCategory, numb_to_eng(self.tPeriod_numb), self.tPeriod
                )
            )
            a.set_ylabel(
                "{} differences, {} {}".format(
                    self.dCategory2, numb_to_eng(self.tPeriod_numb2), self.tPeriod
                )
            )

        # Making sure that both series are equal (important for seasons and months comparison)
        # truncate method cuts the Pandas Series (ideas.md [3])
        if len(s_x) > len(s_y):
            s_x = s_x.truncate(s_x.index[0], s_x.index[len(s_y) - 1])
        elif len(s_y) > len(s_x):
            s_y = s_y.truncate(s_y.index[0], s_y.index[len(s_x) - 1])
        a.scatter(s_x, s_y, s=5)

        # Removing date indexes from the series
        # (otherwise if different months where chosen, it conflicts with Pandas .corr method)
        s_x.reset_index(level=0, drop=True, inplace=True)
        s_y.reset_index(level=0, drop=True, inplace=True)

        # Finding the value of correlation
        corr_val = round(s_x.corr(s_y), 2)
        return "correlation function, ({})".format(corr_val)

    def update_plot(self, d_frame):
        """ Updates data graph """
        # Sorting the DataFrame so that not to create some holes in the plot
        d_frame = d_frame.sort_index()
        a.set_xlabel("{}s".format(TimePeriodsDict[self.tPeriod]))
        a.set_ylabel("{}".format(self.dCategory))
        a.plot(d_frame.index, d_frame)

    def update_autocorr(self, dFrame):
        """ Updates autocorrelation graph """

        a.clear()  # Clearing the previous axes
        corr_list = []
        # Excepting errors when the user tries to enter a new value
        try:  # or misspells something
            self.max_lag = int(self.max_lag)
        except ValueError:
            self.max_lag = 40
        for lag in range(self.max_lag):
            corr_list.append(dFrame.autocorr(lag))
        # the same as in the Matlab language (linearly spaced vector)
        x_ax = np.linspace(1, self.max_lag, self.max_lag)
        a.set_xlabel("Lag")
        a.set_ylabel("{} autocorrelation".format(self.dCategory))
        # Plotting the line on the 0 to improve graph readability
        a.eventplot(
            [0],
            orientation="vertical",
            linewidths=2.0,
            lineoffsets=0,
            linelengths=2 * (self.max_lag + 10),
        )
        a.scatter(x_ax, corr_list, s=25)
        a.vlines(x_ax, [0 for i in range(self.max_lag)], corr_list)
        a.set_xlim((-2, self.max_lag + 2))

    def check_update(self, i=None):
        """ Updates plot when user changes any settings"""
        if UPDATE_FLAG:
            global NEW_FILE
            # Reading the parameters set by the user in the Radio Buttons and Edit
            self.dCategory = self._category.get()
            self.tPeriod = self._time_period.get()
            self.tPeriod_numb = self.frames[MainPage].Edit_tPeriod_numb.get()

            # Getting a second DataFrame with the special data type
            # but the same time period
            self.dCategory2 = self._corr_category.get()
            self.tPeriod_numb2 = self.frames[MainPage].Edit_tPeriod2_numb.get()

            # Getting the number of lags chosen by the user
            self.max_lag = self.frames[MainPage].Edit_autoLag.get()

            # Getting the information about which type of the plot is chosen
            plot_type = self._plot_type.get()

            # Checking if the user has changed something
            if NEW_FILE or (
                self.dCategory,
                self.tPeriod,
                self.tPeriod_numb,
                self.dCategory2,
                self.tPeriod_numb2,
                plot_type,
                self.max_lag,
            ) != (
                self.old_dCategory,
                self.old_tPeriod,
                self.old_tPeriod_numb,
                self.old_dCategory2,
                self.old_tPeriod_numb2,
                self.old_plot_type,
                self.old_max_lag,
            ):

                plot_title = ""
                a.clear()  # Clearing the previous axes
                # Excepting errors when the user tries to enter a new value
                try:  # or misspells something
                    self.tPeriod_numb = int(self.tPeriod_numb)
                except ValueError:
                    self.tPeriod_numb = 1
                plot_title += "Graph of the "
                # Getting a DataFrame with the special time period and data type
                # using my own python script data.py
                d_frame = self.City.get_frame(
                    d_type=self.dCategory,
                    t_interval=self.tPeriod,
                    intr_number=self.tPeriod_numb,
                )

                self.update_stats(d_frame)  # Updating the statistics

                if plot_type == "Autocorrelation":
                    plot_title += "autocorrelation function"
                    self.update_autocorr(d_frame)

                elif plot_type == "Correlation":

                    try:
                        self.tPeriod_numb2 = int(self.tPeriod_numb2)
                    except ValueError:
                        self.tPeriod_numb2 = 1
                    d_frame_second = self.City.get_frame(
                        d_type=self.dCategory2,
                        t_interval=self.tPeriod,
                        intr_number=self.tPeriod_numb2,
                    )

                    plot_title += self.update_corr(d_frame, d_frame_second)

                elif plot_type == "Plot Data":
                    plot_title += "data values"
                    self.update_plot(d_frame)

                a.set_title(plot_title)
                NEW_FILE = False
                # Saving new settings
                self.old_dCategory = self._category.get()
                self.old_tPeriod = self._time_period.get()
                self.old_tPeriod_numb = self.frames[MainPage].Edit_tPeriod_numb.get()
                self.old_dCategory2 = self._corr_category.get()
                self.old_tPeriod_numb2 = self.frames[MainPage].Edit_tPeriod2_numb.get()
                self.old_plot_type = self._plot_type.get()
                self.old_max_lag = self.frames[MainPage].Edit_autoLag.get()


class WarningPage(tk.Frame):
    def __init__(self, parent, controller):
        """ Initializing an object as a child of the Tkinter Frame class. """
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=disclaimer, font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(
            self, text="Agree", command=lambda: controller.show_frame(MainPage)
        )  # Here lambda is used to pass the
        button1.pack()  # arguments of the inside function

        button2 = ttk.Button(self, text="Disagree", command=quit)
        button2.pack()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        """ Initializing an object as a child of the Tkinter Frame class. """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.defaultcolor = self.cget(
            "bg"
        )  # Gets the current colour of the Frame (default colour)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Don't know exactly why, but it is impossible to use 'page flipper'(line 111) inside another page.
        # (the problem seems to appear in the 'Frame' initialization function)
        # So all children frames of the page must be initialized individually
        self.CategoryFrame = tk.LabelFrame(self, text="Data types")
        self.CategoryFrame.grid(
            row=0, column=0, sticky="nsew", padx=5, pady=5, rowspan=2
        )
        self.Category()

        self.TimePeriodFrame = tk.LabelFrame(self, text="Time periods")
        self.TimePeriodFrame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.time_period()

        self.StatisticsFrame = tk.Frame(self)
        self.StatisticsFrame.grid(row=1, column=1, sticky="nsew", rowspan=2)
        self.statistics()

        self.ButtonsFrame = tk.Frame(self)
        self.ButtonsFrame.grid(row=0, column=1, sticky="nsew")
        self.buttons()

        self.PlotFrame = tk.Frame(self)
        self.PlotFrame.grid(row=1, column=1, sticky="nsew", rowspan=2)
        self.plot()

        self.PlotOptionsFrame = tk.LabelFrame(self.PlotFrame, text="Options")
        self.PlotOptionsFrame.grid(row=0, column=0, sticky="nsew")
        self.plot_options()

        self.PlotOptionsTypeFrame = tk.Frame(self.PlotOptionsFrame)
        self.PlotOptionsTypeFrame.grid(row=0, column=0, sticky="nsew")
        self.plot_options_type()

        self.PlotOptionsAutocorrFrame = tk.Frame(self.PlotOptionsFrame)
        self.PlotOptionsAutocorrFrame.grid(row=1, column=0, sticky="nsew")
        self.plot_options_autocorr()

        self.PlotOptionsCorrFrame = tk.Frame(self.PlotOptionsFrame)
        self.PlotOptionsCorrFrame.grid(row=1, column=0, sticky="nsew")
        self.plot_options_corr()

        self.PlotOptionsBlancFrame = tk.Frame(self.PlotOptionsFrame)
        self.PlotOptionsBlancFrame.grid(row=1, column=0, sticky="nsew")
        self.plot_options_blanc()

        self.PlotGraphFrame = tk.Frame(self.PlotFrame)
        self.PlotGraphFrame.grid(row=0, column=1, sticky="nsew")
        self.plot_graph()

        self.TypesFrames = {
            "Autocorrelation": self.PlotOptionsAutocorrFrame,
            "Correlation": self.PlotOptionsCorrFrame,
            "Plot Data": self.PlotOptionsBlancFrame,
        }

        # Defining default pages
        self.PlotOptionsAutocorrFrame.tkraise()
        self.StatisticsFrame.tkraise()

    def Category(self):
        """ Defining the CategoryFrame children """
        self.CategoryRadiobuttons = {}

        label = tk.Label(
            self.CategoryFrame,
            text="Choose the data\nyou are interested in:",
            font=LARGE_FONT,
        )
        label.pack()

        # Adding RadioButton objects to the 'CategoryRadiobuttons' dictionary,
        # for them to be able to be recoloured
        for cType in CategoriesList:
            self.CategoryRadiobuttons[cType] = tk.Radiobutton(
                self.CategoryFrame,
                text=cType,
                font=NORMAL_FONT,
                variable=self.controller._category,
                value=cType,
                command=lambda: self.activate_radio_button(
                    self.controller._category, self.CategoryRadiobuttons
                ),
            )
            self.CategoryRadiobuttons[cType].pack()

        self.CategoryRadiobuttons["DBT"].config(fg="green")

    def activate_radio_button(self, RBnameVar, RBdict):
        """ Changes colour of the RadioButton when it is pressed."""
        RBname = RBnameVar.get()
        for key, RBobject in RBdict.items():
            if key != RBname:
                RBobject.config(fg="black")
            else:
                RBobject.config(fg="green")

    def time_period(self):
        """ Defining the TimePeriodFrame children """
        self.TimePeriodsRadiobuttons = {}

        label = tk.Label(
            self.TimePeriodFrame,
            text="Choose the time period\nyou are interested in:",
            font=LARGE_FONT,
        )
        label.pack(pady=10, padx=10)

        # The same as with the Category RadioButtons (later RB), but this time the names are stored in the dictionary,
        # because the RB text has to be different from the 'data.py' notations
        for pType, pLabel in TimePeriodsDict.items():
            self.TimePeriodsRadiobuttons[pType] = tk.Radiobutton(
                self.TimePeriodFrame,
                text=pLabel,
                font=NORMAL_FONT,
                variable=self.controller._time_period,
                value=pType,
                command=lambda: new_time_period(
                    self.controller._time_period, self.TimePeriodsRadiobuttons
                ),
            )
            self.TimePeriodsRadiobuttons[pType].pack()
        self.TimePeriodsRadiobuttons["week"].config(fg="green")

        def new_time_period(RBnameVar, RBdict):
            """ The command of the RadioButton"""
            self.controller._question.set(
                "Specify the number\nof the {}".format(
                    self.controller._time_period.get()
                )
            )
            self.activate_radio_button(RBnameVar, RBdict)

        label2 = tk.Label(
            self.TimePeriodFrame,
            textvariable=self.controller._question,
            font=LARGE_FONT,
        )
        label2.pack(pady=10, padx=10)

        # Creating a text field with its own Integer Variable
        self.Edit_tPeriod_numb = tk.Entry(self.TimePeriodFrame, width=3)
        self.Edit_tPeriod_numb.pack()
        self.Edit_tPeriod_numb.insert(0, "1")

    def buttons(self):
        """ Defining the ButtonFrame children """
        self.ButtonsFrame.grid_columnconfigure(0, weight=1)
        self.ButtonsFrame.grid_columnconfigure(1, weight=1)
        self.ButtonsFrame.grid_rowconfigure(0, weight=1)

        def b_stat_func():
            """ Statistics button command """
            self.StatisticsFrame.tkraise()
            stat_button.config(bg=light_green)
            plot_button.config(bg=inactive_col)

        def b_plot_func():
            """ Plot button command """
            self.PlotFrame.tkraise()
            plot_button.config(bg=light_green)
            stat_button.config(bg=inactive_col)

        stat_button = tk.Button(
            self.ButtonsFrame,
            text="Statistics",
            font=ULTRA_FONT,
            bg=light_green,
            command=b_stat_func,
        )
        stat_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        plot_button = tk.Button(
            self.ButtonsFrame,
            text="Plot",
            font=ULTRA_FONT,
            bg=inactive_col,
            command=b_plot_func,
        )
        plot_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    def plot(self):
        """Defining the PlotFrame children.
        (actually they are defined in the __init__ function and there is no reason to create
        a separate function for 3 lines of code, but this decision was made to unify the way
        of the Frame initialization)"""
        self.PlotFrame.grid_rowconfigure(0, weight=1)
        self.PlotFrame.grid_columnconfigure(0, weight=1)
        self.PlotFrame.grid_columnconfigure(1, weight=2)

    def statistics(self):
        """ Defining the StatisticsFrame children """
        self.StatisticsFrame.grid_columnconfigure(0, weight=1)
        self.StatisticsFrame.grid_columnconfigure(1, weight=1)
        self.StatisticsFrame.grid_columnconfigure(2, weight=1)
        self.StatisticsFrame.grid_columnconfigure(3, weight=1)

        self.StatisticsFrame.grid_rowconfigure(0, weight=1)
        self.StatisticsFrame.grid_rowconfigure(1, weight=1)
        self.StatisticsFrame.grid_rowconfigure(2, weight=1)

        tk.Label(self.StatisticsFrame, text="Min: ", font=BOLD_FONT).grid(
            row=0, column=0, sticky="nse"
        )
        tk.Label(self.StatisticsFrame, text="Max: ", font=BOLD_FONT).grid(
            row=0, column=2, sticky="nse"
        )
        tk.Label(self.StatisticsFrame, text="Mean: ", font=BOLD_FONT).grid(
            row=1, column=0, sticky="nse"
        )
        tk.Label(self.StatisticsFrame, text="Median: ", font=BOLD_FONT).grid(
            row=1, column=2, sticky="nse"
        )
        tk.Label(
            self.StatisticsFrame, text="Standart \ndeviation: ", font=BOLD_FONT
        ).grid(row=2, column=0, sticky="nse")
        tk.Label(self.StatisticsFrame, text="Variance: ", font=BOLD_FONT).grid(
            row=2, column=2, sticky="nse"
        )

        tk.Label(
            self.StatisticsFrame, textvariable=self.controller.Min, font=LARGE_FONT
        ).grid(row=0, column=1, sticky="nsw")
        tk.Label(
            self.StatisticsFrame, textvariable=self.controller.Max, font=LARGE_FONT
        ).grid(row=0, column=3, sticky="nsw")
        tk.Label(
            self.StatisticsFrame, textvariable=self.controller.Mean, font=LARGE_FONT
        ).grid(row=1, column=1, sticky="nsw")
        tk.Label(
            self.StatisticsFrame, textvariable=self.controller.Median, font=LARGE_FONT
        ).grid(row=1, column=3, sticky="nsw")
        tk.Label(
            self.StatisticsFrame, textvariable=self.controller.Std, font=LARGE_FONT
        ).grid(row=2, column=1, sticky="nsw")
        tk.Label(
            self.StatisticsFrame, textvariable=self.controller.Var, font=LARGE_FONT
        ).grid(row=2, column=3, sticky="nsw")

    def plot_options(self):
        """ Defining the PlotOptionsFrame children """
        self.PlotOptionsFrame.grid_rowconfigure(0, weight=1)
        self.PlotOptionsFrame.grid_rowconfigure(1, weight=1)
        self.PlotOptionsFrame.grid_columnconfigure(0, weight=1)

    def plot_options_type(self):
        """ Defining the PlotOptionsTypeFrame children """
        self.PlotTypeRadiobuttons = {}

        for pType in PlotTypesList:

            self.PlotTypeRadiobuttons[pType] = tk.Radiobutton(
                self.PlotOptionsTypeFrame,
                text=pType,
                font=LARGE_FONT,
                variable=self.controller._plot_type,
                value=pType,
                command=lambda: plot_options_type_command(
                    self.controller._plot_type, self.PlotTypeRadiobuttons
                ),
            )

            self.PlotTypeRadiobuttons[pType].pack(side="top", fill="x")

        def plot_options_type_command(RBnameVar, RBdict):
            """ The command functions of the RB in PlotOptionsTypeFrame """
            self.TypesFrames[RBnameVar.get()].tkraise()
            self.activate_radio_button(RBnameVar, RBdict)

        self.PlotTypeRadiobuttons["Autocorrelation"].config(fg="green")

    def plot_options_autocorr(self):
        """ Defining the PlotOptionsAutocorrFrame children """
        l_text = "\nSpecify the number of the lags"
        label1 = tk.Label(self.PlotOptionsAutocorrFrame, text=l_text, font=LARGE_FONT)
        label1.pack(pady=10, padx=10)

        self.Edit_autoLag = tk.Entry(self.PlotOptionsAutocorrFrame, width=8)
        self.Edit_autoLag.pack()
        self.Edit_autoLag.insert(0, "40")

    def plot_options_corr(self):
        """ Defining the PlotOptionsCorrFrame children """
        self.CorrCategoryRadiobuttons = {}

        for cType in CategoriesList:
            self.CorrCategoryRadiobuttons[cType] = tk.Radiobutton(
                self.PlotOptionsCorrFrame,
                text=cType,
                font=NORMAL_FONT,
                variable=self.controller._corr_category,
                value=cType,
                command=lambda: self.activate_radio_button(
                    self.controller._corr_category, self.CorrCategoryRadiobuttons
                ),
            )

            self.CorrCategoryRadiobuttons[cType].pack(side="top", fill="both")

        self.CorrCategoryRadiobuttons["DBT"].config(fg="green")

        label2 = tk.Label(
            self.PlotOptionsCorrFrame,
            textvariable=self.controller._question,
            font=LARGE_FONT,
        )
        label2.pack(side="top", fill="both")

        self.Edit_tPeriod2_numb = tk.Entry(self.PlotOptionsCorrFrame, width=4)
        self.Edit_tPeriod2_numb.pack(side="top")
        self.Edit_tPeriod2_numb.insert(0, "1")

    def plot_options_blanc(self):
        """ Defining a BlancFrame (detailed explanation: line 516) """
        pass

    def plot_graph(self):
        """ Defining the PlotGraphFrame children """

        # matplotlib in the Tkinter application (ideas.md [1])
        canvas = FigureCanvasTkAgg(f, self.PlotGraphFrame)
        canvas.draw()
        canvas.get_tk_widget().pack(
            side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5
        )
        toolbar = NavigationToolbar2Tk(canvas, self.PlotGraphFrame)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def main():
    """The main function"""
    app = MeteorologyApp()
    app.geometry("1280x720")  # Size of the Tkinter window

    # Object of matplotlib animation, used to update Plot every time something has changed
    ani = animation.FuncAnimation(f, app.check_update, interval=500)
    app.mainloop()


if __name__ == "__main__":
    main()
