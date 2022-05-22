# Imports
import Constants 	as c
import math
import numpy 		as np

# Function Declarations
def read_model(filename):
	f = open(filename, "r")
	model = []

	for line in f:
		triangle = list(map(float, line.strip().split(" ")))
		# Add the 'w' to each vertex as a 1
		triangle.insert(3, 1)
		triangle.insert(7, 1)
		triangle.append(1)

		triangle = np.array_split(np.array(triangle), 3)
		triangle = [list(array) for array in triangle]

		model.append(triangle)

	f.close();
	return np.array(model)

def world_transform(preTransform):
	# Create the matrices used for transformation, did not combine them for clarity
	# Scale
	scale =	(	[c.X_SCALE, 0,         0,         0],
				[0,         c.Y_SCALE, 0,         0],
				[0,         0,         c.Z_SCALE, 0],
				[0,         0,         0,         1])

	# Convert each rotation degrees to radians and put on matrix
	# Rotate
	x_rad = math.radians(c.X_ROT)
	y_rad = math.radians(c.Y_ROT)
	z_rad = math.radians(c.Z_ROT)
	rotateX = (	[1,  0,               0,               0], 
				[0,  math.cos(x_rad), math.sin(x_rad), 0], 
				[0, -math.sin(x_rad), math.cos(x_rad), 0],
				[0,  0,               0,               1])
	rotateY = (	[math.cos(y_rad), 0, -math.sin(y_rad), 0], 
				[0,               1,  0,               0], 
				[math.sin(y_rad), 0,  math.cos(y_rad), 0],
				[0,               0,  0,               1])
	rotateZ = (	[ math.cos(z_rad), math.sin(z_rad), 0, 0], 
				[-math.sin(z_rad), math.cos(z_rad), 0, 0], 
				[0,                0,               1, 0],
				[0,                0,               0, 1])

	# Translate
	translate = (   [1,        0,        0,        0],
					[0,        1,        0,        0],
					[0,        0,        1,        0],
					[c.X_TRAN, c.Y_TRAN, c.Z_TRAN, 1])

	# Multiply Matrices Together
	transformMatrix = np.array(scale) @ np.array(rotateX) @ np.array(rotateY) @ np.array(rotateZ) @ np.array(translate)

	# Loop through the model and for each triangle, divide into 3 different matrices, multiply with transform, then append back together
	postTransform = []
	for triangle in preTransform:
		transformTriangle = []
		for vertex in triangle:
			transformVertex = vertex @ transformMatrix
			transformTriangle.append(list(transformVertex))
		postTransform.append(transformTriangle)

	return np.array(postTransform)


# Code starts here

# Turn the model into a numpy array
model = read_model(c.FILENAME)
# Apply world transformations on the model
worldTransformModel = world_transform(model)