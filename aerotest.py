### Tests aerospace library ###
import sys
# This file should be outside of the aerolibb library
# Change path depending on your own system
sys.path.insert(0, r"C:\Users\sheng\Dropbox\SG\Python\LIBRARIES\aerolibb") #the directory that contains my_pkg
import numpy as np
from aerolibb import framechange as fc
from aerolibb import propulsion as engine
from aerolibb import spacecraft

# create spacecraft
sc = spacecraft.Spacecraft("Juno", "Interplanetary")

# propulsion test
print("STARTING PROPULSION TEST")
sc.engine1 = sc.create_engine("Engine1", "Mono", thrust=.889, isp=150, masse=500) 
deltav, mi, mf, mp = sc.engine1.rocketeqn(mf=100, mi=1000)
sc.engine1.mo = 100
sc.engine1.printDesc()

print("Examine engine instances")
# my_engines = []
# for i in range(100):
    # my_objects.append(engine(i))

# # later
# for obj in my_objects:
    # print obj.type
# foo_vars = {id(instance): instance.foo for instance in A.instances}

# sc.engine1.oneaxismaneuver(np.pi/2, 500, 1.8, 2)

# sc.engine1.unloadrxn(27, 418.879, 2.134, 2)


# framechange test
print("STARTING FRAME CHANGE TEST")
DCM = np.matrix([[-0.0614637, 0.3985394, -0.9150894],[-0.7304249, 0.6068640, 0.3133615],[0.6802215, 0.6876644, 0.2538028]])
q = fc.dcm2q(DCM)
print(q)
DCM = fc.q2dcm(q)

psi, theta, phi = fc.dcm2euler(DCM)
DCM = fc.euler2dcm(psi, theta, phi)
print(DCM)

# rotate frame
print("Rotating position vector frame test:")
l = np.deg2rad(184.4152)
b = np.deg2rad(1.2689)
d = 5.45609173877203
rp = fc.rotate_sphe2rect(l, b, d)
print(rp)
# rsphere = fc.rotate_rect2sphe(rp)
# print(rsphere)

# rp = np.array([[1],[2],[3]])
print("Ready to rotate by Euler angles")
rp = rp.T
print(rp)

rpnew = fc.rotateDCM(DCM,rp)
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