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

def showBatteryProducts():
	FILENAME = os.path.join(os.path.dirname(__file__), 'data/powerbatterydb.csv')
	print("Current space batteries include these. Please choose a number:")
	with open(FILENAME) as csvfile:
		readCSV = csv.reader(csvfile, delimiter=',')
		
		ids = []
		names = []
		Cbats = []
		DODs = []
		Whkgs = []
		WhLs = []
		
		for row in readCSV:
			id = row[0]
			name = row[1]
			Cbat = row[2]
			DOD = row[3]
			Whkg = row[4]
			WhL = row[5]

			print(id + ": " + name)
			
			ids.append(id)
			names.append(name)
			Cbats.append(Cbat)
			DODs.append(DOD)
			Whkgs.append(Whkg)
			WhLs.append(WhL)
		
		whatBattery = input("What battery do you want? Enter ID #: ")
		idex = ids.index(whatBattery)
		
		name = names[idex]
		Cbat = Cbats[idex]
		DOD = DODs[idex]
		Whkg = Whkgs[idex]
		WhL = WhLs[idex]
		
		Cbat = float(Cbat)
		DOD = float(DOD)
		Whkg = float(Whkg)
		WhL = float(WhL)
		
		return Battery(name, DOD, Cbat, Whkg,WhL)
		
class Power:
	def __init__(self, spin, poweravg, missionlife):
		'''
		Like other subsystems, power system requires fulfilling requirements and fall under constraints
		Inputs initialized from other subystems
		Outputs can affect other subsystems so iterate
		Note: power input is taken from the initially generated spacecraft
		INPUTS:
		poweravg - watts (total power) 
		missionlife  - years
		OUTPUTS:
		powermax (battery requirements) - watts
		poweravg (solar panel requirements) - watts
		'''
		
		# Some important notes:
		# 1. Power budget is based on peak power demands.
		# 2. Energy budget is based on average energy consumption.
		
		# powermax is equivalent to night time power
		# at night, thermal control power is approximately doubled
		# thermal control is ~33% of the total power
		powerthermal = poweravg * 0.33
		powermax = poweravg + powerthermal 
		
		# include efficiency losses
		etap = .98 # poiint harness losses
		etac = .95 # converter losses
		
		# mission lifetime determines degradation
		# degradation is 4 - 10% during first year and very little afterwards
		if (missionlife <= 1):
			etaEOL = .95
		else:
			etaEOL = .9

		# if spacecraft is spinning, efficiency is decreased by pi
		if spin == 1: # spinning
			etas = 1/np.pi
		else: # deployable
			etas = 1
			
		eta = etap*etac*etaEOL*etas # total efficiency
		poweravg = poweravg / eta
		powermax = powermax / eta
		
		#inputs object set
		self.poweravg = poweravg
		self.missionlife = missionlife	
		
		# outputs object set
		self.powermax = powermax
		
		
	
	def calc_powerproduction(self, poweravg):
		'''
		Calculates optimal numbers and configuration of batteries
		'''
		self.panelnums = panelnums 
		self.panelmass = panelmass
		return panelnums, panelmass
	
class PowerProducer:
	def __init__(self, name, density, type):
		''' Power producer types share these commonalities: 
		name
		density (kg/m2 for solar or kg/m3 for other)
		type (solar, battery, fuel cell, etc.)
		'''
		self.name = name
		self.density = density
		self.type = type
		
# energy production devices		
class Solar(PowerProducer):
	def __init__(self, name, cellsize, density, specificpower, powerdensity, efficiency,EOL):
		''' subclass of PowerProducer
		size (m2)
		density (kg/m2)
		specificpower (W/kg)
		powerdensity (W/m2)
		efficiency (decimal between 0 and 1) '''
		
		# Initiate with 
		PowerProducer.__init__(self, name, density, "Solar")
		
		self.cellsize = cellsize
		self.specificpower = specificpower
		self.powerdensity = powerdensity
		self.efficiency = efficiency
		self.EOL = EOL
	
	def calc_size(self, powermax):
		''' Inputs: 
		powermax (W) - amount of power required for the system to produce (should be same as powermax)
		
		Predefined:
		specificpower (W/kg)
		powerdensity (W/m3) 
		wattdensity (W/m2) 
		efficiency (decimal between 0 and 1) 
		
		Outputs:
		mass (kg)
		size (m2)
		'''
		
		# mass
		mass = powermax / self.specificpower
		mass = mass / self.efficiency
		
		# size
		size = powermax / self.powerdensity
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
class PowerStorage():
	def __init__(self,name,type):
		self.name = name
		self.type = type
		
