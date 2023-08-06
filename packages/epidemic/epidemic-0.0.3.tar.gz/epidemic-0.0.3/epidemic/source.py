from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
from datetime import date
import math
import numpy as np
import matplotlib.pyplot as plt

history = [2009, 2013, 2014, 2015, 2016, 2020]

def linear_regression(input_i, output_o, return_val):
    """
    linear regression, give two array and a value to predict it's output.

    Parameters:
    input_i (list): list with input
    output_o (list): list with output
    return_val (int): the input to predict output with

    Returns:
    float: the predicted value based on the input (return_val), round to 3 decimal degit if needed.
    """
    input_i = np.array(input_i, dtype=float)
    output_o = np.array(output_o, dtype=float)
    m, b = np.polyfit(input_i, output_o, 1)
    return round(int(m) * int(return_val) + int(b), 3)


def graph(input_i, output_o):
    """
    graph, give two array and return a graph with all datapoint and line of best fit.
    
    Parameters: 
    input_i (list): list with input
    output_o (list): list with output
    
    Returns:
    graph: a graph contained with all datapoint provided and a line of best fit
    """
    input_i = np.array(input_i, dtype=float)
    output_o = np.array(output_o, dtype=float)
    m, b = np.polyfit(input_i, output_o, 1)
    plt.plot(input_i, output_o, 'o')
    plt.plot(input_i, m*output_o + b)
    plt.show()

class Predict:
    """ 
    This is a class for predicting key information/cause for a epidemic. 
      
    Attributes: 
        year (int): The year that you want to estimate the value
    """
    def __init__(self, year):
        """ 
        The constructor for Predict class. 
  
        Parameters: 
           year (int): The year that you want to estimate the value
        """
        self.year = year

    def population(self):
        """ 
        The function to predict population. 
  
        Returns: 
            int: predicted population
        """
        return linear_regression([1500, 1650, 1750, 1804, 1850, 1900, 1927, 1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 1999, 2006, 2009, 2011, 2020], [450000000, 500000000, 700000000, 1000000000, 1200000000, 1600000000, 2000000000, 2550000000, 2800000000, 3000000000, 3300000000, 3700000000, 4000000000, 4500000000, 4850000000, 5300000000, 5700000000, 6000000000, 6500000000, 6800000000, 7000000000, 7800000000], self.year)
        
    def climate_change(self):
        """ 
        The function to predict abnormal temperature. 
  
        Returns: 
            float: predicted abnormal temperature
        """
        # Source: https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt
        return linear_regression([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019], [0.65, 0.66, 0.69, 0.74, 0.78, 0.83, 0.87, 0.91, 0.95, 0.98], self.year)

    def democracy_index(self):
        """ 
        The function to predict democracy index.
  
        Returns: 
            float: predicted democracy index
        """
        # Source: https://en.wikipedia.org/wiki/Democracy_Index#Democracy_Index_by_region
        return linear_regression([2006, 2008, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], [5.52, 5.55, 5.46, 5.49, 5.52, 5.53, 5.55, 5.55, 5.52, 5.48, 5.48], self.year)

    def poverty(self):
        """ 
        The function to predict abnormal temperature. 
  
        Returns: 
            float: predicted abnormal temperature
        """
        # Source: https://data.worldbank.org/topic/poverty
        return linear_regression([1999, 2005, 2008, 2010, 2011, 2012, 2013, 2015], [25.5, 20.7, 18.2, 15.7, 13.7, 12.8, 11.2, 10], self.year)

    def gdp(self):
        """ 
        The function to predict world GDP average. 
  
        Returns: 
            float: predicted GDP average
        """
        # Source: https://www.worldometers.info/gdp/, unit: Trillion
        return linear_regression([2010, 2011, 2012, 2013, 2014, 2015, 2016], [66.04, 73.37, 75.06, 77.22, 73.73, 75.83, 77.80], self.year)

    def life_expectancy(self):
        """ 
        The function to predict world average life expectancy. 
  
        Returns: 
            float: predicted life expectancy
        """
        # Source: https://data.worldbank.org/indicator/SP.DYN.LE00.IN
        return linear_regression([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017], [70.556, 70.884, 71.172, 71.462, 71.742, 71.948, 72.182, 72.383], self.year)

    def global_health_gdp_average(self):
        """ 
        The function to predict abnormal temperature. 
  
        Returns: 
            float: predicted abnormal temperature
        """
        # Source: https://www.healthsystemtracker.org/chart-collection/health-spending-u-s-compare-countries/#item-since-1980-the-gap-has-widened-between-u-s-health-spending-and-that-of-other-countries___2018
        return linear_regression([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017], [10, 10.11, 10.24, 10.46, 10.52, 10.57, 10.62, 10.54], self.year)

    def flights(self):
        """ 
        The function to predict global flights count.
  
        Returns: 
            float: predicted flights count
        """
        # Source: https://www.statista.com/statistics/564769/airline-industry-number-of-flights/
        return linear_regression([2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018], [27.8, 30.1, 31.2, 32, 33, 34, 35.2, 36.4, 38.1], self.year)


def Predict_Epidemic():
    """
    Predict_Epidemic, predict when will next epidemic happen
    
    Returns:
    graph: a graph contained with all datapoint provided and a line of best fit
    """
    year = date.today().year
    probability = {}

    for i in range(10):

        climate_change = Predict(year).climate_change() / Predict(year-1).climate_change() # 20%
        if climate_change < 1:
            climate_change = -climate_change

        democracy_index = Predict(year).democracy_index() / Predict(year).democracy_index() #10%
        if democracy_index > 1:
            democracy_index = -democracy_index

        poverty = Predict(year).poverty() / Predict(year-1).poverty() # 10%
        if poverty < 1:
            poverty = -poverty

        gdp = Predict(year).gdp() / Predict(year-1).gdp() # 10%
        if gdp > 1:
            gdp = -gdp

        life_expectancy = Predict(year).life_expectancy() / Predict(year-1).life_expectancy() # 10%
        if life_expectancy > 1:
            life_expectancy = -life_expectancy

        global_health_gdp_average = Predict(year).global_health_gdp_average() / Predict(year-1).global_health_gdp_average() # 30 %
        if global_health_gdp_average > 1:
            global_health_gdp_average = -global_health_gdp_average

        flights = Predict(year).flights() # 10%
        if poverty > 1:
            poverty = -poverty

        score = climate_change * 0.2 + democracy_index * 0.1 + poverty * 0.1 + gdp * 0.1 + life_expectancy * 0.1 + global_health_gdp_average * 0.3 + flights * 0.1
        try:
            probability[year] = score + probability[year-1]
        except KeyError:
            probability[year] = 50 + score
        year+=1

    for key in probability:
        if probability[key] > 70:
            return key


def Predict_Virus_Growth(day1, day2, day3, day4, day5, predict):
    """
    Predict_Virus_Growth, predict virus/infection/death growth in given day. Use latest 5 consecutive days of data

    Parameters:
    day1 (int): day 1 infection/death data
    day2 (int): day 2 infection/death data
    day3 (int): day 3 infection/death data
    day4 (int): day 4 infection/death data
    day5 (int): day 5 infection/death data
    predict (int): day to predict

    Returns:
    int: virus/infection/death predicted
    """
    # expoential
    b = day2 / day1
    a = day1
    x = 4

    expo = a * (b ** x)

    # linear
    line = linear_regression([1, 2, 3], [day1, day2, day3], 5)

    if abs(expo - day5) > abs(line - day5):
        return int(a * (b ** predict))
    else:
        return int(linear_regression([1, 2, 3, 4, 5], [day1, day2, day3, day4, day5], predict))