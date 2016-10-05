import numpy as np

class Engine(object): 
	# Constants
	instances = [] # spacecraft can have multiple engines so need to keep track of number of instances of this class 
	global g 
	g = 9.80665 # m/s^2
	
	def __init__(self, name, type, thrust, isp, me):
		''' Defines major characteristics of an engine 
		Type of engine affects major design calculations.
		Specifics such as the type of chemicals do not need to be defined.
		INPUTS:
			Name can be anything.
			Type can be the following:
				Mono or 1 (monopropellant)
				Biprop or 2 (bipropellant)
				Coldgas or 3 (cold gas)
				Solid or 4 (solid)
				Ion or 5 (ion thruster)
				Hall or 6 (hall thruster)
				MPD or 7 (magnetoplasmadynamic thruster)
				SEP or 8 (solar electric)
			Thrust is in Newtons.
			isp is in seconds.
			Me is engine mass without propellant or tanks in kg.
		'''
		self.name = name
		self.type = type
		self.thrust = thrust
		self.isp = isp
		self.me = me
		Engine.instances.append(self)

	def printDesc(self):
		print ("Propulsion/Engine Information")
		print("Name: " + self.name)
		print("Type: " + self.type)
		print("Mass of engine: " + str(self.me))
		print("Mass of propellant: " + str(self.mp))
		print("Mass of other propulsion parts: " + str(self.mo))
		self.mass = self.me + self.mp + self.mo
		print("Total propulsion subsystem mass: " + str(self.mass))
		print("Thrust: " + str(self.thrust))
		print("isp: " + str(self.isp))	
		
	# orbital mechanics
	# use for main engine
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
			# Define a set of masses for the propulsion system 
			self.deltav = deltav
			self.mi = mi # initial mass`
			self.mf= mf # final mass
			self.mp = mp # propellant mass
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
	# use for small ADCS engine
	def oneaxismaneuver(self, theta, I, L, n):
		''' Scenario:
		Spacecraft needs to be manuevered to a different orientation. Thrusters fire briefly. Then it stops firing as the spacecraft coasts. Then it fires briefly again to slow down and stop the rotation.
		Calculates mass of propellant required for rotating a particular angle along one-axis. 
		Note that this is only for one axis! Will need to be calculated separately for each axis.
		Inputs:
			theta (rotation angle in radians about the x, y, or z axis)
			I (moment of inertia in kg*m^2 about the x, y, or z axis)
			L (moment arm in m - distance from center of mass to the thruster)
			n (number of thrusters)
		Outputs:
			t (time to perform maneuver in seconds)
			mp (mass of propellant)
		'''
		print("WARNING: Do not use this method if this engine is not used for attitude control.")
		print("Use rocketeqn instead if so.")
		
		F = self.thrust 
		t = 2 * np.sqrt(theta * I / (n * F * L))
		tb = t / 2 # single burn consumption
		mp = 2 * n * F * tb / (g*self.isp)
		
		print("Time for burn is: " + str(t))
		print("Mass of propellant for burn is: " + str(mp))
		
		self.mp = mp
		return t, mp
	
	def unloadrxn(self, Iw, omega, L, n):
		''' Scenario:
		Reaction wheel has spun to the maximum speed. Now, we need to de-spin it to 0 with thrusters firing the opposite direction.
		Answers the question: What is the amount of propellant needed to reset the wheel rotation speed to 0?
		Note also that this does not modify the mass of propellant needed for the engine!!! You need to do that separately.
		Inputs:
			Iw (moment of inertia of the reaction wheel in kg*m^2 about the x, y, or z axis)
			omega (angular velocity of the reaction wheel in rad / s )
			L (moment arm in m - distance from center of mass to the thruster)
			n (number of thrusters)
		Outputs:
			mp (total mass of propellant including trapped and loading error in kg)
			vprop (total volume of such propellant in m3) 
		'''
		
		H = Iw * omega # angular momentum in N*m*s
		t = H / (n * self.thrust * L)
		mp = H / (L * self.isp * g)
		
		print("TIme of burn to de-spin wheel: " + str(t))
		print("Mass of propellant needed to unload wheel: " + str(mp))
		return t, mp
	
	def calcpropsystemvol(self, B, rhop, I=0):
		''' 
		Assume mass of propellant (usable propellant) is known.  Find the total propellant mass (including losses and loading) and total propellant volume.
		Assume the engine isp, thrust, and type is known from defined parameters in creation.
		Assume spherical tank.
		Inputs:
			B (blowdown ratio)
			rhop (density of propellant kg/m**3)
		Outputs:
			mp (mass of propellant with extras)
			Vprop (volume of propellant with extras)
		'''
		if not hasattr(self, 'mp'):
			print("Mass of propellant has not been calculated yet! Please calculate first.")
			return
		
		# usable propellant weight by definition of isp
		# Wu = I / (isp * g)
		Wu = self.mp
		
		if self.type == "Mono" or self.type == 1 or self.type == "Biprop" or self.type == 2:
			T = self.thrust
			isp = self.isp
			# thruster weight (kg)
			Wt = self.me
			# Use following only if you don't know thruster weight:
			# Wt = 0.4 + 0.0033 * T
			# self.masse = Wt
			
			# calculate total volume of propellant to determine tank size (and mass) needed #
			# volume of usable propellant
			Vu = Wu / rhop
			# total volume of unusable propellant is ~3% of useable for monopropellant system
			Vp = Vu / .03 
			
			# ullage volume
			Vgi = Vu / (B - 1)
			
			# bladder volume
			# assume thin shell approximation
			tb = .02 # thickness of bladder
			rb = (0.75 * (Vp + Vgi) / np.pi) ** (1/3)
			Ab = 2 * np.pi * rb**2
			Vb = Ab * tb
		else:
			print("Not an accepted type of propulsion.")
		
		# Assume trapped propellant is 3% and loading error is 0.5%
		mp = Wu + Wu * .03 + Wu * .005
		self.mp = mp
		
		# Find volume of propellant system to calculate tank mass later
		Vprop = Vu + Vp + Vgi + Vb
			
		return mp, Vprop
	
	def tankvol2mass(self, Vprop, rho, n, t, shape="sphere", L=1):
		''' From known volume of tank, finds the mass.
		Inputs: 
		rho (density of tank material in kg/m3)
		V (volume of total propellant in m3)
		n (number of tanks)
		t (thickness of tank wall in m)
		shape (1 or sphere is default)
		L (Optional!) (Use only for cylinder - length of cylinder in m)
		'''
		
		if shape == "sphere" or shape == 1:
			print("Assuming sphere...")
			V = Vprop / n
			r = (3 * V / (4 * np.pi)) ** (1/3)
			R = r + t
			mtank = (4/3) * np.pi * rho * (R**3 - r**3)
			mtank = mtank * n 
		else: # assume cylindrical
			print("Assuming cylinder...")
			print("Assumed length: " + str(L))
			V = Vprop / n
			r = np.sqrt(V / (np.pi * L))
			R = r + t
			mtank = np.pi * L * rho * (R**2 - r**2)
			mtank * n
		
		self.mo = mtank
		return mtank