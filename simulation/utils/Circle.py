'''
Representation of a circle and its attributes
'''
class Circle:
    def __init__(self, radius, startpos):
        self.r = radius
        self.cX = startpos[0]
        self.cY = startpos[1]

    def get_pos(self):
        return (self.cX, self.cY)