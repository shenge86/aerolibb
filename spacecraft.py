import propulsion as prop
import power as pow
import framechange as fc
import numpy as np

class Spacecraft:
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
	
	# recalculate parameters
	def recalc_mass(self):
		''' Add up masses of all subsystems '''
		return self.mass
	
	# General subsystems create
	def create_engine(self, name="Hydrazine Thruster", type="Mono", thrust=3000, isp=275, me=1000):
		return prop.Engine(name, type, thrust, isp, me)
		
	def create_solar(self, name="Just Another Solar Panel", size=5000, mass=5, powerlab=300, efficiency=0.15):
		return pow.Solar(name, size, mass, powerlab, efficiency)
	
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
	
	# Payload Functions
	def define_payload(self, mpayload, ppayload):
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