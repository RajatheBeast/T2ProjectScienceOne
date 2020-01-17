#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:20:05 2020
@author: raja
"""

import numpy as np
import matplotlib.pyplot as plt
import csv



L = 0.1 #lenth of the rod (in meters)
n = 7 #number of nodes
T0 = 23 #initial temperature at one end point
T1s = 200 #left boundary condition
T2s = 23 #right boundary condition
dx = L/n #Thickness of the wall divided by the number of nodes
alpha = 0.0001 #this is the thermal difusivity defined as thermal conductivity / (density (rho) * Cp)
t_final = 6000 #final time  keep as in integer for proper data collection
dt = 1 #the time intervals keep as an integer for proper data collection
showEvolve = False


x = np.linspace(dx/2, L-dx/2, n) # We will be plotting the temperature of space between each node
T = np.ones(n)*T0 #This is the starting temperature
dTdt = np.empty(n) #defining the temperature derivative

t = np.arange(0, t_final, dt) #time vector

'''These are the initial reading that we will determine from our tests
we can imput the 7 sensors readings as soon as the first one reaches
the desired temp (in this case 200 degrees C) and imput them here and 
see how it compares to the real deal!'''
T[0] = 200
T[1] = 180
T[2] = 150
T[3] = 100
T[4] = 95
T[5] = 0
T[6] = 0

#Lists that are used in csv files
time = []

temp0 = []
temp1 = []
temp2 = []
temp3 = []
temp4 = []
temp5 = []
temp6 = []


for j in range(1, len(t)): #Goes through each time and calculates the temperature at that node
    plt.clf()
    plt.ion()
    for i in range (1, n-1): #This loops through each spatial node and finds the derivative at that node
        dTdt[i] = alpha *(-(T[i]-T[i-1])/dx**2+(T[i+1]-T[i])/dx**2) #This is the approximation for every node that isnt on the boundary
        temp1.append(T[1])
        temp2.append(T[2])
        temp3.append(T[3])
        temp4.append(T[4])
        temp5.append(T[5])
    dTdt[0] = alpha *(-(T[0]-T1s)/dx**2+(T[1]-T[0])/dx**2) #Left boundary approximation T1s is the left boundary
    dTdt[n-1] = alpha *(-(T[n-1]-T[n-2])/dx**2+(T2s-T[n-1])/dx**2) #right boundary approximation T2s is the right boundary
    temp0.append(T[0])
    temp6.append(T[6])
    T = T + dTdt*dt
    time.append(j)
    

    if showEvolve == True:
        plt.figure(1)
        plt.plot(x, T)
        plt.axis([0, L, 0, T1s + 50])
        plt.xlabel('Distance (m)')
        plt.ylabel('Temperature (C)')
        #plt.legend(str(j*dt))
        plt.show()
        plt.pause(0.1) 

    
with open('model_data.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['time', 'temp0', 'temp1', 'temp2', 'temp3', 'temp4', 'temp5','temp6'])

    for i in range(0, (t_final/dt)-1):
        csv_writer.writerow([time[i],temp0[i],temp1[i],temp2[i],temp3[i],temp4[i],temp5[i],temp6[i]])


if showEvolve == True:
    plt.figure(1)
    plt.plot(x, T)
    plt.axis([0, L, 0, T1s + 50])
    plt.xlabel('Distance (m)')
    plt.ylabel('Temperature (C)')
    #plt.legend(str(j*dt))
    plt.show()
    plt.pause(0.1)



    

