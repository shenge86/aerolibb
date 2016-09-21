import numpy as np

def euler(psi, theta, phi):
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
	Rrot = phirot.dot(thetarot).dot(psirot)
	return Rrot
	
