import numpy as np
import myconstants

# orbital mechanics functions
# modified May 2019
# astrodynamics constants
global muE, AU, sc
rE = myconstants.rE
iE = myconstants.iE
muE = myconstants.muE
AU = myconstants.AU
sc = myconstants.solarconstant

# Please note:
# 1. All angles are in radians.
# 2. All mu are by default Earth gravitational parameter

# ALL CONIC SECTIONS
def findea(v, r, gamma):
	''' Define an orbit with known position, velocity, and flight path angle at a certain time.
	Inputs:
		v (velocity)
		r (position)
		gamma (flight path angle)
	Outputs:
		a (semimajor axis)
		e (eccentricity)
		theta (true anomaly in radians) (note: this  changes over time as object moves)
		energy (energy of orbit)
		H (angular momentum)
	'''
	energy = v ** 2 / 2 - muE / r
	print("Energy is " + str(energy))
	if energy != 0: # if it is not a parabola
		a = -muE / (2 * energy)
		H = r * v * np.cos(gamma)
		e = np.sqrt(1 - H ** 2 / (muE * a))

	print("a is " + str(a))
	print("H is " + str(H))
	print("e is " + str(e))


	if e == 0:
		theta = "Does not exist since it is a circle"
	elif e < 1:
		print("Elliptical orbit")
		theta = np.arccos(a * (1 - e ** 2) / (r * e) - (1/e))
	elif e > 1:
		print("Hyberpolic orbit")
		theta = np.arccos(abs(a) * (e ** 2 - 1) / (r * e) - (1/e))
		print("theta is: " + str(theta))
	else: # parabola
		print("Parabolic orbit")
		a = "infinity"
		e = 1
		theta = np.arccos((2 * rp - r) / r)

	return a, e, theta, energy, H

def findrv(a, e, theta):
	''' With a defined orbit of a and e, and knowing the true anomaly (theta), find certain parameters.
	Inputs:
		a (semimajor axis in m)
		e (eccentricty)
		theta (true anomaly in radians)
	Outputs:
		r (position in m)
		v (velocity in m/s)
		gamma (flight angle in radians)
	'''
	r = (a * (1 - e ** 2)) / (1 + e * np.cos(theta))
	v = np.sqrt(2 * muE / r - muE / a)

	gamma = np.arctan2(e * np.sin(theta), 1 + e * np.cos(theta))

	return r, v, gamma

# CIRCULAR ORBIT ONLY
def findv_circ(r):
	''''Find circular orbit velocity.
	Inputs:
		r (radius in kilometers)
	Outputs:
		v (velocity in km/s)
	'''
	v = np.sqrt(muE/r)
	print(v)
	return v

def findT_circ(r):
    ''' Find circular orbit period.
    Inputs: 
        r (radius in kilometers)
    Outputs:
        T (period in minutes) 
    '''
    T = 2*np.pi*np.sqrt(r**3/muE)
    print(T)
    return T


# ELLIPTICAL ORBITS ONLY
def findtheta(rp, r, e):
	'''True anomaly can be found from knowing periapsis, position, and eccentricity'''
	theta = np.arccos(rp*(1+e)/(r*e) - 1/e)
	return theta

def finderpra(rp, ra):
	'''Elliptical orbits can be found from knowing periapsis and apoapsis'''
	e = (ra - rp) / (ra + rp)
	return e

def finder1r2(r1, r2, theta1, theta2):
	''' Ellpitical orbit can be found when given two points' positions'''
	e = (r2 - r1) / (r1 * np.cos(theta1) - r2 * (np.cos(theta2)))
	rp = r1 * (1 + e*np.cos(theta1)) / (1+e)
	return e, rp

def eccentric2true(e, E):
	'''ELLPTICAL ORBITS
	From known eccentricity and eccentric anomaly, determine true anomaly
	Inputs:
		e (eccentricity)
		E (eccentric anomaly in radians)
	Outputs:
		theta (true anomaly in radians)
	'''
	if e == 0: # circle (e=0)
		theta = "Undefined since it is a circle. Use argument of latitude (u) or true longitude (l) instead."
		print(theta)
	elif e < 1: # ellipse
		print("Ellipse")
		theta = np.arccos((np.cos(E) - e) / (1 - e * np.cosh(E)))
	elif e > 1: # hyperbola
		print("Hyperbola")
		F = E # F is hyperbolic eccentric anomaly
		theta = np.arccosh((np.cosh(F)-e) / (1 - e * np.cosh(F)))
	else: # parabola (e=1)
		theta = "For parabola, true anomaly (radians) cannot be found from eccentric anomaly (E). Use findea(v, r, gamma) instead."
		print(theta)

	return theta

