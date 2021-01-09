#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Allen(Zifeng) An
@course: 
@contact: anz8@mcmaster.ca
@file: accelerometer.py
@time: 2020/11/5 20:50
'''

import matplotlib.pyplot as plt
import numpy as np
import scipy.io



g = 9.81 # gravitational constant
file = []
with open('accData_10K.txt','r') as f:
    for line in f.readlines():
        file.append(line)

file = file[2:]
ax, ay, az, time_stamp = [], [], [], []


for i in range(len(file)):
    row = file[i].split()

    ax.append(float(row[2])*g)
    ay.append(float(row[3])*g)
    az.append(float(row[4])*g)
    time = row[1].split(':')

    # int((time[0] * 60 ** 2 + time[1] * 60 + time[0]) * 1000)
    time_stamp.append(int((float(time[0]) * 60 ** 2 + float(time[1]) * 60 + float(time[2])) * 1000))


# only for ax
velocity, displacement = 0, 0
v,d=[0],[0]
for i in range(len(ax)-1):
    dt = time_stamp[i+1]-time_stamp[i]

    velocity += dt * ax[i]
    displacement += dt * velocity
    # displacement += velocity*dt+ 0.5*ax[i]*(dt)**2
    v.append(velocity/1000)
    d.append(displacement/1000)


print('total displacement',displacement)
# print('d',d)
# print('v',v)

scipy.io.savemat('accData_10K.mat', mdict={'time': time_stamp,'ax':ax,'ay':ay})

fig, axis = plt.subplots()
axis.plot(time_stamp, ax,label='ax (m/s^2)')
axis.plot(time_stamp, v,label='velocity (m/s)')
# axis.plot(time_stamp,d,label='displacement (m)')

axis.set(xlabel='time (ms)', ylabel='y axis',
       title='Accelerometer Data Visualization')
axis.grid()

plt.legend()
plt.show()

