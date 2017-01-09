# Power Test
import sys
# This file should be outside of the aerolibb library
# Change path depending on your own system
sys.path.insert(0, r"C:\Users\sheng\Dropbox\SG\Python\LIBRARIES\aerolibb") #the directory that contains my_pkg
import numpy as np
from aerolibb import power as pow

# calculate power required
pw = pow.Power(0,1000,5)
power = pw.powermax

# generate solar panel
# solarpanel = pow.Solar(name, size, density, powerlab, efficiency)

# solar panels
solar1 = pow.showSolarProducts()
solar1.calc_size(power)
solar1.printDesc()

# batteries
battery1 = pow.showBatteryProducts()
h = 1000
beta = 0
eclipsetime = battery1.calc_eclipsetime(h,beta)
battery1.calc_mass(power, eclipsetime)
battery1.printDesc()