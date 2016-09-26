import numpy as np
'''Functions useful for reference frame'''

def euler2dcm(psi, theta, phi):
# yaw-pitch-roll angles aka Tait-Bryan angles
# NOTE:
# yaw = psi
# pitch = theta
# roll = phi
# Order of matrix multiplication is as follows:
# 1. Multiply by yaw (psi) matrix.
# 2. Multiply by pitch (theta) matrix.
# 3. Multiply by roll (phi) matrix.
# intrinsic rotation (use axes of rotating coordinate system)
# Note:
# Only difference is that Tait–Bryan angles represent rotations about three distinct axes (e.g. x-y-z, or x-y’-z″), while proper Euler angles use the same axis for both the first and third elemental rotations (e.g., z-x-z, or z-x’-z″).
# Order of rotations: z, y', x"
	psirot = np.matrix([[np.cos(psi), np.sin(psi), 0], [-np.sin(psi), np.cos(psi), 0], [0, 0, 1]])
	thetarot = np.matrix([[np.cos(theta), 0, -np.sin(theta)], [0, 1, 0], [np.sin(theta), 0, np.cos(theta)]])
	phirot = np.matrix([[1, 0, 0], [0, np.cos(phi), np.sin(phi)], [0, -np.sin(phi), np.cos(phi)]])
	# Rrot = phirot * thetarot * psirot
	# DCM means direction cosine matrix
	DCM = phirot.dot(thetarot).dot(psirot)
	return DCM

def dcm2euler(DCM):
	'''Convert direction cosine matrix to yaw, pitch, and roll angles
	yaw = psi
	pitch = theta
	roll = phi
	'''
	psi = np.arctan2(DCM.item(0,1), DCM.item(0,0))
	theta = np.arctan2(-DCM.item(0,2), np.sqrt(1 - DCM.item(0,2)**2))
	phi = np.arctan2(DCM.item(1,2), DCM.item(2,2))
	print(psi)
	print(theta)
	print(phi)
	return psi, theta, phi
	
def dcm2q(DCM):
	'''Convert direction cosine matrix (DCM) to quarternion form'''
	T = np.trace(DCM)
	q4 = 0.5 * (1 + T) ** 0.5
	q1 = (DCM.item(1,2) - DCM.item(2,1)) / (4*q4)
	q2 = (DCM.item(2,0) - DCM.item(0,2)) / (4*q4)
	q3 = (DCM.item(0,1) - DCM.item(1,0)) / (4*q4)
	q = np.array([[q1], [q2], [q3], [q4]])
	return q
	
def q2dcm(q):
	'''Convert quarternion to direction cosine matrix (DCM)'''
	q1 = q.item(0)
	q2 = q.item(1)
	q3 = q.item(2)
	q4 = q.item(3)
	
	c11 = 2*q4**2 + 2*q1**2 - 1
	c21 = 2*q1*q2 - 2*q4*q3
	c31 = 2*q1*q3 + 2*q4*q2
	c12 = 2*q1*q2 + 2*q4*q3
	c22 = 2*q4**2 + 2*q2**2 - 1
	c32 = 2*q2*q3 - 2*q4*q1
	c13 = 2*q1*q3 - 2*q4*q2
	c23 = 2*q2*q3 + 2*q4*q1
	c33 = 2*q4**2 + 2*q3**2 - 1
	DCM = np.matrix([[c11, c12, c13],[c21,c22,c23],[c31,c32,c33]])
	return DCM
	
def rotate(q, r):
	'''Define vector in another coordinate system
	Input: 4-vector quarternion
	Output: 3x1 position vector 
	'''
	DCM = q2dcm(q)
	rnew = DCM*r
	return rnew