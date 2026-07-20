# -*- coding: utf-8 -*-
import numpy as np
"""
@author: Shen Ge
@name: Surface Hopping Calculations

@description:
Calculates optimal trajectory based on constraints for surface hops.

@version:
  24 NOV 2021 Numerically integrate.
  18 NOV 2021 Use sympy for integrations
  7 NOV 2021 Creation
"""
from sympy import *

#%% constants
g = -9.8/6 # m/s^2 (lunar gravity)
m0 = 20     # kg (initial mass of vehicle)
isp = 100 # seconds (engine efficiency)
ve = 9.8*isp # m/s (exhaust velocity)

# Thrust
Tmax = 100 # newtons (maximum thrust during flight)
Tnom = Tmax*0.9 # newtons
Tmin = 0.1*Tmax   # newtons (minimum thrust during flight)

# Pitch rate (maximum)
pitch_rate_max = 10 # degrees / s

# what we can control is the following:
# thrust magnitude
# pitch angle

if __name__ == "__main__":
    # Timestep
    dt = 1 # timestep in seconds

    #%% CONSTRAINTS
    # flight distance constraint (downtrack)
    x0 = 0 # initial
    xf = 89.22 # final distance (target)
    y0 = 0
    yf = 0 # final relative height (prior to vertical descent)

    print('Ready!')
    ets = np.arange(0,100,1)
    a = np.zeros(100)
    ax = np.zeros(100)
    ay = np.zeros(100)
    vx = np.zeros(100)
    vy = np.zeros(100)
    rx = np.zeros(100)
    ry = np.zeros(100)
    m = m0*np.ones(100)
    T = Tnom*np.ones(100)
    pitch = np.zeros(100)
    # pitch angle from vertical
    # 90 degrees will be flying horizontal towards the landing site
    # 0 degrees will be initial starting (vertical straight down)
    # 180 degrees should be impossible!
    # -90 degrees means thrusting opposite direction of landing site
    # can only vary between -90 and 90 degrees

    print('Initial control state: ')
    T[0] = Tnom
    pitch[0] = 0

    print('Initial conditions: ')
    a[0] = T[0]/m0 # m/s^2
    ax[0] = a[0]*np.sin(pitch[0])
    ay[0] = a[0]*np.cos(pitch[0])
    vx[0] = 0
    vy[0] = 0
    rx[0] = 0
    ry[0] = 0

    # Note that thrust and pitch are the control variables
    while i < len(ets):



    # propagate states
    i = 1
    while i < len(ets):
        print('Epoch: ', ets[i])
        vx[i] = vx[i-1] + dt*ax[i-1]
        vy[i] = vy[i-1] + dt*ay[i-1]
        rx[i] = rx[i-1] + dt*vx[i-1] + 0.5*(ax[i]**2)
        ry[i] = ry[i-1] + dt*vy[i-1] + 0.5*(ay[i]**2)

        # update mass, thrust acceleration for next time step
        mdot = T[i]/ve
        m[i] = m[i-1] - mdot*dt
        a[i] = T[i] / m[i]
        ax[i] = a[i]*np.sin(pitch[i])
        ay[i] = a[i]*np.cos(pitch[i])-g

        i+=1

    print('Final conditions: ')
    print('rx: ', rx[-1])
    print('ry: ', ry[-1])
    print('vx: ', vx[-1])
    print('vy: ', vy[-1])
    print('ax: ', ax[-1])
    print('ay: ', ay[-1])
    # k1,k2,k3,k4 = symbols('k1 k2 k3 k4')
    # t = Symbol('t',positive=True)
    # ux = (k3+k4*t)*cos(k1+k2*t)
    # vx = integrate(ux,t)
    # print(vx)

    # x = x0
    # pitch = pitch0
    # vxprevious = vx0
    # while x < xf:
    #     t+=dt
    #     ax    = amax*np.sin(pitch)
    #     vx    = vxprevious+(ax*dt)
    #     rx    = ax*
    #     ay    = amax*np.cos(pitch)
    #
    #     # set everything up for next loop
    #     vxprevious = vx
    #     # prints
    #     print(vx)
    #     print(rx)
