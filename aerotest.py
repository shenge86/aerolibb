### Tests aerospace library ###
import sys
# This file should be outside of the aerolibb library
# Change path depending on your own system
sys.path.insert(0, r"C:\Users\sheng\Dropbox\SG\Python\LIBRARIES\aerolibb") #the directory that contains my_pkg
import numpy as np
# from aerolibb import propulsion
# from aerolibb import framechange
from aerolibb import spacecraft
# propulsion as aero

deltav = 3000
isp = 350
mi = 50000
# (mf, mp) = propulsion.rocketeqn(deltav, isp, mi)

# print(mf)
# print(mp)


# rp = np.array([[1], [1], [1]])
# rotMatrix = framechange.euler(np.pi/4, 0, 0)
# print(rotMatrix)
# print(rp)
# rs = np.dot(rotMatrix, rp)
# r2 = np.matrix([[1, 1, 1], [1, 2, 1]])
#rs = np.dot(r2,rp)

# rs = np.dot(rotMatrix, rp)
# print(rs)

# Test #
sc = spacecraft.spacecraft('lunarcraft',1, 1000,1000,1000)
sc.printDesc()
rp = sc.definePosition(1,1,1)
print("INITIAL CONFIG:")
sc.printDesc()
print(rp)

print("ROTATE TO NEW FRAME: ")
rp = sc.rotateAttitude(0,0,np.pi/4)

print("FINAL CONFIG:")
print("Positions are now defined relative to new frame.")
sc.printDesc()

#
print("Power Test: ")
sc.definePayload(100,1000)
sc.printDesc()

#
print("Engine Test: ")
sc.engine.name = "Unknown"
sc.engine.propellantTank(sc.engine.massp)
sc.engine.printDesc()

sc.engine2 = sc.createEngine("BX2T", "Ion",6000)
sc.engine2.printDesc()

sc.engine3 = sc.createEngine()
sc.engine3.printDesc()


# sc2 = spacecraft.spacecraft('suncraft',1000,1000,1000)
# sc2.engine.printDesc()
