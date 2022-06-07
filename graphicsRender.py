# Note: THis uses a left-handed coordinate system in the clip space

'''
	Information about the pictures
		scene1.png: Light and Camera are at the same position, no rotation or translation, scale = 1
		scene2.png: Light and Camera are at the same position, rotated by 180 degrees along x axis, scale = 1, no translation
		scene3.png: Light and Camera are at the same position, rotated by 180 degrees along x and y axis, scale = 1, translated a bit
		scene4.png: Camera is in a different location than the light, shows shark as if the light is somewhere below it, rotated by 180 degrees along x axis
		scene5.png: Shark is scaled by 0.5, translated a bit, and the light is now red. Camera and light are in different places, and the background is blue
	I hope this is enough to show the capabilities of my program :)
'''

# Imports
import Constants 	as c
import math
import numpy 		as np
import itertools
import graphics

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

def matrix_transform(preTransform, transformMatrix):
	postTransform = []
	for triangle in preTransform:
		transformTriangle = []
		for vertex in triangle:
			transformVertex = vertex @ transformMatrix
			transformTriangle.append(list(transformVertex))
		postTransform.append(transformTriangle)

	return np.array(postTransform)

def unit_vector(vector):
	# Calculates the unit vector for a given numpy array
	return vector / (vector**2).sum()**0.5

def triangle_normal(triangleCoord): # Triangle coords are numpy array
	# Calculates the normal vector for a triangle, returning it as a numpy array unit vector

	# Triangle [p1, p2, p3]
	p1 = triangleCoord[0]
	p2 = triangleCoord[1]
	p3 = triangleCoord[2]

	# U = p2 - p1
	U = np.subtract(p2, p1)
	# P = p3 - p1
	V = np.subtract(p3, p1)

	# Nx = UyVz - UzVy
	# Ny = UzVx - UxVz
	# Nz = UxVy - UyVx
	Nx = (U[1] * V[2]) - (U[2] * V[1])
	Ny = (U[2] * V[0]) - (U[0] * V[2])
	Nz = (U[0] * V[1]) - (U[1] * V[0])
	vector = np.array([Nx, Ny, Nz])

	return unit_vector(vector)

def light_vector(triangleCoord): # Triangle coords are numpy array
	# Averages the three vertexes into one, and creates a unit vector coming from this average to the light source
	avg_X = (triangleCoord[0][0] + triangleCoord[1][0] + triangleCoord[2][0]) / 3
	avg_Y = (triangleCoord[0][1] + triangleCoord[1][1] + triangleCoord[2][1]) / 3
	avg_Z = (triangleCoord[0][2] + triangleCoord[1][2] + triangleCoord[2][2]) / 3

	avg = np.array([avg_X, avg_Y, avg_Z])

	# Vector from avg to light = light - avg
	lightVec = np.subtract(np.array(c.LIGHT_POS), avg)

	# Normalize the light vector
	return unit_vector(lightVec)

def triangle_light(triangleNormal, lightVector):
	# Takes in a triangle normal and applies diffuse lighting effects to it, returning a list of the RGB color for that triangle
	C_LIGHT = np.array([c.M_DIFF[0] * c.C_LIGHT[0], c.M_DIFF[1] * c.C_LIGHT[1], c.M_DIFF[2] * c.C_LIGHT[2]])

	# Dot product between triangleNormal and lightVector
	dot = np.dot(triangleNormal, lightVector)
	# Scale the entire vector to determine brightness
	return C_LIGHT * max(0, dot)


	
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

	return matrix_transform(preTransform, transformMatrix)

def light(model):
	# Performs diffuse light calculations on the model, returning a numpy array where each entry is the RGB color of the associated triangle of the model
	# This is done AFTER world transformation

	modelLightArray = []
	# Go through the model and get the triangle coordinates, give it to a function to calculate the normal for that triangle
	for triangleCoord in model:
		normalUnitVector = triangle_normal(triangleCoord)
		lightUnitVector  = light_vector(triangleCoord)
		# Get the light color and brightness for the triangle
		modelLightArray.append(triangle_light(normalUnitVector, lightUnitVector))

	return np.array(modelLightArray)

