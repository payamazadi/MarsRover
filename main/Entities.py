#Define 2 entities as being equal if their IDs are the same.

class Entity(object):
    '''
    classdocs
    '''
    _id = ""
    _orientation = None 
    _plane = None
    
    def __init__(self, identifier):
        self._id = identifier

    def what_am_i(self):
        raise NotImplementedError("Poor man's (Python's) abstract class: please implement this what_am_i method from Entity!")
    
    def place_self(self):
        if self._plane != None:
            success = self._plane.put_point_entry(self._orientation._point, self)
            if not success:
                raise EntityPlaceFailureException
    
    def __key_tuple(self):
        return (self._id,)
    
    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.__key_tuple() == other.__key_tuple()
        return False
    
    def __hash__(self):
        return hash(self.__key_tuple())
'''In a more complicated setup we could have Moveable and Non-moveable entities
and moveable ones would have to implement validate_move and move() methods so that 
human controller error doesn't accidentally move the entity off a cliff or into
an active volcano.'''

       
class Rover(Entity):
    def __init__(self, identifier, orientation = None, plane = None):
        self._id, self._orientation, self._plane = identifier, orientation, plane
        self.place_self()
        
    def what_am_i(self):
        return self._id + ":Rover"
    
    def rotate(self, direction):
        self._orientation._direction.rotate(direction)
        
    def move(self):
        new_orientation = self._orientation.get_moved_orientation()
        '''The Rover should define how it moves through which spaces. In 
        the case of a bounded plateau (how'd it get here in the first place), 
        it probably shouldn't fall off the edge due to bad user input. 
        Additionally This logic would be different if the Rover could move 
        between planes/spaces (e.g. plateau to another mountain; plateau to 
        crater etc). The object model would be a bit different as the Rover 
        would need a more vast notion of the planet and how different planes are 
        adjacent. There are multiple ways this can be done depending on what the
        most important intended goal is. A rover's plane could have a parent world,
        or a rover gets a world mapping global coordinates to planes/etc, or we make
        Plane2d (or a Plane3d) the whole world and give it a wrap-around 
        movement and generate polygonal/rectangular boundary zones with special
        properties.. these get into major design questions/decisions that are
        far outside the scope of this project, but the model is left flexible
        enough to be able to accommodate those needs without too much recoding.
        '''
        if(self.validate_move(new_orientation)):
            success = self._plane.move_entry_by_one(new_orientation._point, self)
            if success:
                self._orientation = new_orientation
                return True
            else:
                return False
        else:
            #this should just return exceptions returned by the plane classes
            if self._plane.outside_bounds_dangerous() and self._plane.validate_point(new_orientation._point) == False:
                raise FallOffException("If I, " + self.what_am_i() + \
                ", were to move, I would fall off the face of this space. Not moving.")
            else:
                raise EntityPlaceFailureException("Another Rover already occupies this space!")                
    
    #here we could have additional rules. maybe the rover can't move to certain
    #kinds of terrain/points or something.
    def validate_move(self, orientation):
        if self._plane.can_add_entry_at_point(orientation._point, self):
            return True
        return False
        
class FallOffException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class EntityPlaceFailureException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)