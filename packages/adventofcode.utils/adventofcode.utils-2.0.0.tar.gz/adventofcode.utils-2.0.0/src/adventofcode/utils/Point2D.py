class Point2D:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    '''
    Returns the distance between two 2D points
    So called Manhattan Distance
    '''
    def distance(self, value):
        return abs(self.x - value.x) + abs(self.y - value.y)

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

    def __hash__(self):
        return hash((self.x,self.y))

    def __repr__(self):
        return f'({self.x},{self.y})'