def view_transform(preTransform):
	# For each coordinate, transform it into the view space

	eye = np.array(c.CAM_POS)
	up = np.array([0, 1, 0])
	at = c.CAM_DIR

	z_axis = unit_vector(np.subtract(at, eye))
	x_axis = unit_vector(np.cross(up, z_axis))
	y_axis = np.cross(z_axis, x_axis)

	# Transform Matrix
	transformMatrix = (	[ x_axis[0],            y_axis[0],            z_axis[0],           0],
						[ x_axis[1],            y_axis[1],            z_axis[1],           0],
						[ x_axis[2],            y_axis[2],            z_axis[2],           0],
						[-np.dot(x_axis, eye), -np.dot(y_axis, eye), -np.dot(z_axis, eye), 1])

	return matrix_transform(preTransform, transformMatrix)

def persp_transform(preTransform):
	# Same thing as view transform
	yscale = 1 / (np.tan(np.radians(c.FOV/2)))
	xscale = yscale / c.ASPECT_RATIO

	# Variables for shorter names
	zn = c.NEAR_PLANE
	zf = c.FAR_PLANE

	transformMatrix = (	[xscale, 0,      0,                0],
						[0,      yscale, 0,                0],
						[0,      0,      zf/(zf-zn),       1],
						[0,      0,      (-zn*zf)/(zf-zn), 0])

	return matrix_transform(preTransform, transformMatrix)

def w_divide(preTransform):
	# Divide each vertex by its w, then remove the w
	postTransform = []
	for triangle in preTransform:
		transformTriangle = []
		for vertex in triangle:
			transformVertex = np.divide(vertex, vertex[3])
			transformVertex = np.delete(transformVertex, 3)
			transformTriangle.append(list(transformVertex))
		postTransform.append(transformTriangle)

	return np.array(postTransform)

def sortAvgZ(e):
	return (e[0][2] + e[1][2] + e[2][2]) / 3

def clip_sort(preClip):
	# Takes in a list and clip, then sort from lowest Z to highest
	postClip = [x for x in preClip if 0 < x[0][2] < 1 and 0 < x[1][2] < 1 and 0 < x[2][2] < 1]

	postClip.sort(reverse = True, key = sortAvgZ)

	return postClip

# Code starts here

# Turn the model into a numpy array
modelArray = read_model(c.FILENAME)
# Apply world transformations on the model
worldTransformModelArray = world_transform(modelArray)
# Apply Lighting
lightingArray = light(worldTransformModelArray)
# View Transformation
viewTransformModelArray = view_transform(worldTransformModelArray)
# Clip Space Transform
clipSpaceModelArray = persp_transform(viewTransformModelArray)
# Divide by w for perspective effect
perspective = w_divide(clipSpaceModelArray)

# Append the lighting colors to each triangle to avoid losing it while sorting and clipping
preClip = []
for triangle, color in zip(list(perspective), list(lightingArray)):
	preClip.append([list(triangle[0]), list(triangle[1]), list(triangle[2]), list(color)])

# Clip the triangles that have a vertex with a Z that is not [0, 1]
postClip = clip_sort(preClip)

# Draw the image
winSize = 1000
win=graphics.GraphWin("Render",winSize,winSize)
win.setBackground(c.backgroundColor)
for vertex1, vertex2, vertex3, rgb in postClip:
	vertices = [graphics.Point((vertex1[0] * winSize) + winSize/2, (-vertex1[1] * winSize) + winSize/2), graphics.Point((vertex2[0] * winSize) + winSize/2, (-vertex2[1] * winSize) + winSize/2), graphics.Point((vertex3[0] * winSize) + winSize/2, (-vertex3[1] * winSize) + winSize/2)]
	color = graphics.color_rgb(int(rgb[0] * 256), int(rgb[1] * 256), int(rgb[2] * 256))
	triangle = graphics.Polygon(vertices)
	triangle.setFill(color)
	triangle.draw(win)

print("Image rendered, click the window to close it")
win.getMouse()
win.close() 