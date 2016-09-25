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
		
	def rocketeqn(self, deltav, isp, mi):
		"""
		Find final mass and propellant mass from iniitial mass
		"""
		g = 9.80665
		# mp = mi*(1 - np.exp(-deltav / (g*isp)))
		# mf = mi - mp
		mf = mi * np.exp(-deltav / (isp*g))
		mp = mi - mf
		
		# recalculate necessary engine mass
		self.mass = mf
		return mf, mp
		
	def propellant_tank(self, massp):
		'''
		Takes in the mass of the propellant to calculate tank mass
		'''
		masss = massp * 2
		self.masss = masss
		return masss