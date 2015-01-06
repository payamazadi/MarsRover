'''
Created on Aug 31, 2013

@author: azadi
'''
import unittest

from main.Plane import Direction2d
from main.Plane import Orientation2d
from main.Plane import Point2d
from main.Plane import Plateau

from main.Entities import Rover
from main.Entities import FallOffException
from main.Entities import EntityPlaceFailureException

class Test(unittest.TestCase):

    def test_Direction(self):
        dnorth = Direction2d(Direction2d.NORTH)
        deast = Direction2d(Direction2d.EAST)
        deast2 = Direction2d(Direction2d.EAST)
        dwest = Direction2d(Direction2d.WEST)
        dsouth = Direction2d(Direction2d.SOUTH)
        dnorth2 = Direction2d(Direction2d.NORTH)
        assert(dnorth == dnorth2)
        
        dnorth.rotate(Direction2d.turn_map['L'])
        assert(dnorth == dwest)
        
        deast.rotate(Direction2d.turn_map['L'])
        assert(deast == dnorth2)
        
        dwest.rotate(Direction2d.turn_map['L'])
        assert(dwest == dsouth)
        
        dsouth.rotate(Direction2d.turn_map['L'])
        assert(dsouth == deast2)
        
    def test_Orientation(self):
        dnorth = Direction2d(Direction2d.NORTH)
        dnorth2 = Direction2d(Direction2d.NORTH)
        dsouth = Direction2d(Direction2d.SOUTH)
         
        p1 = Point2d(1,4)
        p2 = Point2d(1,4)
        p3 = Point2d(4,1)
         
        o1 = Orientation2d(p1, dnorth)
        o2 = Orientation2d(p2, dnorth2)
        o3 = Orientation2d(p3, dsouth)
         
        assert(o1 == o2)
        assert(o1 != o3)
        
        assert(o1 == p1)
        assert(o1 == dnorth)
     
    def test_Entities(self):
        r1 = Rover("r1")
        r2 = Rover("r2", Orientation2d(Point2d(1,4), Direction2d(Direction2d.SOUTH)))
         
        assert(r1.what_am_i() == "r1:Rover")
         
        r2.rotate(Direction2d.turn_map['L'])
        assert(r2._orientation._direction == Direction2d(Direction2d.EAST))
    
        
    def test_Plateaus(self):
        p1 = Plateau(5,5)
        invalidpoint = Point2d(-1, 4)
        validpoint = Point2d(1,1)
        r1 = Rover("r1", Orientation2d(Point2d(1,4), Direction2d(Direction2d.SOUTH)))
        r2 = Rover("r2", Orientation2d(Point2d(1,4), Direction2d(Direction2d.NORTH)))
        r3 = Rover("r3", Orientation2d(Point2d(4,1), Direction2d(Direction2d.NORTH)))
        
        assert(p1.outside_bounds_dangerous())
        assert(p1.validate_point(invalidpoint) == False)
        assert(p1.validate_point(Point2d(1,4)) == True)
        assert(p1.validate_point(Point2d(6,0)) == False)
        assert(p1.validate_point(Point2d(4,4)) == True)
        assert(p1.validate_point(Point2d(5,5)) == True)
        assert(p1.validate_point(Point2d(6,0)) == False)
        assert(p1.validate_point(Point2d(0,6)) == False)
        
        assert(p1.validate_point(5) == False)
        
        assert(p1.get_point_entry(invalidpoint) == False)
        assert(p1.get_point_entry(validpoint) == None)
        
        assert(p1.put_point_entry(r1._orientation._point, r1))
        assert(p1.put_point_entry(r1._orientation._point, r1) == False)
        assert(p1.put_point_entry(r2._orientation._point, r2) == False)
        assert(p1.put_point_entry(r3._orientation._point, r3) == True)

    def xstr(self):
        if self is None:
            return ''
        else:
            return self
    
    def test_PlateauOrientation(self):
        p1 = Plateau(3,3)
        r1 = Rover("r1", Orientation2d(Point2d(0,0), Direction2d(Direction2d.SOUTH)), p1)
        self.assertRaises(FallOffException, r1.move)
        assert(repr(r1._orientation) == "0 0 S")
        r1.rotate(Direction2d.turn_map['R'])
        assert(repr(r1._orientation) == "0 0 W")
        self.assertRaises(FallOffException, r1.move)
        
    def test_RoversInPlateaus(self):
        p1 = Plateau(5,5)
        
        #1 2 N
        #LMLMLMLMM
        r1 = Rover("r1", Orientation2d(Point2d(1,2), Direction2d(Direction2d.NORTH)), p1)
        r2 = Rover("r2", Orientation2d(Point2d(3,3), Direction2d(Direction2d.EAST)), p1)
        
        r1.rotate(Direction2d.turn_map['L'])
        r1.move() 
        assert(p1.get_point_entry(Point2d(1,2)) == None)
        r1.rotate(Direction2d.turn_map['L'])
        r1.move()
        r1.rotate(Direction2d.turn_map['L'])
        r1.move()
        r1.rotate(Direction2d.turn_map['L'])
        r1.move()
        r1.move()
        assert(repr(r1._orientation) == "1 3 N")
        
        #3 3 E
        #MMRMMRMRRM  
        
        r2.move()
        r2.move()
        r2.rotate(Direction2d.turn_map['R'])
        r2.move()
        r2.move()
        r2.rotate(Direction2d.turn_map['R'])
        r2.move()
        r2.rotate(Direction2d.turn_map['R'])
        r2.rotate(Direction2d.turn_map['R'])
        r2.move()
        assert(repr(r2._orientation) == "5 1 E")
        
        #Check that the plateau actually represents where the rovers are
        assert(p1.get_point_entry(Point2d(1,3)) == r1)
        assert(p1.get_point_entry(Point2d(5,1)) == r2)
        
        
        #R2: M
        self.assertRaises(FallOffException, r2.move)
        
        #R2: LLMMMMRMM
        r2.rotate(Direction2d.turn_map['L'])
        r2.rotate(Direction2d.turn_map['L'])
        r2.move()
        r2.move()
        r2.move()
        r2.move()
        r2.rotate(Direction2d.turn_map['R'])
        r2.move()
        self.assertRaises(EntityPlaceFailureException, r2.move)
    
    
if __name__ == "__main__":
    unittest.main()