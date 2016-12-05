import numpy as np
import os
import csv

# Static methods
# Generate a solar product based on user choice
def showSolarProducts():
	# Shows list of solar panels in database and asks user to choose one
	FILENAME = os.path.join(os.path.dirname(__file__), 'data/powerdb.csv')
	print("Current space solar panels include these. Please choose a number:")
	with open(FILENAME) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		
		# initialize variables
		ids = []
		names = []
		cellsizes = []
		densitys = []
		specificpowers = []
		powerdensitys = []
		efficiencys = []
		EOLs = []
		
		# loop through each table row of products
		for row in readCSV:
			id = row[0]
			name = row[1]
			cellsize = row[2]
			density = row[3]
			specificpower = row[4]
			powerdensity = row[5]
			efficiency = row[6]
			EOL = row[7]
		
			# print out options for user to choose
			print(id + ": " + name)
		
			# store as array for access later
			ids.append(id)
			names.append(name)
			cellsizes.append(cellsize)
			densitys.append(density)
			specificpowers.append(specificpower)
			powerdensitys.append(powerdensity)
			efficiencys.append(efficiency)
			EOLs.append(EOL)
			
		# Choose a solar panel from the options
		whatPanel = input('What panel do you want? Enter ID #: ')
		idex = ids.index(whatPanel)
		
		# set variable to the particular value in the index
		name = names[idex]
		cellsize = cellsizes[idex]
		density = densitys[idex]
		specificpower = specificpowers[idex]
		powerdensity = powerdensitys[idex]
		efficiency = efficiencys[idex]
		EOL = EOLs[idex]
		
		
		print('You have chosen: ')
		print(str(idex) + ": " + name)
		print("Cell Size (m2): " + cellsize)
		print("EOL / BOL Ratio: " + EOL)
		
		# convert the string types  to integer types
		cellsize = float(cellsize)
		density = float(density)
		specificpower = float(specificpower)
		powerdensity = float(powerdensity)
		efficiency = float(efficiency)
		EOL = float(EOL)
		
		# create new object for storage in external function
		return Solar(name,cellsize,density,specificpower,powerdensity,efficiency,EOL)

class Power:
	def __init__(self, name, density, type):
		''' Common to all energy producers:
		name
		density (kg/m2 for solar or kg/m3 for other)
		type (solar, battery, fuel cell, etc.)
		'''
		self.name = name
		self.density = density
		self.type = type

# energy production devices		
class Solar(Power):
	def __init__(self, name, cellsize, density, specificpower, powerdensity, efficiency,EOL):
		''' subclass of Power
		size (m2)
		density (kg/m2)
		specificpower (W/kg)
		powerdensity (W/m2)
		efficiency (decimal between 0 and 1) '''
		
		# Initiate with 
		Power.__init__(self, name, density, "Solar")
		
		self.cellsize = cellsize
		self.specificpower = specificpower
		self.powerdensity = powerdensity
		self.efficiency = efficiency
		self.EOL = EOL
	
	def calc_size(self, power):
		''' Inputs: 
		power (W) - amount of power required for the system to produce
		
		Predefined:
		specificpower (W/kg)
		powerdensity (W/m3) 
		wattdensity (W/m2) 
		efficiency (decimal between 0 and 1) 
		'''
		
		# mass
		mass = power / self.specificpower
		mass = mass / self.efficiency
		
		# size
		size = power / self.powerdensity
		size = size / self.efficiency
		
		self.mass = mass
		self.size = size
		return mass, size
		
	def printDesc(self):
		# please calculate actual size and mass  before running this method
		print("Power Information for System")
		print("Type: " + self.type)
		print("Name: " + self.name)
		print("Mass (kg): " + str(self.mass))
		print("Size (m2): " + str(self.size))
		print("Power Information for Cell")
		print("Specific Power (W/kg): " + str(self.specificpower))
		print("Power Density (W/m2): " + str(self.powerdensity))
		print("Density (kg/m2): " + str(self.density))
		print("Efficiency: " + str(self.efficiency))

# energy storage devices		
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
		
class FlyWheels(Power):
	def __init__(self, name, size, capacity)
		Power.__init__(self, name, size, capacity, "Flywheel")
		
		
	