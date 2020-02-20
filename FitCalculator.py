# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 21:49:30 2020

@author: justi
"""

import csv

# Data in both files should be normalized to start at T = 0s, and run at the same intervals for the same amount of time
CSV_DATA_FILE_NAME = "processed_data.csv" # Name of csv document with processed data
CSV_MODEL_FILE_NAME = "model_data.csv" # Name of the csv document with model data
names = ["Time","TempOne","TempTwo","TempThree","TempFour","TempFive","TempSix","TempSeven","Atmospheric"] # Array of names for columns
u_Temp = 0.125 # Temperature uncertainty
P = 2 # Number of perameters

def calcResiduals():
    sum_nor = [0,0,0,0,0,0,0] # Sum of all residuals squared
    csvDataFile = open(CSV_DATA_FILE_NAME, 'r', newline='') # Open csv files for reading
    csvModelFile = open(CSV_MODEL_FILE_NAME, 'r', newline='')
    csvDataReader = list(csv.DictReader(csvDataFile, fieldnames = names)) # Open proper readers
    csvModelReader = list(csv.DictReader(csvModelFile, fieldnames = names)) # Open proper readers
    num = 0 # Number of data points
    for i in range(0, len(csvDataReader)): # Iterate through rows
        for j in range (1,8): # Iterate through names of temperatures
            data = float(csvDataReader[i][names[j]]) # Get data value
            model = float(csvModelReader[i][names[j]]) # Get model value
            residual = (data - model) # Residual
            sum_nor[j-1] += (residual/u_Temp)**2 # Add to total residuals after processing
            num += 1
    csvDataFile.close() # Close files
    csvModelFile.close()
    return sum_nor, num

def calculateChiScore():
    sumResiduals, num = calcResiduals()
    chiScores = list() # List of x^2-scores
    for i in range(0,7): # Iterate through locations
        chiScores.append(sumResiduals[i]/(num-P)) # Calculate and add x^2 scores
    return chiScores

scores = calculateChiScore()
        