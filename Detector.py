import numpy as np
from MuonGeneration2 import Muon as mu
from scipy import constants as cst


class Detector(object):
    '''A rudimentary class for a cylindrical detector'''

    def __init__(self, radius, height, name, position = np.array([0.,0.,0.])):
        '''Constructor for cylindrical detector
        Arguments:
            radius (meters)
            height (meters)
            position (meters) position of CENTER of detector
            '''

        self.radius = radius
        self.height = height
        self.position = position

        self.fill = "Water"
        self.slantDepth = 6.011 #km w.e.
        self.wallThickness = 2.54 #cm
        self.name = name

    def isInside(self, point):
        '''Returns a boolean indicating whether or not a point in 3-space
            is inside the detector. (Assumes Cartesian coords)
            Argument : point (array-type object of size 3)
        '''

        detX = self.position[0]
        detY = self.position[1]
        detZ = self.position[2]

        x = point[0]
        y = point[1]
        z = point[2]

        if x > detX + self.radius or x < detX - self.radius:
            return False
        elif y > detY + self.radius or y < detY - self.radius:
            return False
        elif z > detZ + self.height or z < detZ:
            return False
        else:
            return True

    def __str__(self):
        '''Renders relevant Detector details into a string'''
        string = self.name + " —>[Rad: " + str(self.radius) + "mm , Ht: " + str(self.height) + "mm , Thk: "\
         + str(self.wallThickness) + "cm ] Pos:" + str(self.position) +"\n"
        return string

    '''def testIntersection(self, muon):
        #Returns entry and exit points of a muon passing through the detector.
        #[x1,y1,z1,x2,y2,z2]
        #If the muon does not intersect, returns None
       
        #First check if the argument is a muon:
        if not isinstance(muon, mu.Muon):
            print("Non-Muon argument; returning None.")
            return None
        #Calculate how many checks are necessary: 1 every cm
        track = muon.getTrack()
        maxX = abs(track[0]) + self.radius + abs(self.position[0]) #these position values will probably be zero
        maxY = abs(track[2]) + self.radius + abs(self.position[1])
        maxZ = abs(track[4])
        iterator =  100 #int(1*np.sqrt(maxX**2 + maxY**2 + maxZ**2))
        #something like the highest possible number of centimeters
        muPos = np.array([track[0], track[2], track[4]]) #see convention, x,y,z (muon.py)
        muDir = np.array([track[1], track[3], track[5]])
        #instantiate list for entry/exit testing
        intersectionQueue = [False, False]
        entry = np.empty(3)
        exit = np.empty(3)
        for i in range(iterator):
            if intersectionQueue == [False, True]:
                #we found the entry point
                entry = muPos
                print(entry)
            elif intersectionQueue == [True, False]:
                #we found the exit point
                exit = muPos
                print(exit)
                return np.append(entry,exit)
            elif i == iterator - 1:
                return None
            print(intersectionQueue)
            #Move point over
            intersectionQueue[0] = intersectionQueue[1]
            #check if the point is inside
            if self.isInside(muPos):
                intersectionQueue[1] = True
            else:
                intersectionQueue[1] = False
                if i > iterator/2:
                    return None
            #calculate the point of the muon, move it ahead a bit (maintain direction)
            muPos += muDir*1.02 # 2cm at a time?'''

    def testIntersection(self, muon):
    #test intersection using the lines

        if not isinstance(muon, mu.Muon):
            print("Non-Muon argument; returning None.")
            return None
           
        #initializing values for whether a hit is there or not, and getting valies for muontrack and slopes/intercept
        hit1 = 0
        hit2 = 0
        hit3 = 0
        lines = muon.lines()
        track = muon.getTrack()
        
        #Inputting extremity values and initializing a list for the coordinates to go into
        zB = [-self.height/2, self.height/2]
        yB = [-self.radius, self.radius]
        xB = [-self.radius, self.radius]
        Height = self.height/2
        coord = []
        
        ###plane1 (x-z)
        for z in zB:
        #checking both Z extremities
            x = (z - lines[1])/lines[0]
            #finding x value using the x-z slope and intercept
            
            if x < self.radius and x > -self.radius:
            #checking if x value is within the bounds of the detector
                hit1 = 1
                #if yes, hit in this plane on top
                y = (z - lines[5])/lines[4]
                #find the y value for this set of x and z values
                
                if y < self.radius and y > -self.radius:
                #check if y value is within bounds of detector
                    coord.append([x, y, z])
                    #if yes, append coordinates since this is a good entry or exit point
                

        for x in xB:
        #checking both X extremities
            z = lines[0]*x + lines[1]
            #finding Z value using the x-z slope and intercept
            
            if z < Height and z > -Height:
            #checking if z value is within the bounds of the detector
                hit1 = 2
                #if yes, hit in this plane along sides
                y = (z - lines[5])/lines[4]
                #find the y value for this set of x and z values
                
                if y < self.radius and y > -self.radius:
                #check if y value is within bounds of detector
                    coord.append([x, y, z])
                    #if yes, append coordinates since this is a good entry or exit point
                
        ###plane2 (x-y) ### circle plane
        reci = 1/lines[2]
        #reciprocol slope to find perpendicular line through origin which will be closest point
        x = - lines[3]/(reci - lines[2])
        #find the x value of closest point where perpendicular line and ours intersect
        y = reci*x
        #find the y value of this point
        dist = np.sqrt(x*x +y*y)
        #find the distance of this point from the origin
        
        if dist < self.radius:
        #if the distance is less than the radius of the circle, it must enter the circle
            hit2 = 1
            #hit in this plane
            
            

        ### plane3 (y-z)
        for z in zB:
        #checking both Z extremities
            y = (z - lines[5])/lines[4]
            #finding Y value using the y-z slope and intercept
            
            if y < self.radius and y > -self.radius:
            #checking if y value is within the bounds of the detector
                hit3 = 1
                #if yes, hit on the top of the detector
                x = (z - lines[1])/lines[0]
                if x < self.radius and x > -self.radius:
                    coord.append([x, y, z])

        for y in yB:
            z = lines[4]*y + lines[5]
            if z < Height and z > -Height:
                hit3 = 2
                x = (z - lines[1])/lines[0]
                if x < self.radius and x > -self.radius:
                    coord.append([x, y, z])
                
        if hit1 > 0 and hit2 == 1 and hit3 > 0:
            #print('hit')
            duplicate = []
            
            if not coord == []: 
                for i in coord:
                    if i not in duplicate:
                        duplicate.append(i)
                #print(lines)
                #print(track)
                if duplicate[0][2] < duplicate[1][2]:
                    duplicate = [duplicate[1],duplicate[0]]
                return duplicate
            
        else:
            return None 
            
             
            
            
                
                
            
            
        
