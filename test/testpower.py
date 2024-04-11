# Power Test
import sys
# This file should be outside of the aerolibb library
# Change path depending on your own system
sys.path.insert(0, r"C:\Users\sheng\Dropbox\SG\Python\LIBRARIES\aerolibb") #the directory that contains my_pkg
import numpy as np
from aerolibb import power as pow
from aerolibb import propulsion as prop
from aerolibb import orbital as orb
from aerolibb import myconstants

# generate propulsion
(ids,names,types,isps,thrusts,masses,subtypes,propellants) = prop.showEngines()
engine1 = prop.chooseEngines(ids,names,types,isps,thrusts,masses,subtypes,propellants)

print("===========")
print("USER INPUTS")
print("===========")
h = 200 # km (altitude)
r1 = myconstants.rE
r2 = (myconstants.rE + h)

print("Initial orbital radius: " + str(r1) + " km")
print("Final orbital radius: " + str(r2) + " km \n")

# default parameters if nothing is given
deltai = 0 # inclination change (degrees)
deltai = np.deg2rad(deltai)
# v0 = 7.726e3
# vf = 3.075e3
mpayload = 280 # kg
mf = engine1.me + mpayload # kg

# deltai = input("Input inclination change: ")
# v0 = input("Input initial velocity: ")
# vf = input("Input final velocity: ")
# mpayload = input("Input payload mass: ")

print("ORBITAL MECHANICS CALCULATIONS")
if (engine1.type == "electric"):
    # ion thrusters use continuous thrust maneuvers
    (deltav, t) = orb.deltav_lowthrust(beta0,v0,deltai,engine1.thrust)
    print("Using low thrus manuever: ")
    print("Delta v is " + str(deltav) + " m/s")
else:
    print("Assume impulsive maneuver: ")
    (deltav,t) = orb.deltav_hohmann(r1,r2)
    deltav = deltav
    # deltav = orb.deltav_coplanar(v0,vf,deltai) + deltav
    print("Delta v is " + str(deltav) + " m/s")

# beta0 = orb.mv_coplanar(v0,vf,deltai)
# print(beta0)
print("\nPROPULSION CALCULATIONS")
kwargs = {'deltav': deltav,'mf': mf}

engine1.rocketeqn(**kwargs)

engine1.printDesc()

print("=================")
print("OTHER INFORMATION")
print("=================")
# calculate ratios
# An optimal rocket maximizes piratio
# Also, lower epsratio is good
piratio = mpayload / engine1.mi
epsratio = engine1.me / (engine1.me + engine1.mp)
twratio = engine1.thrust / (engine1.mi * myconstants.g) # this g assumes that of Earth

print("Payload ratio: " + str(piratio))
print("Structural ratio: " + str(epsratio))
print("Thrust to weight ratio: " + str(twratio))
print("Please note that to enter orbit, the thrust to weight ratio must be greater than 1.")
print("If already in orbit, the thrust to weight ratio can be anything.")

# calculate power required
# pw = pow.Power(0,10000,5)
# power = pw.powermax

# # generate solar panel
# # solarpanel = pow.Solar(name, size, density, powerlab, efficiency)

# # solar panels
# solar1 = pow.showSolarProducts()
# solar1.calc_size(power)
# solar1.printDesc()

# # batteries
# battery1 = pow.showBatteryProducts()
# h = 1000
# beta = 0
# eclipsetime = battery1.calc_eclipsetime(h,beta)
# battery1.calc_mass(power, eclipsetime)
# battery1.printDesc()
