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