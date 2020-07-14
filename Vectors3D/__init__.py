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
    return normal
def average(vectors):
    average = []
    for i in range(0, len(vectors[0])):
        average.append(0)
        for vector in vectors:
            average[i] += vector[i]
        average[i] /= len(vectors[0])
    return average

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
    def get_verts(self):
        return [self.vert1, self.vert2]
#a face with a combination of points and edges
class Face:
    def __init__(self, vertices, edges=[]):
        self.vertices = vertices
        if len(edges) == 0:
            self.edges = [Edge(vertices[i], vertices[i-1]) for i in range(0, len(vertices))]
        else:
            self.edges = edges
        self.isTri = True
        self.normal = [0, 0, 0]
        self.center = average([[vert.x, vert.y, vert.z] for vert in self.vertices])
        #calculations are easier if faces contain only 3 points. Make a list of subfaces (tris) made up of 3 vertices
        if len(self.vertices) > 3:
            self.isTri = False
            self.tris = []
            for i in range(1, len(self.vertices) - 1):
                triEdges = []
                for edge in self.edges:
                    if edge.vert2 in [self.vertices[0], self.vertices[i], self.vertices[i + 1]] and edge.vert1 in [self.vertices[0], self.vertices[i], self.vertices[i + 1]]:
                        triEdges.append(edge)
                self.tris.append(Face([self.vertices[0], self.vertices[i], self.vertices[i + 1]], triEdges))
        self.calculateNormals()
    def calculateCenter(self):
        if self.isTri:
            self.center = average([[vert.x, vert.y, vert.z] for vert in self.vertices])
        elif not self.isTri:
            for tri in self.tris:
                tri.calculateCenter()
    def calculateNormals(self):
        if self.isTri:
            self.normal = crossProduct([self.vertices[0].x - self.vertices[1].x, self.vertices[0].y - self.vertices[1].y, self.vertices[0].z - self.vertices[1].z],
                                       [self.vertices[0].x - self.vertices[2].x, self.vertices[0].y - self.vertices[2].y, self.vertices[0].z - self.vertices[2].z])
        elif not self.isTri:
            self.normal = average([tri.normal for tri in self.tris])
            for tri in self.tris:
                tri.calculateNormals()


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
        #contains all subfaces, made up only of 3 vertices
        self.tris = []
        for face in self.faces:
            if face.isTri:
                self.tris.append(face)
            elif not face.isTri:
                self.tris += face.tris
    def set_pos(self, pos):
        vector = [pos[i] - self.position[i] for i in range(0, 3)]
        for vert in self.vertices:
            vert.x += vector[0]
            vert.y += vector[1]
            vert.z += vector[2]
        self.position = pos
    def set_rot(self, rot):
        for vert in self.vertices:
            vector = [vert.x - self.pivotPoint[0], vert.y - self.pivotPoint[1], vert.z - self.pivotPoint[2]]
            if rot[0] != 0:
                # x axis
                length = dist([vector[1], vector[2]], [0, 0, 0])
                if vert.y >= self.pivotPoint[1] and vert.z >= self.pivotPoint[2]:
                    vector[1] = length * math.cos(math.radians(math.degrees(math.acos(vector[1] / length)) - self.rotation[0] + rot[0]))
                    vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) - self.rotation[0] + rot[0]))
                elif vert.y < self.pivotPoint[1] and vert.z >= self.pivotPoint[2]:
                    vector[1] = length * math.cos(math.radians(math.degrees(math.acos(vector[1] / length)) - self.rotation[0] + rot[0]))
                    vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) + self.rotation[0] - rot[0]))
                elif vert.y < self.pivotPoint[1] and vert.z < self.pivotPoint[2]:
                    vector[1] = length * math.cos(math.radians(math.degrees(math.acos(vector[1] / length)) + self.rotation[0] - rot[0]))
                    vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) + self.rotation[0] - rot[0]))
                elif vert.y >= self.pivotPoint[1] and vert.z < self.pivotPoint[2]:
                    vector[1] = length * math.cos(math.radians(math.degrees(math.acos(vector[1] / length)) + self.rotation[0] - rot[0]))
                    vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) - self.rotation[0] + rot[0]))

            if rot[1] != 0:
                # y axis
                length = dist([vector[0], vector[2]], [0, 0, 0])
                if vert.x >= self.pivotPoint[0] and vert.z >= self.pivotPoint[2]:
                    vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) - self.rotation[1] + rot[1]))
                    vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) - self.rotation[1] + rot[1]))
                elif vert.x < self.pivotPoint[0] and vert.z >= self.pivotPoint[2]:
                    vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) - self.rotation[1] + rot[1]))
                    vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) + self.rotation[1] - rot[1]))
                elif vert.x < self.pivotPoint[0] and vert.z < self.pivotPoint[2]:
                    vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) + self.rotation[1] - rot[1]))
                    vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) + self.rotation[1] - rot[1]))
                elif vert.x >= self.pivotPoint[0] and vert.z < self.pivotPoint[2]:
                    vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) + self.rotation[1] - rot[1]))
                    vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) - self.rotation[1] + rot[1]))

            if rot[2] != 0:
                # z axis
                length = dist([vector[0], vector[1]], [0, 0, 0])
                if vert.x >= self.pivotPoint[0] and vert.y >= self.pivotPoint[1]:
                    vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) - self.rotation[2] + rot[2]))
                    vector[1] = length * math.sin(math.radians(math.degrees(math.asin(vector[1] / length)) - self.rotation[2] + rot[2]))
                elif vert.x < self.pivotPoint[0] and vert.y >= self.pivotPoint[1]:
                    vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) - self.rotation[2] + rot[2]))
                    vector[1] = length * math.sin(math.radians(math.degrees(math.asin(vector[1] / length)) + self.rotation[2] - rot[2]))
                elif vert.x < self.pivotPoint[0] and vert.y < self.pivotPoint[1]:
                    vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) + self.rotation[2] - rot[2]))
                    vector[1] = length * math.sin(math.radians(math.degrees(math.asin(vector[1] / length)) + self.rotation[2] - rot[2]))
                elif vert.x >= self.pivotPoint[0] and vert.y < self.pivotPoint[1]:
                    vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) + self.rotation[2] - rot[2]))
                    vector[1] = length * math.sin(math.radians(math.degrees(math.asin(vector[1] / length)) - self.rotation[2] + rot[2]))

            vert.x = self.pivotPoint[0] + vector[0]
            vert.y = self.pivotPoint[1] + vector[1]
            vert.z = self.pivotPoint[2] + vector[2]

        self.rotation[0] = rot[0]


