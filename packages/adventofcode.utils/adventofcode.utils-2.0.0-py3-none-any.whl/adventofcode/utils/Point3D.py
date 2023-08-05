class Point3D:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    '''
    Returns the distance between two 3D points
    '''
    def distance(self, value):
        return abs(self.x - value.x) + abs(self.y - value.y) + abs(self.z - value.z)

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y and self.z == value.z

    def __hash__(self):
        return hash((self.x,self.y,self.z))

    def __repr__(self):
        return f'({self.x},{self.y},{self.z})'

    def __add__(self,value):
        return Point3D(self.x + value.x, self.y + value.y, self.z + value.z)