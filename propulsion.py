import numpy as np

class Engine: 
	def __init__(self, name, type, masse, massp, masss, size, thrust, isp):
		self.name = name
		self.type = type
		self.masse = masse # mass of engine
		self.massp = massp # mass of propellant
		self.masss = masss # mass of tanks and structure
		self.size = size
		self.thrust = thrust
		self.isp = isp

	def printDesc(self):
		print ("Propulsion/Engine Information")
		print("Name: " + self.name)
		print("Type: " + self.type)
		print("Mass of engine: " + str(self.masse))
		print("Mass of propellant: " + str(self.massp))
		print("Mass of tanks: " + str(self.masss))
		mass = self.masse + self.massp + self.masss
		print("Total Mass: " + str(mass))
		print("Size: " + str(self.size))
		print("Thrust: " + str(self.thrust))
		print("isp: " + str(self.isp))	
		
	def rocketeqn(self, **kwargs):
		"""
		Inputs can be in any order but must be named as such: 
		deltav (change in velocity)
		mi (initial mass)
		mf (final mass)
		mp (propellant mass)
		From known parameters, calculates other parameters.
		"""
		# constants
		g = 9.80665 # m/s^2
		# isp is specific to the engine so it cannot be changed
		isp = self.isp # s 
		
		def selfset(self):
			self.deltav = deltav
			self.mi = mi
			self.mf= mf
			self.mp = mp
			print("Calculated / Given Values: ")
			print("With an engine that has an isp of " + str(isp) + ": ")
			print("deltav: " + str(deltav))
			print("mi (initial mass): " + str(mi))
			print("mf (final mass): " + str(mf))
			print("mp (propellant mass): " + str(mp))
		
		if "deltav" in kwargs and "mi" in kwargs:
			print("Given deltav: " + str(kwargs["deltav"]))
			deltav = kwargs["deltav"]
			mi = kwargs["mi"]
			mp = mi * (1 - np.exp(-deltav / (g * isp)))
			mf = mi - mp
			selfset(self)
			return deltav, mi, mf, mp
		
		if "deltav" in kwargs and "mf" in kwargs:
			deltav = kwargs["deltav"]
			mf = kwargs["mf"]
			mp = mf * (np.exp(deltav / (g*isp)) - 1)
			mi = mp + mf
			selfset(self)
			return deltav, mi, mf, mp
			
		if "mi" in kwargs and "mf" in kwargs:	
			print("Given mi: " + str(kwargs["mi"]))
			print("Given mf: " + str(kwargs["mf"]))
			mi = kwargs["mi"]
			mf = kwargs["mf"]
			deltav = g * isp * np.log(mi / mf)
			mp = mi - mf
			selfset(self)
			return deltav, mi, mf, mp
		
	def propellant_tank(self, massp):
		'''
		Takes in the mass of the propellant to calculate tank mass
		'''
		masss = massp * 2
		self.masss = masss
		return masss