import math

def dist(pos1, pos2):
    distance = 0
    for i in range(0, len(pos1)):
        distance += (pos1[i] - pos2[i]) ** 2
    distance = math.sqrt(distance)
    return distance

def dotProduct(vector1, vector2):
    product = 0
    for i in range(0, len(vector1)):
        product += vector1[i] * vector2[i]
    return product

def crossProduct(vector1, vector2):
    normal = []
    normal.append(vector1[1] * vector2[2] - vector1[2] * vector2[1])
    normal.append(vector1[2] * vector2[0] - vector1[0] * vector2[2])
    normal.append(vector1[0] * vector2[1] - vector1[1] * vector2[0])

#a point
class Vertice:
    def __init__(self, x, y, z):
        #3d coordinates
        self.x = x
        self.y = y
        self.z = z
        self.screenPos = [] #a 2d coordinate for where the vertice is to be displayed onto the screen
#an edge connecting two points
class Edge:
    def __init__(self, vert1, vert2):
        self.vert1 = vert1
        self.vert2 = vert2
#a face with a combination of points and edges
class Face:
    def __init__(self, vertices):
        self.vertices = vertices

#superclass for all objects
class Object:
    def __init__(self, position, rotation, scale):
        self.position = position
        self.pivotPoint = position
        self.rotation = rotation
        self.scale = scale
    def get_pos(self):
        return self.position
    def set_pos(self, pos):
        self.position = pos
    def get_rot(self):
        return self.rotation
    def set_rot(self, rot):
        self.rotation = rot
    def get_scale(self):
        return self.scale
    def set_scale(self, scale):
        self.scale = scale

#mesh is an object that contains vertices, edges, and faces
class Mesh(Object):
    def __init__(self, position, rotation, scale, vertices, edges, faces):
        super().__init__(position, rotation, scale)
        self.vertices = vertices
        self.edges = edges
        self.faces = faces

#the camera projects the scene onto the screen
class Camera(Object):
    def __init__(self, position, rotation, scale, width, height, fov, projectionType = "perspective"):
        super().__init__(position, rotation, scale)
        self.width = width
        self.height = height
        self.fov = fov #field of vision
        self.projectionType = projectionType
        self.cameraVector = [1, 0, 0] #direction vector of where the camera is pointing
        self.xPlane = [0, 1, 0] #normal of the x-plane of the screen (3d points projected onto this plane create corresponding x-positions on a 2d screen)
        self.yPlane = [0, 0, 1] #normal of the y-plane of the screen (3d points projected onto this plane create corresponding y-positions on a 2d screen)
    def project(self, objects):
        for ob in objects:
            if isinstance(ob, Mesh):
                for vert in ob.vertices:
                    if self.projectionType == "perspective":
                        #convert vertice into vector away from camera
                        vector = [(vert.x - self.position[0]), (vert.y - self.position[1]), (vert.z - self.position[2])]

                        #project the vector onto the x-component of the camera
                        xProjection = dotProduct(self.xPlane, vector) / (dist(self.xPlane, [0, 0, 0])**2)
                        xVector = (vector[0] - xProjection * self.xPlane[0], vector[1] - xProjection * self.xPlane[1], vector[2] - xProjection * self.xPlane[2])


                        xAngle = math.degrees(math.acos(dotProduct(self.cameraVector, xVector) / (math.dist(self.cameraVector, [0, 0, 0]) * math.dist(xVector, [0, 0, 0]))))
                        xpos = (self.width * xAngle) / ((self.fov * self.width) / max([self.width, self.height])) + self.width / 2

                        # project the vector onto the x-component of the camera
                        yProjection = dotProduct(self.yPlane, vector) / (dist(self.yPlane, [0, 0, 0]) ** 2)
                        yVector = (vector[0] - yProjection * self.yPlane[0], vector[1] - yProjection * self.yPlane[1], vector[2] - yProjection * self.yPlane[2])

                        yAngle = math.degrees(math.acos(dotProduct(self.cameraVector, yVector) / (math.dist(self.cameraVector, [0, 0, 0]) * math.dist(yVector, [0, 0, 0]))))
                        ypos = (self.height * yAngle) / ((self.fov * self.height) / max([self.width, self.height])) + self.height / 2

                        vert.screenPos = [int(xpos), int(ypos)]