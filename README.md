MarsRover
=========
MarsRover is one of three problems we (at DealerOn) send candidates, from which they pick and solve one. Genreally three days is alotted for completion. The test is adapted from the code test used at ThoughtWorks.

Problem prompt
=========
A squad of robotic rovers are to be landed by NASA on a plateau on Mars. This plateau, which is 
curiously rectangular, must be navigated by the rovers so that their on board cameras can get a 
complete view of the surrounding terrain to send back to Earth. 

A rover's position and location is represented by a combination of x and y co-ordinates and a letter 
representing one of the four cardinal compass points. The plateau is divided up into a grid to simplify 
navigation. An example position might be 0, 0, N, which means the rover is in the bottom left corner and 
facing North. 

In order to control a rover, NASA sends a simple string of letters. The possible letters are 'L', 'R' and 'M'. 
'L' and 'R' makes the rover spin 90 degrees left or right respectively, without moving from its current 
spot. 'M' means move forward one grid point, and maintain the same heading. 
Assume that the square directly North from (x, y) is (x, y+1). 

The first line of input is the upper-right coordinates of the plateau, the lower-left coordinates are 
assumed to be 0,0. 

The rest of the input is information pertaining to the rovers that have been deployed. Each rover has 
two lines of input. The first line gives the rover's position, and the second line is a series of instructions 
telling the rover how to explore the plateau. 

The position is made up of two integers and a letter separated by spaces, corresponding to the x and y 
co-ordinates and the rover's orientation. 

Each rover will be finished sequentially, which means that the second rover won't start to move until the 
first one has finished moving. 

The output for each rover should be its final co-ordinates and heading. 

Example Input and Output:

Input:
  * 5 5
  * 1 2 N
  * LMLMLMLMM
  * 3 3 E
  * MMRMMRMRRM

Output:
  * 1 3 N
  * 5 1 E

Proposed rubric
=========
Solutions are required to be in VB.NET/C#. The rubric used to evaluate code tests is not very stringent, and is as follows:

  * Fail / Do Not Evaluate:
      - Code does not compile unless due to reasonable / foreseeable configuration issue on the reviewer's machine
      - Code does not solve the problem accurately using the inputs and outputs supplied in the problem instructions
      - Code is sloppily formatted making it extremely difficult to read
  * Below Average:
      - Code is written in one or two monolithic methods
      - Variable names are cryptic or unnecessarily short 
  * Average:
      - Coarse breakdown of functionality into multiple objects
      - Various edge cases accounted for that go above and beyond the input provided in the problem instructions
      - Code is well formatted and easy to follow 
  * Above Average:
      - No compiler warnings
      - Code represents a good object oriented design (loose coupling / high cohesion)
      - Unit tests or script used as input to the program 
  * Exceptional:
      - Code satisfies the inputs and outputs supplied in the problem instructions
      - Unit tests with positive and negative cases resulting in over 90% coverage are supplied
      - Code has a build and packaging script included with it
      
When I review the code tests, I additionally look for the following:
  - Does every class/interface have a purpose and is it used? Or is it superfluous to try and show some knowledge of OO?
  - Is there a novel implementation of the core algorithm, or just brute force?
  - Every spec has details missing or in conflict - does the code or documentation address any of it?

Solution
=========
This is a canonical solution written in Python and attempts to set the bar for 'exceptional', which includes the factors outside of the rubric that I consider.
 
Design goals of this solution:
  - Novel solution to turning/moving: use +/-90 degree turns mod 360, instead of checking current direction and deciding which way is left and which way is right
 - Address the unstated problem of two rovers colliding, without overengineering
 - Address the unstated problem of control and placement - 'who' controls each rover, where does it live, and what structure provides a 'map' of the area?
 - Leave some breadcrumbs and skeleton structure for extending the code without overengineering: 
  - Allowing space and direction to be implemented in 3d
  - Mapping entities other than Rovers
  - Mapping entities that can move and those that can't, describing a physical structure other than a rectangular plateau