class Battery(PowerStorage):
	def __init__(self, name, DOD, Cbat, specificenergy,specificvol):
		''' subclass of PowerStorage
		battery
		'''
		PowerStorage.__init__(self, name, "Battery")
		self.DOD = DOD
		self.Cbat = Cbat
		self.specificenergy = specificenergy
		self.specificvol = specificvol
	
	def calc_eclipsetime(self, h, beta):
		'''
		INPUTS:
		h (altitude above Earth - m)
		beta (beta angle - rad)
		OUTPUTS:
		eclipsetime (s)
		
		NOTE:
		Assumed mean motion for calculating period. Used average radius.
		beta angle requires a lot of calculations
		'''
		rE = 6371000 # m
		r = rE + h
		
		# eclipse fraction
		fE = np.arccos(np.sqrt(h**2 + 2*rE*h) / (r*np.cos(beta))) / np.pi
		
		# average orbital period
		TP = 2*np.pi / r**3
		
		eclipsetime = fE * TP
		
		return eclipsetime
	
	
	def calc_mass(self, powermax, eclipsetime):
		'''
		Calculates optimal numbers and configuration of batteries
		INPUTS:
		powermax (W)
		eclipsetime (s)
		OUTPUTS:
		batterynums (number of batteris)
		batterymass (total mass of all batteries - kg)
		batterysize (total size of all batteries - m3)
		# Another idea:
		Have another method that calls this method. Loops through all available products
		'''
		
		# given
		DOD = self.DOD # DOD (depth of discharge - 0% to 100%)
		Cbat = self.Cbat # Cbat (battery capacity - taken from battery object - Ah)
		specificenergy = self.specificenergy # specificenergy (taken from battery object - Wh/kg)
		specificvol = self.specificvol # specificvol (taken from battery object - Wh/L)
		
		# calculates for batteries #
		# capacity requirements. Number of batteries must at least provide this capacity
		bateta = 0.97 # bateta (battery-to-load efficiency) - 0% to 100%
		systemvoltage = 28 # 28V is default for most spacecraft systems
		
		Creq = powermax * (eclipsetime / 60) / (bateta * DOD*systemvoltage) # Ah
		
		# add one for redundancy
		batterynums = np.ceil(Creq/Cbat) + 1
		
		# energy capacity of all batteries
		Eb = batterynums * Cbat * systemvoltage # Wh
		
		# mass of batteries
		batterymass = Eb / specificenergy
		
		# size of batteries
		batterysize = Eb / (specificvol *.001)
		
		# assign to the particular object
		self.batterynums = batterynums
		self.batterymass = batterymass
		self.batterysize = batterysize
		return batterynums, batterymass, batterysize

	def printDesc(self):
		print("Power Storage System Info: ")
		print("Numer of batteries: " + str(self.batterynums))
		print("Batteries mass: " + str(self.batterymass))
		print("Batteris size: " + str(self.batterysize))
		
		print("Battery Info: ")
		print("Capacity (Ah): " + str(self.Cbat))
		print("Depth of discharge: " + str(self.DOD))
		print("Specific Energy (Wh/kg): " + str(self.specificenergy))
		print("Specific Energy Volume (Wh/L): " + str(self.specificvol))
		
		
class FuelCell(PowerStorage):
	def __init__(self, name, size, capacity, efficiency):
		''' subclass of Power
		fuel cells
		'''
		PowerStorage.__init__(self, name, size, capacity, "Fuel Cell")
		self.capacity = capacity
		self.efficiency = efficiency
		
	def calc_density(self,td,T):
		''' 
		Calculates densities (W/kg,Whr/kg, W/L, Whr/L) for secondary fuel cells
		Based on 2013 AIAA report "Fuel Cells for Space Applications" written by Kenneth A. Burke of NASA Glenn Research Center
		INPUTS:
		td (dicharge time in hours)
		T (temperature) - can be 200 K
		OUTPUTS:
		rhoP (power density in W/kg)
		rhoE (energy density in Whr/kg)
		gammaP (volume power density in W/L) 1 L = .001 m3
		gammaE (volume energy  density in W*hr/L)
		'''	
		
		# Change as appropriate
		etae = .44 # efficiency
		Vd = 1.68 # discharge / charge voltage (V)
		Id = 1000 # discharge current density (mac/m2)
		Am = 1540 # specific area (cm2/kg)
		mu = 1800 # figure of merit proportion (atm-liter/kg)
		R = .082 # atm-L/(g/mol * K)
		PT = 70*9.86923 # maximum operating pressure of the tank (atm) - based on Toyota Mirai operating pressure
		
		rhoP = (3661*(td**-1)*etae*mu) / (3661*etae*mu*(Vd*Id*Am*td)**-1 + 83.3*R*T+ PT + mu)
		rhoE = rhoP * td
		
		Av = 715 # cm2 / L
		gammaP = 1 / ((td*R*T + .12*PT) / (43.93*etae*PT) + 1/(Vd*Id*Av))
		gammaE = gammaP * td
		return rhoP, rhoE, gammaP, gammaE
	
	def calc_sizemass(self,td,T):
		'''
		Calculates size and mass of secondary fuel cells
		'''
		
		# calculates densities for secondary fuel cells
		rhoP, rhoE, gammaP, gammaE = self.calc_density(self,td,T)
		
		# identify power requirements of the parent class
		power = super(FuelCell,self).powermax
		
		size = power / gammaP
		mass = power / rhoP 
		
		self.size = size
		self.mass = mass
		return size, mass
	
class FlyWheels(PowerStorage):
	def __init__(self, name, size, capacity):
		PowerStorage.__init__(self, name, size, capacity, "Flywheel")
		
		
	