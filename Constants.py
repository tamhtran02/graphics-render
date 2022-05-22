# Constants to change, change these for different renders
# General
FILENAME = "test.raw"
'''
	Light and Camera
'''
LIGHT_POS = [0, 0, 0]
LIGHT_RGB = [1, 1, 1]

CAM_POS   = [0, 0, 0]
CAM_DIR   = [1, 1, 1]
'''
	Transformations
	Done in the order of:
		1) Scale
		2) Rotate
		3) Translation
'''
# Object Scaling
X_SCALE = 0.5
Y_SCALE = 0.5
Z_SCALE = 0.5
# Object Rotation in Direct3D conventions: Angles are measured clockwise when looking along the rotation axis toward the origin.
X_ROT   =  45
Y_ROT   = -45
Z_ROT   =   0
# Object Translation
X_TRAN  = 5
Y_TRAN  = 5
Z_TRAN  = 5

'''
	Projection
'''
# Perspective Projection
FOV          = 60
ASPECT_RATIO =  1
NEAR_PLANE   =  1
FAR_PLANE    = 20