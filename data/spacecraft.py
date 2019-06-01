import propulsion as prop
import power as pow
import framechange as fc
import orbital as orb
import numpy as np

class Spacecraft:
	# class variables shared by all instances	

	def __init__(self, name, type, trl, mass=1000, vol=1000, power=100, cost=1000, x=0, y=0, z=0, yaw=0, pitch=0, roll=0):
		''' Constructor for the class 
		 Create instance variable unique to each instance
		INPUTS:
		type (of satellite) :
		1 Communications
		2 Meteorology
		3 Planetary
		4 Other
		trl (technology readiness level)
		1 - 3 New
		4 - 6 Nexxt-gen
		7 - 9 Production-levl
		
		'''
		self.name = name
		self.type = type
		self.trl = trl
		self.mass = mass
		self.vol = vol
		self.power = power
		self.cost = cost
		self.x = x # position in current frame
		self.y = y
		self.z = z
		self.rp = np.array([[x],[y],[z]]) # array display of position in current frame`
		self.yaw = yaw # current frame's axis displayed as rotations relative to inertial frame
		self.pitch = pitch
		self.roll = roll
	
	def printDesc(self):
		print("Spacecraft Overview: ")
		print("Name: " + self.name)
		print("Type: " + str(self.type))
		print("OPTIONS: ")
		print("Type 1: Communications")
		print("Type 2: Meteorology")
		print("Type 3: Planetary")
		print("Type 4: Other")
		print("Mass (kg): " + str(self.mass))
		print("Volume (m^3): " + str(self.vol))
		print("Power (W): " + str(self.power))
		print("Cost ($): " + str(self.cost))
		print("Current position (xyz) (km): [%f %f %f]" % (self.x, self.y, self.z))
		print(self.rp)
		print("Current attitude (ypr) (rad): [%f %f %f]" % (self.yaw, self.pitch, self.roll))
	
	# Estimate parameters
	def est_mp(self, mpayload, ppayload):
		'''
		
		'''
		self.mpayload = mpayload
		self.ppayload = ppayload
		if self.type == 1: # communications
			power = 1.1568*ppayload + 55.497
			mass = 3.6 * mpayload
		elif self.type == 2: # meteorology
			power = 602.18 * np.log(ppayload) - 2761.4
			mass = 4.8 * mpayload
		elif self.type == 3: # planetary
			power = 332.93 * np.log(ppayload) - 1046.6
			mass = 7 * mpayload
		else: # other
			power = 210 + 1.3*ppayload
			# mass unknown here but default is same as planetary
			mass = 7 * mpayload
		
		# add mass margin depending on mass and TRL level
		if self.trl <= 3:
			if mass <= 50:
				mass = mass * 1.5
			elif mass <= 500:
				mass = mass * 1.35
			elif mass <= 2500:
				mass = mass * 1.3
			else:
				mass = mass * 1.28
		elif self.trl <= 6:
			if mass <= 50:
				mass = mass * 1.3
			elif mass <= 500:
				mass = mass * 1.25
			elif mass <= 2500:
				mass = mass * 1.2
			else:
				mass = mass * 1.18
		else:
			if mass <= 50:
				mass = mass * 1.04
			elif mass <= 500:
				mass = mass * 1.04
			elif mass <= 2500:
				mass = mass * 1.02
			else:
				mass = mass * 1.01
		
		if self.trl <= 3:
			if power <= 500:
				power = power * 1.9
			elif power <= 1500:
				power = power * 1.8
			elif power <= 5000:
				power = power * 1.7
			else:
				power = power * 1.4
		elif self.trl <= 6:
			if power <= 500:
				power = power * 1.4
			elif power <= 1500:
				power = power * 1.35
			elif power <= 5000:
				power = power * 1.3
			else:
				power = power * 1.25
		else:
			if power <= 500:
				power = power * 1.13
			elif power <= 1500:
				power = power * 1.13
			elif power <= 5000:
				power = power * 1.13
			else:
				power = power * 1.13
		
		# allocate masses
		# this assumes 3rd party builds the payloads (not same company as spacecraft company)
		if self.type == 1: # communications
			mstructure = mass * 0.29
			mthermal = mass * 0.04
			madcs = mass * 0.07
			mpower = mass * 0.26
			mcabling = mass * 0.03
			mprop = mass * 0.07
			mcdh = mass * 0.04
			mtelecom = 0 # no telecom since the payload is a giant communication device
			
			pthermal = power * 0.3
			padcs = power * 0.28
			ppower = power * 0.16
			pcdh = power * 0.19
			ptelecom = 0
			pprop = power * 0.07
			pstructure = 0 # mostly mechanisms
			
		elif self.type == 2: # metsats
			mstructure = mass * 0.2
			mthermal = mass * 0.03
			madcs = mass * 0.09
			mpower = mass * 0.16
			mcabling = mass * 0.08
			mprop = mass * 0.05
			mcdh = mass * 0.04
			mtelecom = mass * 0.04
			
			pthermal = power * 0.48
			padcs = power * 0.19
			ppower = power * 0.05
			pcdh = power * 0.13
			ptelecom = power * 0.15
			pprop = 0
			pstructure = 0 # mostly mechanisms
		elif self.type == 3: # planetary
			mstructure = mass * 0.26
			mthermal = mass * 0.03
			madcs = mass * 0.09
			mpower = mass * 0.19
			mcabling = mass * 0.07
			mprop = mass * 0.13
			mcdh = mass * 0.06
			mtelecom = mass * 0.06
			
			pthermal = power * 0.28
			padcs = power * 0.2
			ppower = power * 0.1
			pcdh = power * 0.17
			ptelecom = power * 0.23
			pprop = power * 0.01
			pstructure = power * 0.01 # mostly mechanisms
		else: # other
			mstructure = mass * 0.21
			mthermal = mass * 0.03
			madcs = mass * 0.08
			mpower = mass * 0.21
			mcabling = mass * 0.05
			mprop = mass * 0.05
			mcdh = mass * 0.04
			mtelecom = mass * 0.04
		
			pthermal = power * 0.33
			padcs = power * 0.11
			ppower = power * 0.02
			pcdh = power * 0.15
			ptelecom = power * 0.3
			pprop = power * 0.04
			pstructure = power * 0.05 # mostly mechanisms
		
		self.power = power
		self.mass = mass
		return mass, power
	
	# Calculate parameters
	# Note: More detailed than  estimated parameters.
	def calc_mass(self):
		''' Add up masses of all subsystems. Subsystems include:
		Payload
		Propulsion
		Attitude determination and control
		Power
		Telecommunication
		Command & Data Handling
		Thermal
		Structure
		'''
		
		mass = mpayload + mprop + madcs + mpower + mtelecom + mcdh + mthermal + mstructure + mcabling
		margin = 0.25
		mass = mass * (1 + margin)
		self.mass = mass
		return self.mass
	
	# General subsystems create
	def create_engine(self, name="Hydrazine Thruster", type="Mono", thrust=3000, isp=275, me=1000):
		return prop.Engine(name, type, thrust, isp, me)
		
	def create_solar(self, name="Just Another Solar Panel", size=5000, density=5, powerlab=3000, efficiency=0.15):
		return pow.Solar(name, size, density, powerlab, efficiency)
	
	def create_battery(self, name="Just Another Battery", size=100, capacity=300, efficiency=0.15):
		return pow.Battery(name, size, capacity, efficiency)
	
	# Orbital Functions
	def define_position(self, x, y, z, *rp):
		self.x = x
		self.y = y
		self.z = z
		self.rp = np.array([[x],[y],[z]])
		return rp
	
	# Attitude Functions
	def define_attitude(self,yaw,pitch,roll):
		self.yaw = yaw
		self.pitch = pitch
		self.roll = roll
		return yaw, pitch, roll
	
	def rotate_attitude(self,yaw,pitch,roll, *rp):
		''' Locate the point in a rotated coordinate frame 
		rp is optional since you will already know rp from x, y, and z coordinates
		but you can redefine another rp if you would like '''
		self.yaw = yaw
		self.pitch = pitch
		self.roll = roll
		rotMatrix = fc.euler2dcm(yaw,pitch,roll)
		print(rotMatrix)
		print(self.rp)
		print("Coordinates in rotated frame: ")
		self.rp = np.dot(rotMatrix,self.rp)
		self.x = self.rp[0]
		self.y = self.rp[1]
		self.z = self.rp[2]
		print(self.rp)
		return rp
	
	
	
	# Test Functions
	def test(self):
		prop.say()