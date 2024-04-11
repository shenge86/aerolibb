# Orbital Mechanics Problems
import numpy as np
from aerolibb import orbital as orb

mu = 398600 # km**3/s**2
# 3.1
R0 = 6378.14 # km
e = 0 # circular orbit
theta = 30 # true anomaly (doesn't matter for circle since velocity is same throughout!)

# 1.0 find period of Earth orbit at geosynchronous orbit



r, v, gamma = orb.findrv(R0, e, theta)
print(v)

# 3.2
v = 10.7654
r = 1500 + R0
gamma = 23.174 # degrees
gamma = np.deg2rad(gamma)

a, e, theta, energy, H = orb.findea(v, r, gamma)

# 3.3
rp = 6500
ra = 60000
r = R0 + 500

e = orb.finderpra(rp, ra)
theta = orb.findtheta(rp,r,e)
print(e)
print(np.rad2deg(theta))

# 3.4
r1 = orb.AU
r2 = 39.5574 * r1
theta1 = np.deg2rad(16.26)
theta2 = np.deg2rad(169.66)

e, rp = orb.finder1r2(r1,r2,theta1,theta2)
print(e)
print(rp)

# 3.5
print("Problem 3.5")
print("Magellan orbiting about Venus starts at a true anomaly of 280 degrees. What are the altitude, flight path angle, velocity, and time since periapsis at this point?")
a = 10424.1
e = 0.39433
theta = np.deg2rad(280)

orb.muE = 324858.81 # change mu to that of Venus's
r,v,gamma = orb.findrv(a,e,theta)
n,P,E,t = orb.tof_ellipse(a,e,theta)
print(r)
print(v)
print(np.rad2deg(gamma))
print(E)
print(n)
print(t)
print(P)

# 3.6
print("Problem 3.6")
print("What is the escape velocity from the surface of the moon?")
orb.muE = 4902.8
R0 = 1738
vesc = orb.escapev(R0)
print(vesc)

# 3.7
print("3.7")
print("Elements of departure hyperbola of Viking I Mars Lander were as such. What C3 value is provided by the lander's Titan IIIE LV?")
orb.muE = 398600.4 # back to Earth's
a = 18849.7

vinf, C3 = orb.excessv(a)
print(C3)

# 3.8
print("3.8")
print("Voyager 2 flew past Neptune on a hyberolic orbit. What was the time since periapsis of encounter?")
a = 19985
e = 2.45859
r = 354600

theta = np.arccos(abs(a) * (e ** 2 - 1) / (r * e) - (1/e))
print(theta)

r,v,gamma = orb.findrv(a, e, theta)
n,F,t = orb.tof_hyperbola(a, e, theta)


print(n)
print(t)

# 3.11
print("3.11")
print("Direct circular Earth orbit of radius 9100 km and a final coplanar elliptical orbit with e = 0.1, rp = 9000 km. What velocity change is needed?")




deltav = orb.mv_coplanar(vi,vf,alpha)
print(deltav)


# Other
theta = orb.eccentric2true(1,np.pi/2)