import numpy as np

class Engine: 
	# Constants
	global g 
	g = 9.80665 # m/s^2
	
	def __init__(self, name, type, masse, massp, masss, size, thrust, isp):
		''' Defines major characteristics of an engine 
		Type of engine affects major design calculations.
		Specifics such as the type of chemicals do not need to be defined.
		Type can be the following:
		Mono (monopropellant)
		Biprop (bipropellant)
		Coldgas (cold gas)
		Solid (solid)
		'''
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
		Rocket equation
		Used for orbital manuevers
		Inputs can be in any order but must be named as such: 
		deltav (change in velocity)
		mi (initial mass)
		mf (final mass)
		mp (propellant mass)
		From known parameters, calculates other parameters.
		"""
		# constants
		
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
	
	# Attitude Manuevers
	
	def oneaxismaneuver(self, theta, I, L, n):
		''' Scenario:
		Spacecraft needs to be manuevered to a different orientation. Thrusters fire briefly. Then it stops firing as the spacecraft coasts. Then it fires briefly again to slow down and stop the rotation.
		Calculates mass of propellant required for rotating a particular angle along one-axis. 
		Note that this is only for one axis! Will need to be calculated separately for each axis.
		Note also that this does not modify the mass of propellant needed for the engine!!! You need to do that separately.
		Inputs:
			theta (rotation angle in radians about the x, y, or z axis)
			I (moment of inertia in kg*m^2 about the x, y, or z axis)
			L (moment arm in m - distance from center of mass to the thruster)
			n (number of thrusters)
		Outputs:
			t (time to perform maneuver in seconds)
			mp (mass of propellant)
		'''
		
		F = self.thrust 
		t = 2 * np.sqrt(theta * I / (n * F * L))
		tb = t / 2 # single burn consumption
		mp = 2 * n * F * tb / (g*self.isp)
		
		print("Time for burn is: " + str(t))
		print("Mass of propellant for burn is: " + str(mp))
		return t, mp
	
	def unloadrxn(self, Iw, omega, L, n):
		''' Scenario:
		Reaction wheel has spun to the maximum speed. Now, we need to de-spin it to 0 with thrusters firing the opposite direction.
		Answers the question: What is the amount of propellant needed to reset the wheel rotation speed to 0?
		Note also that this does not modify the mass of propellant needed for the engine!!! You need to do that separately.
		'Inputs:
			Iw (moment of inertia of the reaction wheel in kg*m^2 about the x, y, or z axis)
			omega (angular velocity of the reaction wheel in rad / s )
			L (moment arm in m - distance from center of mass to the thruster)
			n (number of thrusters)
		'''
		
		H = Iw * omega # angular momentum in N*m*s
		t = H / (n * self.thrust * L)
		mp = H / (L * self.isp * g)
		
		print("TIme of burn to de-spin wheel: " + str(t))
		print("Mass of propellant needed to unload wheel: " + str(mp))
		return t, mp
	
	# Structure
	
	def tankmass2vol(rho, r, t)
		''' From known volume of tank, finds the mass.
		Inputs:
		rho (density of tank material in kg/m3)
		r (internal radius of tank in m)
		t (thickness of tank wall in m)
		'''
		R = r + t
		masss = (4/3) * np.pi * rho * (R**3 - r**3)
		self.masss = masss
		return masss