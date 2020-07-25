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


#superclass for all objects
class Object:
    def __init__(self, position, rotation, scale, mode = "object"):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.mode = mode #different objects will have different modes that can be activated for specific features
        self.selected = False
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


#the camera projects the scene onto the screen
class Camera(Object):
    def __init__(self, position, rotation, scale, width, height, fov, projectionType = "perspective", displayType = "solid"):
        super().__init__(position, rotation, scale)
        self.width = width
        self.height = height
        self.fov = fov # field of vision
        self.projectionType = projectionType
        self.cameraVector = [1, 0, 0] # direction vector of where the camera is pointing
        self.xPlane = [0, 0, 1] # normal of the x-plane of the screen (3d points projected onto this plane create corresponding x-positions on a 2d screen)
        self.yPlane = [0, 1, 0] # normal of the y-plane of the screen (3d points projected onto this plane create corresponding y-positions on a 2d screen)
        self.screen = pg.display.set_mode((self.width, self.height))
        self.displayType = displayType
    def projectPoint(self, point):
        if self.projectionType == "perspective":
            # convert vertice into vector away from camera
            vector = [(point[0] - self.position[0]), (point[1] - self.position[1]), (point[2] - self.position[2])]

            # project the vector onto the x-component of the camera
            xProjection = dotProduct(self.xPlane, vector) / (dist(self.xPlane, [0, 0, 0]) ** 2)
            xVector = (vector[0] - xProjection * self.xPlane[0], vector[1] - xProjection * self.xPlane[1],
                       vector[2] - xProjection * self.xPlane[2])

            # find the angle between the x-component of the vector and the direction of the camera
            try:
                xAngle = math.degrees(math.acos(dotProduct(self.cameraVector, xVector) / (math.dist(self.cameraVector, [0, 0, 0]) * math.dist(xVector, [0, 0, 0]))))
            except:
                xAngle = 90
            # account for negative angles
            if vector[0] * self.yPlane[0] + vector[1] * self.yPlane[1] + vector[2] * self.yPlane[2] < 0:
                xAngle *= -1

            # convert the ratio between the angles into a definite x-position
            xpos = (self.width * xAngle) / ((self.fov * self.width) / max([self.width, self.height])) + self.width / 2

            # project the vector onto the x-component of the camera
            yProjection = dotProduct(self.yPlane, vector) / (dist(self.yPlane, [0, 0, 0]) ** 2)
            yVector = (vector[0] - yProjection * self.yPlane[0], vector[1] - yProjection * self.yPlane[1],
                       vector[2] - yProjection * self.yPlane[2])

            # find the angle between the y-component of the vector and the direction of the camera
            try:
                yAngle = math.degrees(math.acos(dotProduct(self.cameraVector, yVector) / (math.dist(self.cameraVector, [0, 0, 0]) * math.dist(yVector, [0, 0, 0]))))
            except:
                yAngle = 90
            if vector[0] * self.xPlane[0] + vector[1] * self.xPlane[1] + vector[2] * self.xPlane[2] < 0:
                yAngle *= -1

            # convert the ratio between the angles into a definite y-position
            ypos = (self.height * yAngle) / (
                        (self.fov * self.height) / max([self.width, self.height])) + self.height / 2

            # return the screen position of the vertice
            return xpos, ypos
    def project(self, objects):
        for ob in objects:
            if isinstance(ob, Mesh):
                verts = [] # lists all vertices
                vertDist = [] # lists distance from camera of each vertice in relation to the above list (for use when ordering)
                for vert in ob.vertices:
                    screenPos = self.projectPoint([vert.x, vert.y, vert.z])
                    vert.screenPos = [int(screenPos[0]), int(screenPos[1])]
                    verts.append(vert)
                    vertDist.append(dist(vert.get_pos(), self.position))
                for face in ob.faces:
                    face.calculateCenter()
                    face.calculateNormals()

                #order the faces in order of furthest to the camera to closest to the camera
                #this is in order to make sure faces closer to the camera are drawn in front of faces further away
                remainingVerts = verts.copy()
                remainingVertDists = vertDist.copy()
                tris = []
                while len(remainingVerts) > 0:
                    #print(f"""remaining verts = {remainingVerts}""")
                    closestVert = remainingVerts[remainingVertDists.index(max(remainingVertDists))]
                    connectedTris = ob.trisFrom(closestVert)
                    connectedTrisDists = []
                    for tri in connectedTris.copy():
                        if tri in tris:
                            #print('--')
                            #print(tri)
                            #print(connectedTris)
                            connectedTris.remove(tri)
                            #print(connectedTris)
                            #print('--')
                        else:
                            #print("yuh")
                            connectedTrisDists.append([vertDist[verts.index(tri.vertices[i])] for i in range(0, 3) if tri.vertices[i] != closestVert])
                    #print(f"""connected tris = {connectedTris}""")
                    #print(f"""connected dist = {connectedTrisDists}""")
                    #print(f"""tris = {tris}""")
                    #print(connectedTrisDists)
                    while len(connectedTris) > 0:
                        maxDist = max(list(itertools.chain.from_iterable(connectedTrisDists)))
                        maxIndex = int(list(itertools.chain.from_iterable(connectedTrisDists)).index(maxDist) / 2)
                        maxTri = connectedTris[maxIndex]
                        tris.append(maxTri)
                        connectedTris.pop(maxIndex)
                        connectedTrisDists.pop(maxIndex)
                    remainingVerts.remove(closestVert)
                    remainingVertDists.remove(max(remainingVertDists))
                ob.tris = tris

    def display(self, objects):
        if self.displayType == "solid":
            self.solidDisplay(objects)
        elif self.displayType == "wireframe":
            self.wireframeDisplay(objects)
    def solidDisplay(self, objects):
        for ob in objects:
            if isinstance(ob, Mesh):
                for tri in ob.tris:
                    # displays a face
                    angle = math.degrees(math.acos(dotProduct(tri.normal, self.cameraVector) / (dist(tri.normal, [0, 0, 0]) * dist(self.cameraVector, [0, 0, 0]))))
                    angle = math.degrees(math.asin(math.sin(math.radians(angle))))
                    # the closer the angle between the normal and the direction of the camera is to 90 degrees, the darker the color
                    # the closer the angle between the normal and the direction of the camera is to 0 degrees, the lighter the color
                    color = [int(255 * ((90 - angle) / 90)), int(255 * ((90 - angle) / 90)),
                             int(255 * ((90 - angle) / 90))]
                    pg.draw.polygon(self.screen, color, [vert.screenPos for vert in tri.vertices], 0)
                    # selected objects have yellow edges
                    edgeColor = (255, 255, 255)
                    if ob.selected:
                        edgeColor = (255, 200, 0)
                    if ob.mode == "edit":
                        for vert in tri.vertices:
                            if vert in ob.selectedVertices:
                                pg.draw.circle(self.screen, (50, 50, 255), vert.screenPos, 2, 0)
                            elif vert not in ob.selectedVertices:
                                pg.draw.circle(self.screen, (255, 255, 255), vert.screenPos, 2, 0)
                    # edges should only be displayed if the object is selected or in edit mode
                    if ob.mode == "edit" or (ob.mode == "object" and ob.selected):
                        for edge in tri.edges:
                            pg.draw.line(self.screen, edgeColor, (edge.vert1.screenPos), (edge.vert2.screenPos), 1)

            pivotPoint = self.projectPoint(ob.position)
            pg.draw.circle(self.screen, (255, 200, 0), [int(pivotPoint[0]), int(pivotPoint[1])], 2, 0)
    def wireframeDisplay(self, objects):
        for ob in objects:
            if isinstance(ob, Mesh):
                for edge in ob.edges:
                    pg.draw.line(self.screen, (255, 255, 255), edge.vert1.screenPos, edge.vert2.screenPos, 1)
                for vert in ob.vertices:
                    pg.draw.circle(self.screen, (255, 255, 255), vert.screenPos, 2, 0)
            pivotPoint = self.projectPoint(ob.position)
            pg.draw.circle(self.screen, (255, 200, 0), [int(pivotPoint[0]), int(pivotPoint[1])], 2, 0)

    def selectObject(self, objects, mousePos):
        for ob in objects:
            if isinstance(ob, Mesh):
                for tri in ob.tris:
                    cursorInTri = True
                    for index in [0, 1, 2]:
                        #vector connecting one of the verts to the selected vert
                        vertVector1 = [tri.vertices[index - 1].screenPos[0] - tri.vertices[index].screenPos[0],
                                       tri.vertices[index - 1].screenPos[1] - tri.vertices[index].screenPos[1]]
                        #vector connecting the other vert to the selected vert
                        vertVector2 = [tri.vertices[index - 2].screenPos[0] - tri.vertices[index].screenPos[0],
                                       tri.vertices[index - 2].screenPos[1] - tri.vertices[index].screenPos[1]]

                        if factorVector(vertVector1) != factorVector(vertVector2) and dist(vertVector1, [0, 0, 0]) * dist(vertVector2, [0, 0, 0]) != 0:
                            print(tri.vertices[0].get_pos(), tri.vertices[0].screenPos)
                            print(tri.vertices[1].get_pos(), tri.vertices[1].screenPos)
                            print(tri.vertices[2].get_pos(), tri.vertices[2].screenPos)
                            print(vertVector2, vertVector1)
                            #find the angle between the vectors
                            vertAngle = math.degrees(math.acos(dotProduct(vertVector1, vertVector2) / (dist(vertVector1, [0, 0, 0]) * dist(vertVector2, [0, 0, 0]))))

                            #vector connecting the cursor position to the selected vert
                            mouseVector = [mousePos[0] - tri.vertices[index].screenPos[0],
                                           mousePos[1] - tri.vertices[index].screenPos[1]]

                            if factorVector(mouseVector) != factorVector(vertVector1) and dist(vertVector1, [0, 0, 0]) * dist(mouseVector, [0, 0, 0]) != 0:
                                print(mouseVector)
                                #find the angle between the mouse and one of the vertice vectors
                                mouseAngle = math.degrees(math.acos(dotProduct(vertVector1, mouseVector) / (dist(vertVector1, [0, 0, 0]) * dist(mouseVector, [0, 0, 0]))))

                                #if the angle between the mouse and the selected vertice is greater than the vertices its connected to, it will not be inside the face
                                if mouseAngle > vertAngle:
                                     cursorInTri = False
                                     break
                            else:
                                cursorInTri = False
                                break
                        else:
                            cursorInTri = False
                            break
                    if cursorInTri:
                        return ob

def createSphere(segments, rings):
    vertices = []
    edges = []
    faces = []
    for ring in range(0, rings + 1):
        z = 2 / rings * (ring - rings/2)
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