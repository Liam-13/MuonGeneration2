import numpy as np
import scipy as sp
import random
from scipy import constants as cst
from Elements import Muon as mu

class Generator(object):
    '''A class for a circular generator of muons located with the overburden of SNOLAB.
            The overburden comes into play with the muon's instantiated directions and energies.

    Attributes:
    **********

    radius   :    the radius of the generator disk (m)
    r        :    position in 3-space -> some kind of array [ x , y , z ] w.r.t the centre
    meiHime  :    the muon intensity w.r.t. the zenith angle, taken from the famous Mei and Hime paper

    '''

    def __init__(self, radius, position = np.array([0.,0.,10.])):
        self.radius = radius # meters
        self.position = position
        self.resolution = 1000

    def generateMuons(self, numberOfMuons):
        '''Generates a number of muons at random positions on the Disk
            with zenith angles according to the Mei Hime function and random phi angles

            Returns list of muons

            NOTE: Energy has not yet been worked out.
        '''
        muons = [] #np.empty(numberOfMuons)

        slantDepth = 6.011 #km w.e.
        I1 = 8.60e-6 # ± 0.53e-6 /sec/cm^2/sr
        I2 = 0.44e-6 # ± 0.06e-6 /sec/cm^2/sr
        lam1 = 0.45 # ± 0.01 km.w.e.
        lam2 = 0.87 # ± 0.02 km.w.e.

        #Zenith angle range
        phiRad = np.linspace(0, np.pi/2, self.resolution)

        #Muon Angular distribution intensity
        meiHime = (I1*np.exp(-slantDepth/(lam1*np.cos(phiRad)))+I2*np.exp(-slantDepth/(lam2*np.cos(phiRad))))/np.cos(phiRad)

        meiHime = meiHime / np.sqrt(meiHime.sum()**2) #Normalizes the mei hime distribution function



        for i in range(numberOfMuons):

            #random radius
            rho = random.random()*self.radius

            #Defining a random Zenith angle according to meiHime
            phi = np.random.choice(np.linspace(phiRad[0],phiRad[-1], len(meiHime)),p=meiHime)

            theta = 2*random.random()*np.pi

            #generate a random position on the disk
            position = np.array([rho*np.cos(theta) + self.position[0], rho*np.sin(theta) + self.position[1], self.position[2]])

            muons.append(mu.Muon(position, phi))

        return muons

    def __str__(self):
        string = "Generator —>[Rad: " + str(self.radius) + "m ], Pos: " + str(self.position) +"\n"
        return string
