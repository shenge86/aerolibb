import propulsion as prop
import framechange as fc
import numpy as np

class spacecraft:
	# class variables shared by all instances
	

	def __init__(self, name, type, mass=1000, vol=1000, power=100, cost=1000, x=0, y=0, z=0, yaw=0, pitch=0, roll=0):
		''' Constructor for the class '''
		# create instance variable unique to each instance
		# initialize
		self.name = name
		self.type = type
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
		# initialize subsystems with default parameters
		self.engine = prop.engine("Engine 1", "LH2/LOX", 110, 5000, 505, 100, 300, 350) # main engine
	
	def printDesc(self):
		print("Spacecraft state: ")
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
	
	# recalculate parameters
	def recalcMass(self):
		''' Add up masses of all subsystems '''
		# self.mass = 
		return self.mass
	
	# General subsystems create
	def createEngine(self, name="Just Another Engine", type="Xe Hall Thruster", isp=5000):
		return prop.engine(name, type, 11, 500, 50, 10, 30, isp)
		
	
	# Orbital Functions
	def definePosition(self, x, y, z, *rp):
		self.x = x
		self.y = y
		self.z = z
		self.rp = np.array([[x],[y],[z]])
		return rp
	
	# Attitude Functions
	def defineAttitude(self,yaw,pitch,roll):
		self.yaw = yaw
		self.pitch = pitch
		self.roll = roll
		return yaw, pitch, roll
	
	def rotateAttitude(self,yaw,pitch,roll, *rp):
	# point location in new coordinate frame
		self.yaw = yaw
		self.pitch = pitch
		self.roll = roll
		rotMatrix = fc.euler(yaw,pitch,roll)
		print(rotMatrix)
		print(self.rp)
		print("Coordinates in rotated frame: ")
		self.rp = np.dot(rotMatrix,self.rp)
		self.x = self.rp[0]
		self.y = self.rp[1]
		self.z = self.rp[2]
		print(self.rp)
		return rp
	
	# Payload Functions
	def definePayload(self, mpayload, ppayload):
		self.mpayload = mpayload
		self.ppayload = ppayload
		if self.type == 1:
			power = 1.1568*ppayload + 55.497
		elif self.type == 2:
			power = 602.18 * np.log(ppayload) - 2761.4
		elif self.type == 3:
			power = 332.93 * np.log(ppayload) - 1046.6
		else:
			power = 210 + 1.3*ppayload
		
		self.power = power
		
		mass = mpayload * 2
		self.mass = mass
		return mass, power
	
	# Test Functions
	def test(self):
		prop.say()