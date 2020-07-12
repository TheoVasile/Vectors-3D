#a point
class Vertice:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
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
        self.positon = position
        self.pivotPoint = position
        self.rotation = rotation
        self.scale = scale
    def get_pos(self):
        return self.positon
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
    def __init__(self, position, rotation, scale, fov):
        super().__init__(position, rotation, scale)
        self.fov = fov