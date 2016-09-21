import propulsion as prop
import framechange as fc
import numpy as np

class spacecraft:
	# class variables shared by all instances
	

	def __init__(self, name, mass=1000, vol=1000, cost=1000, x=0, y=0, z=0, yaw=0, pitch=0, roll=0):
		''' Constructor for the class '''
		# create instance variable unique to each instance
		# initialize
		self.name = name
		self.mass = mass
		self.vol = vol
		self.cost = cost
		self.x = x # position in current frame
		self.y = y
		self.z = z
		self.rp = np.array([[x],[y],[z]]) # array display of position in current frame`
		self.yaw = yaw # current frame's axis displayed as rotations relative to inertial frame
		self.pitch = pitch
		self.roll = roll
	
	def printDesc(self):
		print("Spacecraft state: ")
		print(self.name)
		print(self.mass)
		print(self.vol)
		print(self.cost)
		print("Current position (xyz): [%f %f %f]" % (self.x, self.y, self.z))
		print(self.rp)
		print("Current attitude (ypr): [%f %f %f]" % (self.yaw, self.pitch, self.roll))
	
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
	
	# Mass Functions
	def payload_mass(self, mp):
		self.mp = mp
		return self.mp
	
	# Test Functions
	def test(self):
		prop.say()