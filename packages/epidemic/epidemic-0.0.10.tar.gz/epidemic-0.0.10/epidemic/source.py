from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
from datetime import date
import math
import numpy as np
import matplotlib.pyplot as plt

import csv

from termcolor import colored
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

import requests


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


def train_epidemic(predict_evidence, year):
    """
    train the model for epidemic

    Parameters:
    predict_evidence
    predict (int): day to predict

    Returns:
    int: virus/infection/death predicted
    """

    request = requests.get('https://boyuan12.github.io/epidemic/epidemic.csv')
    wrapper = csv.reader(request.text.strip().split('\n'))

    evidence = []
    labels = []
    next(wrapper)

    for row in wrapper:
        # 1 = True, 0 = False

        if row[2] == 'True':
            if row[0] == str(year):
                return 1, 1, str(row[1])

            labels.append(1)
        else:
            if row[0] == str(year):
                return 1, 0, 'no'

            labels.append(0)

        population = float(row[3])
        climate_change = float(row[4])
        democracy_index = float(row[5])
        poverty = float(row[6])
        global_health = float(row[7])
        flight = float(row[8])

        evidence.append([population, climate_change,
                         democracy_index, poverty, global_health, flight])

    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=0.1
    )

    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, y_train)

    predictions = model.predict([predict_evidence])

    correct = round((y_test == predictions).sum() / len(y_test), 2)
    incorrect = round((y_test != predictions).sum() / len(y_test), 2)

    return correct, predictions[0], None


def Predict_Epidemic(year):

    population = Predict(year).population()
    climate_change = Predict(year).climate_change()
    democracy_index = Predict(year).democracy_index()
    poverty = Predict(year).poverty()
    global_health = Predict(year).global_health_gdp_average()
    flight = Predict(year).flights()
    correct, prediction, epi = train_epidemic(
        [population, climate_change, democracy_index, poverty, global_health, flight], year)
    return correct, prediction, epi

