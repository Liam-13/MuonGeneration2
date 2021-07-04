####################################################
#                    Muon Class                    #
#        Muon Class for Storing Attributes         #
#               And Distribution Data              #
####################################################


import numpy as np
import scipy.constants as cst

class Muon(object):
    '''The Muon class for our favourite particle to veto. Attenuated by the SNOLAB overburden.

    Attributes:
    **********

    charge   :    the elementary charge -> from CODATA
    mass     :    ordinary mass of muons -> from CODATA
    r        :    initial position in 3-space -> some kind of array [ x , y , z ]
    energy   :    due to attenuation in the overburden, muon energy is random, but not totally.
    dir      :    direction of Muon propagation
    mom      :    momentum in 3-space -> some kind of array

    '''

    #All muons have:

    mass = cst.value('muon mass') #From CODATA
    charge = cst.e #From CODATA

    #For random choices
    angleResolution = 1000
    thetas = np.linspace(0,np.pi*2,angleResolution) #Arbitrary resolution at 1000 different angles


    def __init__(self, initial_position, phi, energy = 1.0):
        '''Built to initialize a muon with a position, energy and direction
            dictated by the two angles of spherical coordinates
        '''

        #Basic assignment of initial position
        self.r = initial_position
        self.theta = np.random.random()*np.pi*2  #Radially symmetric
        self.energy = energy
        self.phi = phi

    #def getTrack(self):
        #'''Using the position, and angles, this returns a track for the propagating muons
        # as an array: [initial_X, initial_Y, initial_Z, zenith, azimuth]'''

        #angles = np.array([self.phi, self.theta])
        #position = self.r
        #track = np.append(position, angles)
        #return track

    def getTrack(self):
        '''Using the position, and angles, this returns a track as a unit vector
        in cartesian coordinates with the initial positions [x_0, x_component, y_0, y_component, z_0, z_component]
        '''
        angles = np.array([self.phi, self.theta])
        position = self.r

        x = np.array([position[0], np.sin(self.theta)*np.cos(self.phi)])
        y = np.array([position[1], np.sin(self.theta)*np.sin(self.phi)])
        z = np.array([position[2], -np.cos(self.phi)])
        y = np.append(y,z)
        track = np.append(x,y)
        return track
        
    def lines(self):
        '''Here I will try to use the unit vectors to make two line equations to represent the path and make a hopefully more efficient test.'''
        # plane 1 = x-z, plane2 = x-y, plane3 = y-z 
        #line is [slope1, intercept1, slope2, intercept2, slope3, intercept3]
        
        angles = np.array([self.phi, self.theta])
        position = self.r
        
        x = np.array(np.sin(self.theta)*np.cos(self.phi))
        y = np.array(np.sin(self.theta)*np.sin(self.phi))
        z = np.array(-np.cos(self.phi))
        
        slope1 = z/x
        Zint1 = position[2]-slope1*position[0]
        line = np.array([slope1, Zint1])
        
        slope2 = y/x 
        Yint2 = position[1]-slope1*position[0]
        line = np.append(line, [slope2, Yint2])
        
        slope3 = z/y
        Zint3 = position[2]-slope1*position[1]
        line = np.append(line, [slope3, Zint3])
        return line
        
        
    def __str__(self):
        string = "[Phi: " + str(self.phi) + " Theta: " + str(self.theta) +"] POS:" + str(self.r) +"\n"
        return string

### Generic Methods ###

def mass():
    '''Returns CODATA Muon Mass from Scipy Package'''
    return cst.value('muon mass')

def charge():
    '''Returns CODATA elementary charge from Scipy Package '''
    return cst.e
