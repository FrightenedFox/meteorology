# **Meteorology**  
*By Vitalii Morskyi*  
  
***
  
This project is a part of the curriculum in "Wstęp do programowania"
of the Polytechnic University of Rzeszów, Poland.  
  

## The purpose of the project  
  
The aim of the project was creating an application which would be able to show and plot some statistics data, such as standard deviation, variance, correlation, autocorrelation, etc., about weather characteristics in any time period of the year.
  
  
## Results  
  
In this chapter, I would like to demonstrate some screen shots of the application.  
  
After loading the file, the application shows some summary about the data. A user is able to choose which type of data and time period he is interested in. The example of the summary statistics is shown on the image below.
![Statistics page](/Images/statistics.png)  
  
***  
  
The user is also able to choose *Plot* page, where the plots are created. The default plot is an autocorrelation plot. The example of the autocorrelation function graph can be found on the screen shot below.  
![Autocorrelation function](/Images/autocorrelation.png)  
  
***
  
Except from the default graph type, which is autocorrelation, there are two more types, namely the correlation function and the data plot.
There are two images below, on which the outcome of the program is shown.
![Correlation function](/Images/correlation.png)
![Plot data](/Images/plot_data.png)

  
## Future ideas  
  
Here I would like to mention some improvements which can be implemented to make the use of the application a lot more convenient.  
  
It would be great to:  
 - create program's own exceptions, such as:  
 	* given file is empty  
 	* the structure of an input data appears to be different from the common one  
 	* some lines are damaged  
 - be prepared for an empty line  
 - forbid to input more lags then there are data points  
 - create a 'Help' menu  
 - improve axes ticks  
  
## Executing info  
  
The GUI version of an application is held in the file `gui.py`.  
Some basic operations on the database in the console are provided in the script in the file `data.py`.  

To run the application properly, three Python packages (`pandas`, `numpy` and `matplotlib`) have to be installed on your PC.  
[An official guide of installing `pandas`](https://pandas.pydata.org/getting_started.html)  
[An official guide of installing `numpy`](https://numpy.org/install/)  
[An official guide of installing `matplotlib`](https://matplotlib.org/3.1.1/users/installing.html)  
  
The other information about the files in the repository:
 - /Data - the main database is held in that folder;  
 - /Images - images used in the README.md file are stored;  
 - Ideas.md - some useful info and tutorials used to make this project are presented;  
 - time-arrays.py - the script for manual file loading and preprocessing;  


  
## Data  
  
### Archive  

The archive with the data used in this project can be reached by [the following link](https://archiwum.miir.gov.pl/media/51867/wmo122950iso.txt).  
  
### Data explanation  

Some notes about what the data in the archive mean are held on [the following web page](https://archiwum.miir.gov.pl/strony/zadania/budownictwo/charakterystyka-energetyczna-budynkow/dane-do-obliczen-energetycznych-budynkow-1/#Typowe%20lata%20meteorologiczne%20i%20statystyczne%20dane%20klimatyczne%20do%20oblicze%C5%84%20energetycznych%20budynk%C3%B3w).  
  
The meaning of the abbreviations are given below:  

	N 	- Number of the hour in the year
	M 	- Month
	D 	- Day
	H 	- Local time
	DBT - Dry bulb temperature 
	RH 	- Relative humidity
	HR 	- Humidity ratio (specific humidity)
	WS 	- Wind speed
	WD 	- Wind direction
	ITH - Total Solar Radiation
	IDH - Direct (beam) solar radiation
	ISH	- Diffuse solar radiation
	TSKY- Temperature of the Sky
	N_0
	N_30, NE_30, E_30....,N_45, NE_45...., N_60...., N_90
  