def tof_ellipse(a, e, theta):
	''' ELLIPITICAL ORBITS ONLY
	Time taken by spacecraft to move from periapsis to a given true anomaly (time since periapsis)
	Also known as Kepler equation
	Inputs:
		a (semimajor axis)
		e (eccentricity)
		theta (true anomaly in radians)
	Outputs:
		n (mean motion in in radians / second)
		P (orbital period)
		E (eccentric anomaly in radians)
		t (time since periapsis)
	'''
	n = np.sqrt(muE / a**3)
	P = 2 * np.pi / n
	E = np.arccos((e + np.cos(theta)) / (1 + e * np.cos(theta))) # E (eccentric anomaly)

	t = (E - e * np.sin(E)) / n
	# if true anomaly is greater than half the orbit, must find time by subtracting from total period.
	# This is because earlier formula only calculates journey in the shortest direction
	if theta > np.pi/2:
		t = P - t

	return n, P, E, t

# def eccentricanomaly():
#	return

# PARABOLIC ORBITS ONLY
def escapev(r):
	'''PARABOLIC ORBITS ONLY
	Find escape velocity knowing initial radius (distance from focus)
	Inputs:
		r (position)
	Outputs:
		v (escape velocity)
	'''
	vesc = np.sqrt(2 * muE / r)
	return vesc

# HYPERBOLIC ORBITS ONLY
def excessv(a):
	'''HYERBOLIC ORBITS ONLY
	Find velocity in excess of escape velocity
	Inputs:
		a (semimajor axis)
	Outputs:
		vinf (excess velocity)
		C3
	'''
	vinf = np.sqrt(muE / abs(a))
	C3 = vinf ** 2
	return vinf, C3

def tof_hyperbola(a, e, theta):
	'''HYPERBOLIC ORBITS ONLY
	Inputs:
		a (semimajor axis)
		e (eccentricity)
	Outputs:
		n (mean motion in 1 / s)
		F (hyperbolic eccentric anomaly in radians)
		t (time since periapsis passage in s)
	'''
	n = np.sqrt(muE / a**3)

	F = np.cosh((e + np.cos(theta)) / (1 + e * np.cos(theta)))
	t = (e * np.sinh(F) - F) / n
	return n, F, t

# ORBITAL TRANSFERS
# in-plane maneuvers
def deltav_hohmann(r1, r2):
	'''
	Hohmann transfer for a spacecraft to go from radius 1 to radius 2
	'''
	# semimajor axis of transfer ellipse
	aT = (r1+r2)/2

	vinitial = np.sqrt(muE/r1)
	vtransferi = np.sqrt(muE*(2/r1 - 1/aT))
	deltav1 =  np.abs(vtransferi - vinitial)

	vfinal = np.sqrt(muE/r2)
	vtransferf = np.sqrt(muE*(2/r2 - 1/aT))
	deltav2 = np.abs(vfinal - vtransferf)

	deltav = deltav1 + deltav2

	print(vinitial)
	print(vtransferi)
	print(vfinal)
	print(vtransferf)
	print("Deltav1 is: " + str(deltav1) + " km/s")
	print("Deltav2 is: " + str(deltav2) + " km/s")
	print("Delta v is " + str(deltav) + " m/s")

	t = np.pi * np.sqrt((r1+r2)**3/(8*myconstants.muE))
	return (deltav, t)

# plane change manuevers
def mv_coplanar(v0, vf, deltai):
	''' Changes initial orbit velocity vi to an intersecting coplanar orbit with velocity vf
	beta0 is the initial thrust vector yaw angle, Δi, is the total inclination change
	'''
	beta0 = np.sin(np.pi/2 * deltai) / (v0 / vf - np.cos(np.pi/2 * deltai)) # radians
	return beta0

def deltav_lowthrust(beta0, v0, deltai, f):
	''' Electric Propulsion or Other Continuous Thrust Manuevers Only
	Used to calculate deltav and time of flight with known
	beta0 (thrust vector yaw angle)
	f (spacecraft acceleration)
	'''
	deltav = v0 * np.cos(beta0) - (v0*np.sin(beta0)) / (np.tan(np.pi*deltai/2 + beta0)) # km/s
	t = deltav / f;
	return (deltav, t)

def deltav_coplanar(v0,vf,deltai):
	''' Chemical Propulsion or Impulsive Manuevers Only
	'''
	deltav = np.sqrt(v0 ** 2 + vf ** 2 - 2 * v0 * vf * np.cos(deltai))
	return deltav

def test():
	print("Testing")
	return
