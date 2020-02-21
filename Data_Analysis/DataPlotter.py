# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 22:20:35 2020

@author: justi
"""

import csv
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

CSV_FILE_NAME = "rawdata10s.csv" # Name of csv document
names = ["Time","TempOne","TempTwo","TempThree","TempFour","TempFive","TempSix","TempSeven","Atmospheric"] # Array of names for columns

position = [] ## x, y, and z axis
time = []
temperature = []

def fillAxes():
    
    csvFile = open(CSV_FILE_NAME, 'r', newline='') # Open csv file for reading
    csvReader = csv.DictReader(csvFile, fieldnames = names) # Open proper reader
    skip = 0 # Counter to skip first two rows
    for row in csvReader: # Iterate through rows
        if skip >= 2:
            for i in range (1,8): # Iterate through names
                position.append(i) # Store readings
                time.append(float(row["Time"]))
                temperature.append(float(row[names[i]]))
        skip += 1
    csvFile.close() # Close file
    
def plot():
    fig = plt.figure() # I don't know why this is needed
    axes = fig.add_subplot(111, projection = "3d") # 3d axes in a variable!
    axes.scatter(position,time,temperature) # And plot
    
fillAxes()
plot()
