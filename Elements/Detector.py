import numpy as np
from Elements import Muon as mu
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
        string = self.name + " —>[Rad: " + str(self.radius) + "m , Ht: " + str(self.height) + "m , Thk: "\
         + str(self.wallThickness) + "cm ] Pos:" + str(self.position) +"\n"
        return string

    '''def testIntersection(self, muon):
        Returns entry and exit points of a muon passing through the detector.
            [x1,y1,z1,x2,y2,z2]
            If the muon does not intersect, returns None
       

        #First check if the argument is a muon:
        if not isinstance(muon, mu.Muon):
            print("Non-Muon argument; returning None.")
            return None

        #Calculate how many checks are necessary: 1 every cm
        track = muon.getTrack()
        maxX = abs(track[0]) + self.radius + abs(self.position[0]) #these position values will probably be zero
        maxY = abs(track[2]) + self.radius + abs(self.position[1])
        maxZ = abs(track[4])
        iterator = int(100*np.sqrt(maxX**2 + maxY**2 + maxZ**2))
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
            elif intersectionQueue == [True, False]:
                #we found the exit point
                exit = muPos
                return np.append(entry,exit)
            elif i == iterator - 1:
                return None


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
            muPos += muDir*0.02 # 2cm at a time?'''

    def testIntersection(self, muon):
    #test intersection using the lines

        if not isinstance(muon, mu.Muon):
            print("Non-Muon argument; returning None.")
            return None
           
        hit1 = 0
        hit2 = 0
        hit3 = 0
        lines = muon.lines()
        track = muon.getTrack()
        ###plane1 (x-z)
        zB = [-6.65, 6.65]
        yB = [-6.172, 6.172]
        xB = [-6.172, 6.172]
        coord = []
        for z in zB:
            x = (z - lines[1])/lines[0]
            if x < 6.172 and x > -6.172:
                hit1 = 1
                y = (z - lines[5])/lines[4]
                if y < 6.172 and y > -6.172:
                    coord.append([x, y, z])
                

        for x in xB:
            z = lines[0]*x + lines[1]
            if z < 6.65 and z > -6.65:
                hit1 = 2
                y = (z - lines[5])/lines[4]
                if y < 6.172 and y > -6.172:
                    coord.append([x, y, z])
                
        ###plane2 (x-y) ### circle plane
        reci = 1/lines[2]
        x = - lines[3]/(reci - lines[2])
        y = reci*x
        dist = np.sqrt(x*x +y*y)
        if dist < 6.172:
            hit2 = 1
            
            

        ### plane3 (y-z)
        for z in zB:
            y = (z - lines[5])/lines[4]
            if y < 6.172 and y > -6.172:
                hit3 = 1
                x = (z - lines[1])/lines[0]
                if x < 6.172 and x > -6.172:
                    coord.append([x, y, z])

        for y in yB:
            z = lines[4]*y + lines[5]
            if z < 6.65 and z > -6.65:
                hit3 = 2
                x = (z - lines[1])/lines[0]
                if x < 6.172 and x > -6.172:
                    coord.append([x, y, z])
                
        if hit1 > 0 and hit2 == 1 and hit3 > 0:
            #print('hit')
            duplicate = []
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
            
             
            
            
                
                
            
            
        