#the camera projects the scene onto the screen
class Camera(Object):
    def __init__(self, position, rotation, scale, width, height, fov, projectionType = "perspective"):
        super().__init__(position, rotation, scale)
        self.width = width
        self.height = height
        self.fov = fov #field of vision
        self.projectionType = projectionType
        self.cameraVector = [1, 0, 0] #direction vector of where the camera is pointing
        self.xPlane = [0, 0, 1] #normal of the x-plane of the screen (3d points projected onto this plane create corresponding x-positions on a 2d screen)
        self.yPlane = [0, 1, 0] #normal of the y-plane of the screen (3d points projected onto this plane create corresponding y-positions on a 2d screen)
    def project(self, objects):
        for ob in objects:
            if isinstance(ob, Mesh):
                for vert in ob.vertices:
                    if self.projectionType == "perspective":
                        # convert vertice into vector away from camera
                        vector = [(vert.x - self.position[0]), (vert.y - self.position[1]), (vert.z - self.position[2])]

                        # project the vector onto the x-component of the camera
                        xProjection = dotProduct(self.xPlane, vector) / (dist(self.xPlane, [0, 0, 0])**2)
                        xVector = (vector[0] - xProjection * self.xPlane[0], vector[1] - xProjection * self.xPlane[1], vector[2] - xProjection * self.xPlane[2])

                        # find the angle between the x-component of the vector and the direction of the camera
                        xAngle = math.degrees(math.acos(dotProduct(self.cameraVector, xVector) / (math.dist(self.cameraVector, [0, 0, 0]) * math.dist(xVector, [0, 0, 0]))))
                        #account for negative angles
                        if vector[0] * self.yPlane[0] + vector[1] * self.yPlane[1] + vector[2] * self.yPlane[2] < 0:
                            xAngle *= -1

                        # convert the ratio between the angles into a definite x-position
                        xpos = (self.width * xAngle) / ((self.fov * self.width) / max([self.width, self.height])) + self.width / 2

                        # project the vector onto the x-component of the camera
                        yProjection = dotProduct(self.yPlane, vector) / (dist(self.yPlane, [0, 0, 0]) ** 2)
                        yVector = (vector[0] - yProjection * self.yPlane[0], vector[1] - yProjection * self.yPlane[1], vector[2] - yProjection * self.yPlane[2])

                        # find the angle between the y-component of the vector and the direction of the camera
                        yAngle = math.degrees(math.acos(dotProduct(self.cameraVector, yVector) / (math.dist(self.cameraVector, [0, 0, 0]) * math.dist(yVector, [0, 0, 0]))))
                        if vector[0] * self.xPlane[0] + vector[1] * self.xPlane[1] + vector[2] * self.xPlane[2] < 0:
                            yAngle *= -1

                        # convert the ratio between the angles into a definite y-position
                        ypos = (self.height * yAngle) / ((self.fov * self.height) / max([self.width, self.height])) + self.height / 2

                        # set the screen position of the vertice
                        vert.screenPos = [int(xpos), int(ypos)]
                for face in ob.faces:
                    face.calculateCenter()
                    face.calculateNormals()

                tris = [tri for tri in ob.tris]
                dists = [dist(tri.center, self.position) for tri in ob.tris]
                newTris = []
                while len(tris) > 0:
                    index = dists.index(max(dists))
                    selectedTri = tris[index]
                    newTris.append(selectedTri)
                    tris.pop(index)
                    dists.pop(index)
                ob.tris = newTris