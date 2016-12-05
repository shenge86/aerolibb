# Power Test
import sys
# This file should be outside of the aerolibb library
# Change path depending on your own system
sys.path.insert(0, r"C:\Users\sheng\Dropbox\SG\Python\LIBRARIES\aerolibb") #the directory that contains my_pkg
import numpy as np
from aerolibb import power as pow


# generate solar panel
# solarpanel = pow.Solar(name, size, density, powerlab, efficiency)

# Show list of solar products
solar1 = pow.showSolarProducts()
power = 3000 # watts
solar1.calc_size(power)
solar1.printDesc()