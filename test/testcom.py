# Telecom Test
import sys
# This file should be outside of the aerolibb library
# Change path depending on your own system
sys.path.insert(0, r"C:\Users\sheng\Dropbox\SG\Python\LIBRARIES\aerolibb") #the directory that contains my_pkg
import numpy as np
from aerolibb import telecom as com

f = 8.4e9
Pmax = 500 # W
mmax = 150 # pounds
Amax = 50 # m

com = com.Telecom(f, Pmax, mmax, Amax)

com.calc_EIRP(com.f, com.mmax)