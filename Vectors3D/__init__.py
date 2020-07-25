import math
import itertools
import pygame as pg

# returns the distance between two points, regardless of dimensions
def dist(pos1, pos2):
    distance = 0
    #iterate through each axis
    for i in range(0, len(pos1)):
        distance += (pos1[i] - pos2[i]) ** 2
    distance = math.sqrt(distance)
    return distance

# returns dot product of 2 vectors, regardless of dimensions
def dotProduct(vector1, vector2):
    product = 0 # product is a scalar value
    for i in range(0, len(vector1)):
        product += vector1[i] * vector2[i]
    return product

# returns the cross product of 2 vectors
def crossProduct(vector1, vector2):
    normal = [] # result of cross product is a vector perpendicular to both vectors, the normal
    normal.append(vector1[1] * vector2[2] - vector1[2] * vector2[1])
    normal.append(vector1[2] * vector2[0] - vector1[0] * vector2[2])
    normal.append(vector1[0] * vector2[1] - vector1[1] * vector2[0])
    return normal

#returns the average location of a series of points, regardless of dimensions
def average(vectors):
    average = [] # average point
    #iterate through each axis
    for i in range(0, len(vectors[0])):
        average.append(0)
        for vector in vectors:
            average[i] += vector[i]
        average[i] /= len(vectors[0])
    return average

def factorVector(vector):
    newVector = []
    maxVal = max(vector)
    if abs(min(vector)) > maxVal:
        maxVal = abs(min(vector))

    if vector[0] < 0:
        maxVal *= -1

    if maxVal == 0:
        return vector
    else:
        for i in vector:
            newVector.append(i / maxVal)
        return newVector

# a point in 3D space
class Vertice:
    def __init__(self, x, y, z):
        # 3D coordinates
        self.x = x
        self.y = y
        self.z = z
        self.screenPos = [] # a 2D coordinate for where the vertice is to be displayed onto the screen
    def get_pos(self):
        return self.x, self.y, self.z
    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]

# an edge connecting two points
class Edge:
    def __init__(self, vert1, vert2):
        # the 2 points are inputed as Vertices
        self.vert1 = vert1
        self.vert2 = vert2
    # returns the vertices the edge connects
    def get_verts(self):
        return [self.vert1, self.vert2]

# a face with a combination of points and edges
class Face:
    def __init__(self, vertices, edges=[]):
        self.vertices = vertices # lists all the points that the face connects to, as Vertices

        # unless otherwise given, the edges will be created by joining Vertices in the order they were inputed
        if len(edges) == 0:
            self.edges = [Edge(vertices[i], vertices[i-1]) for i in range(0, len(vertices))]
        else:
            # edges can be defined manually
            self.edges = edges
        self.isTri = True # states wether or not the face is made of only 3 points
        self.normal = [0, 0, 0] # the vector perpendicular to the face
        self.center = average([[vert.x, vert.y, vert.z] for vert in self.vertices]) #the center of the face

        # calculations are easier if faces are triangles made only of 3 points.
        # subfaces (tris) are created to break down the face into triangles
        if len(self.vertices) > 3:
            self.isTri = False # the face is not a tri
            self.tris = [] # lists all triangle subfaces
            for i in range(1, len(self.vertices) - 1):
                # since the parent face is not a triangle, some edges that a triangle would normally have will not exist in the parent face
                # determine which edges of the triangle are present in the parent face
                # if an edge in the tri does not exist in the parent face, it won't be a part of it's edge list
                triEdges = []
                for edge in self.edges:
                    if edge.vert2 in [self.vertices[0], self.vertices[i], self.vertices[i + 1]] and edge.vert1 in [self.vertices[0], self.vertices[i], self.vertices[i + 1]]:
                        triEdges.append(edge)
                self.tris.append(Face([self.vertices[0], self.vertices[i], self.vertices[i + 1]], triEdges))
        #faces cannot be made from 2 points, they are edges
        elif len(self.vertices) < 3:
            print("yeet")
            del self
        elif len(self.vertices) == 3 and self.vertices[0].get_pos() == self.vertices[1].get_pos() and self.vertices[0].get_pos() == self.vertices[2].get_pos() and self.vertices[2].get_pos() == self.vertices[1].get_pos():
            print("yeet")
            del self
        print(len(self.vertices))
        print(self.isTri)
        self.calculateNormals() # determine the normal vectors
        print(self.normal)

    # calculates the middle of the face, as well as its subfaces
    def calculateCenter(self):
        if self.isTri:
            self.center = average([[vert.x, vert.y, vert.z] for vert in self.vertices])
        elif not self.isTri:
            for tri in self.tris:
                tri.calculateCenter()

    # calculates the normal vector of the face, as well as its subfaces
    def calculateNormals(self):
        if self.isTri:
            self.normal = crossProduct([self.vertices[0].x - self.vertices[1].x, self.vertices[0].y - self.vertices[1].y, self.vertices[0].z - self.vertices[1].z],
                                       [self.vertices[0].x - self.vertices[2].x, self.vertices[0].y - self.vertices[2].y, self.vertices[0].z - self.vertices[2].z])
        elif not self.isTri:
            self.normal = average([tri.normal for tri in self.tris])
            for tri in self.tris:
                tri.calculateNormals()

def createSphere(segments, rings):
    vertices = []
    edges = []
    faces = []
    for ring in range(0, rings + 1):
        z = math.cos(math.radians(ring * (180 / rings)))#2 / rings * (ring - rings/2)
        r = math.sqrt(1 - z ** 2)
        for segment in range(0, segments + 1):
            dAngle = 360 / segments
            x = r * math.cos(math.radians(segment * dAngle))
            y = r * math.sin(math.radians(segment * dAngle))
            vertices.append(Vertice(x, y, z))
            if len(vertices) > 2:
                edges.append(Edge(vertices[-1], vertices[-2]))
            if len(vertices) - 1 > segments:
                edges.append(Edge(vertices[-1], vertices[-segments - 2]))
            if ring > 1 and ring < rings and segment > 0:
                faces.append(Face([vertices[-1], vertices[-2], vertices[-segments - 3], vertices[-segments - 2]]))
                #print(vertices[-1].get_pos())
                #print(vertices[-2].get_pos())
                #print(vertices[-segments - 1].get_pos())
    return Mesh((0, 0, 0), [0, 0, 0], [1, 1, 1], vertices, edges, faces)

from Vectors3D.camera import Camera
from Vectors3D.mesh import Mesh
from Vectors3D.object import Object