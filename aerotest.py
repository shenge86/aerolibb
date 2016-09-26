### Tests aerospace library ###
import sys
# This file should be outside of the aerolibb library
# Change path depending on your own system
sys.path.insert(0, r"C:\Users\sheng\Dropbox\SG\Python\LIBRARIES\aerolibb") #the directory that contains my_pkg
import numpy as np
# from aerolibb import propulsion
from aerolibb import framechange as fc
from aerolibb import spacecraft
# propulsion as aero

deltav = 3000
isp = 350
mi = 50000
# (mf, mp) = propulsion.rocketeqn(deltav, isp, mi)

# print(mf)
# print(mp)

# framechange test
DCM = np.matrix([[-0.0614637, 0.3985394, -0.9150894],[-0.7304249, 0.6068640, 0.3133615],[0.6802215, 0.6876644, 0.2538028]])
q = fc.dcm2q(DCM)
print(q)
DCM = fc.q2dcm(q)

psi, theta, phi = fc.dcm2euler(DCM)
DCM = fc.euler2dcm(psi, theta, phi)
print(DCM)

# rotate frame
rp = np.array([[1],[2],[3]])
rpnew = np.dot(DCM,rp)
print(rpnew)

rpnew = fc.rotate(q,rp)
print(rpnew)

# rp = np.array([[1], [1], [1]])
# rotMatrix = framechange.euler(np.pi/4, 0, 0)
# print(rotMatrix)
# print(rp)
# rs = np.dot(rotMatrix, rp)
# r2 = np.matrix([[1, 1, 1], [1, 2, 1]])
#rs = np.dot(r2,rp)

# rs = np.dot(rotMatrix, rp)
# print(rs)




# Test  SPACECRAFT#
'''
sc = spacecraft.Spacecraft('lunarcraft',1, 1000,1000,1000)
sc.printDesc()
rp = sc.define_position(1,1,1)
print("INITIAL CONFIG:")
sc.printDesc()
print(rp)

print("ROTATE TO NEW FRAME: ")
rp = sc.rotate_attitude(0,0,np.pi/4)

print("FINAL CONFIG:")
print("Positions are now defined relative to new frame.")
sc.printDesc()

#
print("Power Test: ")
sc.define_payload(100,1000)
sc.printDesc()

#
print("Engine Test: ")
sc.engine.name = "Unknown"
sc.engine.propellant_tank(sc.engine.massp)
sc.engine.printDesc()

sc.engine2 = sc.create_engine("BX2T", "Ion",isp=6000)
sc.engine2.printDesc()

sc.engine3 = sc.create_engine()
sc.engine3.printDesc()


# sc2 = spacecraft.spacecraft('suncraft',1000,1000,1000)
# sc2.engine.printDesc()


sc.solar1 = sc.create_solar("SunStar", size=100, efficiency=0.97)
sc.solar1.calc_size(sc.solar1.power, 300,0.96)
sc.solar1.printDesc()
'''