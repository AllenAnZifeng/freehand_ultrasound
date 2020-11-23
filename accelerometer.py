#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Allen(Zifeng) An
@course: 
@contact: anz8@mcmaster.ca
@file: accelerometer.py
@time: 2020/11/5 20:50
'''
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
g = 9.81 # gravitational constant
file = []
with open('accData.txt', 'r') as f:
    for line in f.readlines():
        file.append(line)

file = file[2:]
ax, ay, az, time_stamp = [], [], [], []
for i in range(len(file)):
    row = file[i].split()
    ax.append(float(row[2]))
    ay.append(float(row[3]))
    az.append(float(row[4]))
    time_stamp.append(float(row[1].split('.')[1]))

# print('ax',ax)
# print('time stamp',time_stamp)
# print('ay',ay)
# print('az',az)

continuous_time=[]
count=0
for i in range(len(time_stamp)-1):
    if time_stamp[i]<=time_stamp[i+1]:
        continuous_time.append(time_stamp[i]+count*1000)
    else:
        continuous_time.append(time_stamp[i]+count*1000)
        count += 1

# print('continuous_time',continuous_time)


# only for ax
velocity, displacement = 0, 0
v,d=[],[]
for i in range(len(ax)-1):
    dt = time_stamp[i+1]-time_stamp[i]
    if dt<=0:
        dt +=1000
    dt = dt/1000
    velocity += dt * ax[i] *g
    displacement += dt * velocity
    # displacement += velocity*dt+ 0.5*ax[i]*(dt)**2
    v.append(velocity)
    d.append(displacement)


print('total displacement',displacement)
# print('d',d)
# print('v',v)

ax = [a*g for a in ax]

fig, axis = plt.subplots()
axis.plot(continuous_time, ax[:-1],label='ax (m/s^2)')
axis.plot(continuous_time, v,label='velocity (m/s)')
# axis.plot(continuous_time,d,label='displacement (m)')

axis.set(xlabel='time (ms)', ylabel='y axis',
       title='Accelerometer Data Visualization')
axis.grid()

plt.legend()
plt.show()


