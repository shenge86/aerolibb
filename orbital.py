import numpy as np

global muE
muE = 398600 # km3/s2

# simple calculations
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
	'''
	energy = v ** 2 / 2 - muE / r 
	if energy != 0:
		a = -muE / (2 * energy)
	
	H = r * v * np.cos(gamma)
	e = np.sqrt(1 - H ** 2 / (muE * a))
	
	if e == 0:
		theta = "Does not exist since it is a circle"
	elif e < 0:
		theta = np.acos(a * (1 - e ** 2) / (r * e) - (1/e))
	elif e > 0:
		theta = np.acos(a * (e ** 2 - 1) / (r * e) - (1/e))
	else # parabola
		rp = r # periapsis (NEED TO CORRECT!)
		theta = np.acos((2 * rp - r) / (r * e))
	
	return a, e, theta
	

def eccentric2true(e, E):
	'''From known eccentricity and eccentric anomaly, determine true anomaly
	Inputs:
		e (eccentricity)
		E (eccentric anomaly in radians)
	Outputs:
		theta (true anomaly in radians)
	'''
	if e < 1: # ellipse
		theta = np.acos((np.cos(E) - e) / (1 - e * cosh(E)))
	elif e > 1: # hyperbola
		F = E # F is hyperbolic eccentric anomaly
		theta = np.acosh((np.cosh(F)-e) / (1 - e * np.cosh(F))
	
	return theta	
	
def eccentricanomaly():
	return 