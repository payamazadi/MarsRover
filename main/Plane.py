class Plane(object):
    _grid = None
    
    def __init__(self):
        pass

    def validate_point(self, point):
        raise NotImplementedError("Abstract method: subclass must define")
    
    def outside_bounds_dangerous(self):
        raise NotImplementedError("Abstract method: subclass must define")
    
    def get_point_entry(self, point):
        raise NotImplementedError("Abstract method: subclass must define")
    
    def can_add_entry_at_point(self, point, entry):
        raise NotImplementedError("Abstract method: subclass must define")
    
    def put_point_entry(self, point, entry):
        raise NotImplementedError("Abstract method: subclass must define")
    
class Plane2d(Plane):
    _grid = None
    _xsize = _ysize = 0
    
    def __init__(self, xsize, ysize):
        self._xsize, self._ysize = xsize+1, ysize+1
        self._grid = {Point2d(x,y):None for x in range(self._xsize) for y in range(self._ysize)}
    
    #Just for fun this is set to false. Naturally anything outside of this plane, which would be some other plane, could not be assumed to be safe..
    def outside_bounds_dangerous(self):
        return False
    
    def __within_bounds(self, point):
        x,y = point._x, point._y;
        return x >= 0 and y >= 0 and y < self._ysize and x < self._xsize
        
    def validate_point(self, point):
        if (isinstance(point, Point2d) and 
        self.__within_bounds(point)):
            return True
        return False
    
    def get_point_entry(self, point):
        if self.validate_point(point):
            return self._grid[point]
        return False
    
    #we can wrap additional error checking mechanisms here. there really should be a good exception raising system here, which gets propagated through movements methods to caller
    def can_add_entry_at_point(self, point, entry):
        if self.validate_point(point) and (isinstance(self._grid[point], type(None))):
            return True
        return False
        
    def put_point_entry(self, destination, entry):
        if self.can_add_entry_at_point(destination, entry):
            self._grid[destination] = entry
            return True
        return False
    
    def move_entry_by_one(self, destination, entry):
        if self.can_add_entry_at_point(destination, entry) and destination.distance(entry._orientation._point) <= 1:
            self._grid[entry._orientation._point] = None
            self._grid[destination] = entry
            return True
        return False
                
        

class Plateau(Plane2d):    
    def __init__(self, xsize, ysize):
        super().__init__(xsize, ysize)
         
    def outside_bounds_dangerous(self):
        return True
    
class Point(object):
    _points = ()
     
    def __init__(self, *points):
        self._points = points
         
    def get_point(self):
        return self._points
     
    def set_point(self, new_coordinates):
        self._points = new_coordinates
         
    def __eq__(self,other):
        return self._points == other._points
         
    def __ne__(self,other):
        return not self == other
         
    def __hash__(self):
        return hash(self._points)
    
    def distance(self, other):
        raise NotImplementedError("Abstract method: different distance formulas for different dimensions. Please implement.")
    
class Point2d(Point):
    _x =_y = 0
     
    def __init__(self, x=0, y=0):
        self._x, self._y = x,y
        super().__init__(x, y) 
        
    #in this case use Manhattan distance (so that diagonals can't be used, since we can't turn diagonally)
    #if we could move points diagonally, we'd use Cartesian distance
    def distance(self, other):
        if isinstance(other, Point2d):
            return abs(self._x - other._x) + abs(self._y - other._y)
        raise NotImplementedError("You are trying to compare a 2d point to a non-2d point. Please define that comparison..")

class Direction2d(object):
    NORTH, EAST, SOUTH, WEST = 0, 90, 180, 270
    direction_map = {"N":NORTH, "S":SOUTH, "E":EAST, "W":WEST}
     
    #Maybe overkill? Makes rest of code much easier to write anyway.
    TURN_LEFT, TURN_RIGHT = -90, 90;
    turn_map = {"L":TURN_LEFT, "R":TURN_RIGHT}
     
    '''Instance attributes'''
    _direction = NORTH
     
    def __init__(self, direction = NORTH):
        self._direction = direction
     
    def rotate(self, turn):
        self._direction = (self._direction + turn) % 360
           
    def __eq__(self, other):
        return self._direction == other._direction
     
    def __ne__(self, other):
        return not self == other
    
    class Direction3dOrSomething(object):
        def __init__(self):
            #stub. this is just proof of concept. purposefully unused.
            pass  

class Orientation2d(object):
    coord_shift_map = {Direction2d.NORTH:(0,1), Direction2d.SOUTH:(0,-1), Direction2d.EAST:(1,0), Direction2d.WEST:(-1,0)}
    
    _point = None
    _direction = None
    
    def __init__(self, point, direction):
        self._point, self._direction = point, direction
        
    def get_moved_orientation(self):
        addx, addy = self.coord_shift_map[self._direction._direction]
        new_point = Point2d(self._point._x + addx, self._point._y + addy)
        
        return Orientation2d(new_point, self._direction)
    
    def __eq__(self, other):
        if(isinstance(other, Point2d)):
            return self._point == other
        elif isinstance(other, Direction2d):
            return self._direction == other
        elif isinstance(other, Orientation2d):
            return self._direction == other._direction and self._point == other._point
        else: return False
    
    def __ne__(self, other):
        return not self == other
    
    def __str__(self):
        return "Orientation2d: (" + repr(self._point._x) + "," + repr(self._point._y) + ") facing: " + next((directionstring for directionstring, direction in Direction2d.direction_map.items() if direction == self._direction._direction), None)
    
    def __repr__(self):
        return repr(self._point._x) + " " + repr(self._point._y) + " " + next((directionstring for directionstring, direction in Direction2d.direction_map.items() if direction == self._direction._direction), None)
