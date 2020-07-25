from Vectors3D import *
from Vectors3D.object import Object

#mesh is an object that contains vertices, edges, and faces
class Mesh(Object):
    def __init__(self, position, rotation, scale, vertices, edges, faces):
        super().__init__(position, rotation, scale)
        self.vertices = vertices
        self.edges = edges
        self.faces = faces
        self.selectedVertices = [self.vertices[40]]
        self.selectedEdges = []
        self.selectedFaces = []
        #contains all subfaces, made up only of 3 vertices
        self.tris = []
        for face in self.faces:
            if face.isTri:
                self.tris.append(face)
            elif not face.isTri:
                self.tris += face.tris
    def set_pos(self, pos):
        # find the vector connecting the initial position and the final position
        vector = [pos[i] - self.position[i] for i in range(0, 3)]
        if self.mode == "object":
            # add that vector to all the vertices so that they all move along with the object
            for vert in self.vertices:
                vert.x += vector[0]
                vert.y += vector[1]
                vert.z += vector[2]
            self.position = pos
        elif self.mode == "edit":
            for vert in self.selectedVertices:
                vert.x += vector[0]
                vert.y += vector[1]
                vert.z += vector[2]
    def set_rot(self, rot):
        for vert in self.vertices:
            # find the vector connecting the object position (which will function as a pivot point) to the vertice position
            vector = [vert.x - self.position[0], vert.y - self.position[1], vert.z - self.position[2]]
            if dist(vector, [0, 0, 0]) != 0:
                if rot[0] != 0:
                    # x axis
                    # x axis rotations will only affect the y and z axis components of the vector
                    # distance of the vector only in the y and z axis
                    length = dist([vector[1], vector[2]], [0, 0])

                    # adjust the vector to be offset by the difference between the initial rotation and final rotation in the x axis
                    # different vertice orientations must be accounted for differently for consistent results
                    if vert.y >= self.position[1] and vert.z >= self.position[2]:
                        vector[1] = length * math.cos(math.radians(math.degrees(math.acos(vector[1] / length)) - self.rotation[0] + rot[0]))
                        vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) - self.rotation[0] + rot[0]))
                    elif vert.y < self.position[1] and vert.z >= self.position[2]:
                        vector[1] = length * math.cos(math.radians(math.degrees(math.acos(vector[1] / length)) - self.rotation[0] + rot[0]))
                        vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) + self.rotation[0] - rot[0]))
                    elif vert.y < self.position[1] and vert.z < self.position[2]:
                        vector[1] = length * math.cos(math.radians(math.degrees(math.acos(vector[1] / length)) + self.rotation[0] - rot[0]))
                        vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) + self.rotation[0] - rot[0]))
                    elif vert.y >= self.position[1] and vert.z < self.position[2]:
                        vector[1] = length * math.cos(math.radians(math.degrees(math.acos(vector[1] / length)) + self.rotation[0] - rot[0]))
                        vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) - self.rotation[0] + rot[0]))

                    # new vertice position will be the result of the object position and the new vector
                    vert.x = self.position[0] + vector[0]
                    vert.y = self.position[1] + vector[1]
                    vert.z = self.position[2] + vector[2]

                if rot[1] != 0:
                    # y axis
                    # y axis rotations will only affect the x and z axis components of the vector
                    # distance of the vector only in the x and z axis
                    length = dist([vector[0], vector[2]], [0, 0])
                    if vert.x >= self.position[0] and vert.z >= self.position[2]:
                        vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) - self.rotation[1] + rot[1]))
                        vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) - self.rotation[1] + rot[1]))
                    elif vert.x < self.position[0] and vert.z >= self.position[2]:
                        vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) - self.rotation[1] + rot[1]))
                        vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) + self.rotation[1] - rot[1]))
                    elif vert.x < self.position[0] and vert.z < self.position[2]:
                        vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) + self.rotation[1] - rot[1]))
                        vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) + self.rotation[1] - rot[1]))
                    elif vert.x >= self.position[0] and vert.z < self.position[2]:
                        vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) + self.rotation[1] - rot[1]))
                        vector[2] = length * math.sin(math.radians(math.degrees(math.asin(vector[2] / length)) - self.rotation[1] + rot[1]))

                    # new vertice position will be the result of the object position and the new vector
                    vert.x = self.position[0] + vector[0]
                    vert.y = self.position[1] + vector[1]
                    vert.z = self.position[2] + vector[2]

                if rot[2] != 0:
                    # z axis
                    # z axis rotations will only affect the x and y axis components of the vector
                    # distance of the vector only in the x and y axis
                    length = dist([vector[0], vector[1]], [0, 0])
                    if vert.x >= self.position[0] and vert.y >= self.position[1]:
                        vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) - self.rotation[2] + rot[2]))
                        vector[1] = length * math.sin(math.radians(math.degrees(math.asin(vector[1] / length)) - self.rotation[2] + rot[2]))
                    elif vert.x < self.position[0] and vert.y >= self.position[1]:
                        vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) - self.rotation[2] + rot[2]))
                        vector[1] = length * math.sin(math.radians(math.degrees(math.asin(vector[1] / length)) + self.rotation[2] - rot[2]))
                    elif vert.x < self.position[0] and vert.y < self.position[1]:
                        vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) + self.rotation[2] - rot[2]))
                        vector[1] = length * math.sin(math.radians(math.degrees(math.asin(vector[1] / length)) + self.rotation[2] - rot[2]))
                    elif vert.x >= self.position[0] and vert.y < self.position[1]:
                        vector[0] = length * math.cos(math.radians(math.degrees(math.acos(vector[0] / length)) + self.rotation[2] - rot[2]))
                        vector[1] = length * math.sin(math.radians(math.degrees(math.asin(vector[1] / length)) - self.rotation[2] + rot[2]))

                    # new vertice position will be the result of the object position and the new vector
                    vert.x = self.position[0] + vector[0]
                    vert.y = self.position[1] + vector[1]
                    vert.z = self.position[2] + vector[2]

        self.rotation = rot

    def selectVert(self, mousePos):
        for vert in self.vertices:
            distance = dist(vert.screenPos, mousePos)
            if distance <= 5:
                return vert

    #returns all edges connected to a vertice
    def edgesFrom(self, vertice):
        edges = []
        for edge in self.edges:
            if vertice in edge.get_verts():
                edges.append(edge)
        return edges
    # returns all tris connected to a vertice
    def trisFrom(self, vertice):
        tris = []
        for tri in self.tris:
            if vertice in tri.vertices:
                tris.append(tri)
        return tris
    #returns all faces connected to a vertice
    def facesFrom(self, vertice):
        faces = []
        for face in self.edges:
            if vertice in face.vertices:
                faces.append(face)
        return faces