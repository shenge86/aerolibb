import numpy as np

class Power:
	def __init__(self, name, size, density, type):
		self.name = name
		self.type = type
		self.size = size
		self.density = density
		self.mass = size*density
					
class Solar(Power):
	def __init__(self, name, size, density, powerlab, efficiency=0.97):
		''' subclass of Power
		powerlab is the power produced by the entire solar array before efficiency loss
		size (m2)
		efficiency (decimal between 0 and 1) '''
		Power.__init__(self, name, size, density, "Solar")
		self.power = powerlab*efficiency
		self.efficiency = efficiency
	
	def calc_size(self, powerlab, wattdensity, efficiency):
		''' Units: powerlab (W) 
		wattdensity (W/m2) 
		efficiency (decimal between 0 and 1) 
		Note: 
		Both efficiency and watt density can be modified here! '''
		power = powerlab*efficiency
		size = power / wattdensity
		mass = self.density * size
		
		self.size = size
		self.mass = mass
		self.power = power
		self.efficiency = efficiency
		return size, mass, power, efficiency
	
	
	
	def printDesc(self):
		# please calculate actual size and mass  before running this method
		print("Power Information")
		print("Name: " + self.name)
		print("Type: " + self.type)
		print("Power Produced (W): " + str(self.power))
		print("Size (m2): " + str(self.size))
		print("Density (kg/m2): " + str(self.density))
		print("Mass (kg): " + str(self.mass))
		print("Efficiency: " + str(self.efficiency))
		
	class Battery(Power):
		def __init__(self, name, size, capacity, efficiency):
			''' subclass of Power
			battery
			'''
			Power.__init__(self, name, size, capacity, "Battery")
			self.capacity = capacity
			self.efficiency = efficiency
			
		def calc_capacity(self, size, efficiency):
			capacity = size * efficiency
			
			self.capacity = capacity
			return capacity
			
	class FuelCell(Power):
		def __init__(self, name, size, capacity, efficiency):
			''' subclass of Power
			fuel cells
			'''
			Power.__init__(self, name, size, capacity, "Fuel Cell")
			self.capacity = capacity
			self.efficiency = efficiency
			
