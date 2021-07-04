####################################################
#                 Simulation Script                #
#           Uses the Generator, detector           #
#                 and Muon Classes                 #
####################################################
import Generator as gn
import Detector as det
import Muon
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

#Entry message for program
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("$\tSimulation Script\t$")
print("$     For Generating Muons\t$ \n$\tand Counting Hits\t$")
print("$\t\t\t\t$")
print("$ *All Coordinates Cylindrical* $")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
print("     Regan Ross, Version 1.0\n\n")


### User Defined Parameters ###

#ONLY TEMPORARY
numEvents = 100

"""Detector"""
detectorRadius = 2.8 #m
detectorHeight = 7.9 #m
detectorCentre = np.array([0.,0.,0.]) #This is actually set by default
slantDepth = 6.011 # km w.e.

#Detector instantiation
miniCLEAN = det.Detector(detectorRadius, detectorHeight, slantDepth)

"""Generator"""
generatorRadius = 20. #m
generatorCentre = np.array([0.,0.,20.])

#Generator instantiation
muonGen = gn.Generator(generatorRadius, generatorCentre) #Making Generator with 30m radius

print("Detector generated and plotted.\n")
#miniCLEAN.detectorPlot(100)

resolution = int(input("How many bins?\n"))

thetaRad = np.linspace(0,np.pi/2,resolution)

slantDepth = 6.011 #km w.e.
I1 = 8.60e-6 # ± 0.53e-6 /sec/cm^2/sr
I2 = 0.44e-6 # ± 0.06e-6 /sec/cm^2/sr
lam1 = 0.45 # ± 0.01 km.w.e.
lam2 = 0.87 # ± 0.02 km.w.e.

meiHimeIntensity = (I1*np.exp(-slantDepth/(lam1*np.cos(thetaRad)))+I2*np.exp(-slantDepth/(lam2*np.cos(thetaRad))))/np.cos(thetaRad) # /cm^2/second
meiHimeIntensityNORM = meiHimeIntensity/np.sqrt(np.sum(meiHimeIntensity**2))
meiHimeIntensityNORM *= 3.77e-10 #NORMALIZED MUON INTENSITY

'''Figure Six: Muon Intensity (not normalized)'''
plt.figure(num = "Muon Intensity")
plt.plot(np.cos(thetaRad), meiHimeIntensity)
plt.ylabel('Muon Intensity /cm^2/sec/sr')
plt.xlabel('Cosine of Zenith Angle')
plt.title("Muon Angular Distribution (SNOLAB)")
plt.show()

'''Figure Seven: Muon Angular Distribution'''
#Normalized and then multiplied by local omnidirectional muon flux
plt.figure(num = "Normalized Muon Intensity")
plt.plot(np.cos(thetaRad), meiHimeIntensityNORM)
plt.ylabel('Muon Intensity (arbitrary units)')
plt.xlabel('Cosine of Zenith Angle')
plt.title("Normalized Muon Angular Distribution (SNOLAB)")
plt.show()
