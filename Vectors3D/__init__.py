class Vertice:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
class Edge:
    def __init__(self, vert1, vert2):
        self.vert1 = vert1
        self.vert2 = vert2
class Face:
    def __init__(self, vertices):
        self.vertices = vertices

class Object:
    def __init__(self, position, rotation, scale):
        self.positon = position
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

class Mesh(Object):
    def __init__(self, position, rotation, scale, vertices, edges, faces):
        super().__init__(position, rotation, scale)
        self.vertices = vertices
        self.edges = edges
        self.faces = faces

class Camera(Object):
    def __init__(self, position, rotation, scale, fov):
        super().__init__(position, rotation, scale)
        self.fov = fov