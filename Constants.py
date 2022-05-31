# Constants to change, change these for different renders
# General
FILENAME = "shark_ag.raw"
'''
	Light and Camera
'''
LIGHT_POS = [20, 20, 20]
LIGHT_RGB = [1, 1, 1]

CAM_POS   = [20, 20, 20]
CAM_DIR   = [0, 0, 0]

# The RGB color of the diffuse material reflectance of the object
M_DIFF	= [1, 1, 1]
# The RGB color of the light
C_LIGHT = [1, 1, 1]

'''
	Transformations
	Done in the order of:
		1) Scale
		2) Rotate
		3) Translation
'''
# Object Scaling
X_SCALE = 1
Y_SCALE = 1
Z_SCALE = 1
# Object Rotation in Direct3D conventions: Angles are measured clockwise when looking along the rotation axis toward the origin.
X_ROT   = 0
Y_ROT   = 0
Z_ROT   =   0
# Object Translation
X_TRAN  = 0
Y_TRAN  = 0
Z_TRAN  = 0

'''
	Projection
'''
# Perspective Projection
FOV          = 90
ASPECT_RATIO =  1
NEAR_PLANE   = 5
FAR_PLANE    = 50