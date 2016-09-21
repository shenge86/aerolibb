import numpy as np

def say():
	print ('TEST!')

def rocketeqn(deltav, isp, mi):
	"""
	Find final mass and propellant mass from iniitial mass
	"""
	g = 9.80665
	# mp = mi*(1 - np.exp(-deltav / (g*isp)))
	# mf = mi - mp
	mf = mi * np.exp(-deltav / (isp*g))
	mp = mi - mf
	return mf, mp