from Vectors3D import *
from Vectors3D.mesh import Mesh
from Vectors3D.object import Object
import pygame as pg
import math
import itertools

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
    def set_rot(self, rotation):
        if rotation[0] != 0:
            self.xPlane[1] = dist([self.xPlane[1], self.xPlane[2]], [0, 0]) * math.cos(math.radians(rotation[0]))
            self.xPlane[2] += dist([self.xPlane[1], self.xPlane[2]], [0, 0]) * math.sin(math.radians(rotation[0]))
            self.yPlane[1] += dist([self.yPlane[1], self.yPlane[2]], [0, 0]) * math.cos(math.radians(rotation[0]))
            self.yPlane[2] = dist([self.yPlane[1], self.yPlane[2]], [0, 0]) * math.sin(math.radians(rotation[0]))
            self.rotation[0] = rotation[0]
        if rotation[1] != 0:
            self.xPlane[0] = dist([self.xPlane[0], self.xPlane[2]], [0, 0]) * math.cos(math.radians(rotation[1]))
            self.xPlane[2] += dist([self.xPlane[0], self.xPlane[2]], [0, 0]) * math.sin(math.radians(rotation[1]))
            self.yPlane[0] = dist([self.yPlane[0], self.yPlane[2]], [0, 0]) * math.cos(math.radians(rotation[1]))
            self.yPlane[2] = dist([self.yPlane[0], self.yPlane[2]], [0, 0]) * math.sin(math.radians(rotation[1]))
            self.rotation[1] = rotation[1]
        if rotation[2] != 0:
            self.xPlane[0] = dist([self.xPlane[0], self.xPlane[1]], [0, 0]) * math.cos(math.radians(rotation[2]))
            self.xPlane[1] = dist([self.xPlane[0], self.xPlane[1]], [0, 0]) * math.sin(math.radians(rotation[2]))
            self.yPlane[0] = dist([self.yPlane[0], self.yPlane[1]], [0, 0]) * math.cos(math.radians(rotation[2]))
            self.yPlane[1] += dist([self.yPlane[0], self.yPlane[1]], [0, 0]) * math.sin(math.radians(rotation[2]))
            self.rotation[2] = rotation[2]
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
        displayedEdges = []
        displayedVerts = []
        allTris = []
        allVerts = []
        vertDist = []

        obFrom = {}

        for ob in objects:
            if isinstance(ob, Mesh):
                allTris += ob.tris
                for tri in ob.tris:
                    obFrom[tri] = ob
                allVerts += ob.vertices
                vertDist.append(dist(allVerts[-1].get_pos(), [0, 0, 0]))

        dists = [dist(tri.center, self.position) for tri in allTris]
        newTris = []
        while len(allTris) > 0:
            index = dists.index(max(dists))
            selectedTri = allTris[index]
            newTris.append(selectedTri)
            allTris.pop(index)
            dists.pop(index)
        allTris = newTris

        """
        # order the faces in order of furthest to the camera to closest to the camera
        # this is in order to make sure faces closer to the camera are drawn in front of faces further away
        remainingVerts = allTris.copy()
        remainingVertDists = vertDist.copy()
        tris = []
        while len(remainingVerts) > 0:
            # print(f\"""remaining verts = {remainingVerts}\""")
            closestVert = remainingVerts[remainingVertDists.index(max(remainingVertDists))]
            connectedTris = ob.trisFrom(closestVert)
            connectedTrisDists = []
            for tri in connectedTris.copy():
                if tri in tris:
                    # print('--')
                    # print(tri)
                    # print(connectedTris)
                    connectedTris.remove(tri)
                    # print(connectedTris)
                    # print('--')
                else:
                    # print("yuh")
                    connectedTrisDists.append([vertDist[verts.index(tri.vertices[i])] for i in range(0, 3) if
                                               tri.vertices[i] != closestVert])
            # print(f\"""connected tris = {connectedTris}\""")
            # print(f\"""connected dist = {connectedTrisDists}\""")
            # print(f\"""tris = {tris}\""")
            # print(connectedTrisDists)
            while len(connectedTris) > 0:
                maxDist = max(list(itertools.chain.from_iterable(connectedTrisDists)))
                maxIndex = int(list(itertools.chain.from_iterable(connectedTrisDists)).index(maxDist) / 2)
                maxTri = connectedTris[maxIndex]
                tris.append(maxTri)
                connectedTris.pop(maxIndex)
                connectedTrisDists.pop(maxIndex)
            remainingVerts.remove(closestVert)
            remainingVertDists.remove(max(remainingVertDists))
        """

        #for ob in objects:
        #    if isinstance(ob, Mesh):
                #for tri in ob.tris:
        for tri in allTris:
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
            if obFrom[tri].selected:
                edgeColor = (255, 200, 0)
            if obFrom[tri].mode == "edit":
                for vert in tri.vertices:
                    if vert not in displayedVerts:
                        if vert in obFrom[tri].selectedVertices:
                            pg.draw.circle(self.screen, (50, 50, 255), vert.screenPos, 2, 0)
                        elif vert not in obFrom[tri].selectedVertices:
                            pg.draw.circle(self.screen, (255, 255, 255), vert.screenPos, 2, 0)
                        displayedVerts.append(vert)
            # edges should only be displayed if the object is selected or in edit mode
            if obFrom[tri].mode == "edit" or (obFrom[tri].mode == "object" and obFrom[tri].selected):
                for edge in tri.edges:
                    if edge not in displayedEdges:
                        pg.draw.line(self.screen, edgeColor, (edge.vert1.screenPos), (edge.vert2.screenPos), 1)
                        displayedEdges.append(edge)

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
    def selectSingle(self, object, mousePos, vertices = True, edges = False, faces = False):
        for vert in object.vertices:
            distance = dist(vert.screenPos, mousePos)
            if distance <= 5:
                return vert
    def selectCircle(self, object, mousePos, radius, vertices = True, edges = False, faces = False):
        selectedVerts = []
        for vert in object.vertices:
            distance = dist(vert.screenPos, mousePos)
            if distance <= radius:
                selectedVerts.append(vert)
        return selectedVerts