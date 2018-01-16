# Power Test
import sys
# This file should be outside of the aerolibb library
# Change path depending on your own system
sys.path.insert(0, r"C:\Users\sheng\Dropbox\SG\Python\LIBRARIES\aerolibb") #the directory that contains my_pkg
import numpy as np
from aerolibb import power as pow
from aerolibb import propulsion as prop
from aerolibb import orbital as orb

# generate propulsion
(ids,names,types,isps,thrusts,masses,subtypes,propellants) = prop.showEngines()
engine1 = prop.chooseEngines(ids,names,types,isps,thrusts,masses,subtypes,propellants)


print("USER INPUTS")
# default parameters if nothing is given
deltai = 30 # inclination change (degrees)
deltai = np.deg2rad(deltai)
v0 = 7.726e3
vf = 3.075e3
mpayload = 1000 # kg
mf = engine1.me + mpayload # kg

# deltai = input("Input inclination change: ")
# v0 = input("Input initial velocity: ")
# vf = input("Input final velocity: ")
# mpayload = input("Input payload mass: ")

beta0 = orb.mv_coplanar(v0,vf,deltai)
print(beta0)

# ion thrusters use continuous thrust maneuvers
if (engine1.type == "electric"):
    (deltav, t) = orb.deltav_lowthrust(beta0,v0,deltai,engine1.thrust)
    print("Delta v is " + str(deltav) + " m/s")
else:
    deltav = orb.deltav_coplanar(v0,vf,deltai)
    print("Delta v is " + str(deltav) + " m/s")

kwargs = {'deltav': deltav,'mf': mf}

engine1.rocketeqn(**kwargs)

engine1.printDesc()



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
