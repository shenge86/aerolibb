import numpy as np

# Telecommunications subsystem
# Typically, need to maximize EIRP (and hence EbN0) under the constraint of a max power, mass, and size.
# Sometimes, we are given satellite transmitter power requirements and the frequency so we can do the reverse of finding the mass.

class Telecom:
	def __init__(self, f, Pmax, mmax, Amax):
		'''Inputs:
		f (frequency of tranmission)
		Pmax (maximum power allowed for transmitting antenna)
		mMax (maximum mass allowed for atenna and corresponding power supply)
		Amax (maximum area allowed for antenna)
		
		
		Note:
		Pmax will depend on the power available
		Amax will depend on the launch vehicle shroud size
		
		# For DSN:
		4 dB for X-band or Ka-band
		'''
		
		self. f = f
		self.Pmax = Pmax
		self.mmax = mmax
		self.Amax = Amax
	
	def calc_EIRP(self, f, mmax):
		# Optimize EIRP with mass constraint and given frequency
		# Inputs:
		# f (Hz)
		# mMax (kg)
		#
		# Outputs:
		# D: antenna diameter (m)
		# Pt: transmitter power (W)
		# Gt: transmitter gain
		# EIRP: effective isotropic radiated power  (W)
		# theta: half-power beamwidth (angle across which gain is within 3  dB aka 50% of peak gain) (degrees)
		
		# assume parabolic
		eta = .65
		c = 3e8 / .3048 # feet/s (speed of light)
		coeff = [-16 * eta * np.pi**2 * f**2 / c**2, 0, 4*eta*np.pi**2*(mmax-40)*f**2/c**2, 0]
		D = np.roots(coeff)
		D = np.around(np.max(D),3)
		print(D)
		Pt = 2*(mmax-40)  - 4*D**2
		Gt = eta*(np.pi*D*f/c)**2
		EIRP = Gt*Pt
		print(Pt)
		print(EIRP)
		
		D = D *.3048 # meters
		theta = 21 / (f * D)
		
		self.D = D
		self.Pt = Pt
		return D, Pt, Gt, EIRP, theta
		
	def calc_EbN0(self, EIRP,  Rb, R, f):
		# link equation
		# Inputs:
		# EIRP
		# Rb energy per bit (J) per N0 noise spectral density (W/Hz)
		# R (m) distance from transmitter to receiver
		# f (Hz) frequency
		
		k = 228.6 # (dB) Boltzmann's constant
		
		Lm = 0.9698 # data modulation loss - data power to total power
		Lt = 0.9 # transmitter circuit loss ?????????
		Lp = 0.9 # performance margin for tolerances and weather  ?????????
		
		losses = Lm + Lt + Lp
		
		Gr = 73.89 # receiver gain
		Tr = 24.98 # K - receiver system temperature - comment out if known
		
		FSL = 32.4 + 20*np.log10(R)  + 20*np.log10(f)
		
		EbN0 = EIRP + Gr / Tr - FSL - k - losses
		return EbN0
		
	# Use to find total mass (assuming no mass constraint given but power, distance, frequency is given).
	def calc_mass(self, pT, R, f):
		'''INPUTS:
		pT in W (transmitting power)
		R in m (distance from transmitter to receiver) 
		f in Hz (frequency of signal)
		# for DSN:
		8.45 GHz (X-band)
		32.0 GHz (Ka-band)
		
		OUTPUTS:
		mpar (mass of antenna if parabolic)
		mflat (mass of antenna if flat)
		
		NOTES:
		Most of these constants come from spacecraft mass tradeoffs.
		'''
		
		# Constants
		k = 1.3806e-13 # joules/kevin (Boltzmann's constant)
		c = 3e8 # m (speed of light)
		
		# System parameters 
		EbN0 = self.EbN0
		# For DSN:
		# 4 dB for X-band or Ka-band < - should not be in dB for these calculations
		Tsys = 24.98 # kelvin (system noise temperature) 
		# For DSN:
		# 24.98 K for X-band
		# 31.2 K for Ka-bond
		GR = 73.89 # gain
		# For DSN:
		# 73.89 for X-band
		# 84.84 for Ka-band
		
		#==========for parabolics=========#
		kT = .434 # kg/W
		kC = .38 # kg/sqrt(W)
		etaApar = .55 # for parabola
		etaT = .90 # (efficiency to convert raw DC power to radio frequency power) ???????????????
		kA = 2.94 # kg/m2 (antenna mass per physical area) 
		
		Lm = 0.9698 # data modulation loss - data power to total power
		Lt = 0.9 # transmitter circuit loss ?????????
		Lp = 0.9 # performance margin for tolerances and weather  ?????????
		Tb = 1 # s (bit time) ????????
		
		B1 = EbN0 * k * Tsys * 4 * np.pi * R**2 / (GR*etaT*Lm*Lt*Tb*Lp)
		
		mpar = kT * pT + etaApar * kA * (B1/pT) + kC * np.sqrt(pT / etaT)
		
		#=========for flat=============#
		etaAflat = .90 # for flat
		kA = 25.7 # kg/m2 (antenna area to mass)
		kR = 20.77 # kg/m2 (radiator area to mass)
		kC = .537 # kg/sqrt(W) (power converter power to mass)
		
		wavelength = c / f # m (wavelength of signal)
		D = 1 # seperation of elements relative to wavelength
		A0 = (D*wavelength) ** 2 # m2 (area of one antenna element)
		
		N = 10 # number of antenna elements in each row and column
		p0 = pT / (N**2) # W (power for each element)
		
		AT = N**2 * A0 # m2 (one-sided physical area of flat plate)
		
		# m = 0, 1, 2, ... , 22 for 8 GHz (max power = 2.5 W, m = 50)
		# m = 0, 1, 2, ... , 8 for 32 GHz (max power = 0.05 W, m = 8)
		# M = 1/4 (m, M are selected for computing values of radio-frequency powers and masses in plotting)
		m = 50	
		M = 1/4
		
		mA = etaAflat * kA * AT # mass of antenna
		mT = 0.1 * kA * AT  * (10**(0.01574*m)) # mass of transmitter
		
		AD = 2*AT # radiator area  (NOTE: if radiator area is smaller than 2*AT, then we don't need a radiator!)
		B2 = AD / pT
		mR = kR * (p0 * N**2 * (2**M)**m * B2) - 2*A0*N**2# mass of radiator
		
		mC = kC*np.sqrt(pT/etaT) # mass of converter
		
		mflat =  mA + mT + mR + mC
		
		self.mpar = mpar
		self.mflat = mflat
		return mpar, mflat