#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:20:05 2020
@author: raja
"""

import numpy as np
import matplotlib.pyplot as plt
import csv



L = 0.3048 #lenth of the rod (in meters)
n = 56 #number of nodes
T0 = 331.96 #initial temperature at one end point
T1s = 280.15 #left boundary condition
T2s = 280.15 #right boundary condition
dx = L/n #Thickness of the wall divided by the number of nodes
alpha = .00004891 #this is the thermal difusivity defined as thermal conductivity / (density (rho) * Cp)
alpha_air = .000020
t_final = 332.826 #final time keep as in integer for proper data collection
dt = .01 #the time intervals keep as an integer for proper data collection
showEvolve = False


x = np.linspace(dx/2, L-dx/2, n) # We will be plotting the temperature of space between each node
T = np.ones(n)*T0 #This is the starting temperature
dTdt = np.empty(n) #defining the temperature derivative

t = np.arange(0, t_final, dt) #time vector

'''These are the initial reading that we will determine from our tests
we can imput the 7 sensors readings as soon as the first one reaches
the desired temp (in this case 200 degrees C) and imput them here and 
see how it compares to the real deal!'''
T0 = T0
T1 = 314.09
T2 = 302.90
T3 = 294.84
T4 = 289.4
T5 = 285.96
T6 = 284.65

for i in range(0,7):
    T[i],T[i+7],T[i+14],T[i+21],T[i+28],T[i+35],T[i+42],T[i+49] = T0,T1,T2,T3,T4,T5,T6,T6


#Lists that are used in csv files
time = []

temp0 = []
temp1 = []
temp2 = []
temp3 = []
temp4 = []
temp5 = []
temp6 = []
plotTime = []


data_times = list()
skip = 0
first_time = 0
with open('data.csv', 'r', newline = '') as data_file:
    csvReader = csv.DictReader(data_file, fieldnames=["Time","TempOne","TempTwo","TempThree","TempFour","TempFive","TempSix","TempSeven","Atmospheric"])
    for row in csvReader:
        if skip == 2:
            first_time = float(row["Time"])/1000
        if not (skip < 2):
            data_times.append((float(row["Time"])/1000) - first_time)
        skip += 1

k = 0
for j in range(0, len(t)): #Goes through each time and calculates the temperature at that node
    plt.clf()
    plt.ion()
    for i in range (1, n-1): #This loops through each spatial node and finds the derivative at that node
        dTdt[i] = alpha *(-(T[i]-T[i-1])/dx**2+(T[i+1]-T[i])/dx**2) #This is the approximation for every node that isnt on the boundary
            
    dTdt[0] = alpha_air *(-(T[0]-T1s)/dx**2+(T[1]-T[0])/dx**2) #Left boundary approximation T1s is the left boundary
    dTdt[n-1] = alpha_air *(-(T[n-1]-T[n-2])/dx**2+(T2s-T[n-1])/dx**2) #right boundary approximation T2s is the right boundary

    T = T + dTdt*dt
    time.append(j*dt)

    if round(time[j], 2) == round(data_times[k], 2):
        temp0.append(T[6])
        temp1.append(T[13])
        temp2.append(T[20])
        temp3.append(T[27])
        temp4.append(T[34])
        temp5.append(T[41])
        temp6.append(T[47])
        plotTime.append(j*dt)
        k += 1
    
    if k == len(data_times):
        break

    if showEvolve == True:
        plt.figure(1)
        plt.plot(x, T)
        plt.axis([0, L, 0, 400])
        plt.xlabel('Distance (m)')
        plt.ylabel('Temperature (C)')
        #plt.legend(str(j*dt))
        plt.show()
        plt.pause(0.1) 


with open('model_data.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['time (s)', 'temp0', 'temp1', 'temp2', 'temp3', 'temp4', 'temp5','temp6'])

    for i in range(0, len(temp0)):
        csv_writer.writerow([plotTime[i],temp0[i],temp1[i],temp2[i],temp3[i],temp4[i],temp5[i],temp6[i]])


if showEvolve == True:
    plt.figure(1)
    plt.plot(x, T)
    plt.axis([0, L, 0, 400])
    plt.xlabel('Distance (m)')
    plt.ylabel('Temperature (C)')
    #plt.legend(str(j*dt))
    plt.show()
    plt.pause(0.1)



    

