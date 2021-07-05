import numpy as np
from Elements import Muon as mu
from Elements import Generator as gen
from Elements import Detector as det
import csv
import argparse #For future options


### Commandline Args ###
parser = argparse.ArgumentParser(description='Necessary Arguments')
parser.add_argument('numOfMuons',\
 help="The integer number of muons to generate in csv", type=int,\
 action='store', default=1)
parser.add_argument('outputFile', action='store',\
 help="The name of the csv file in which to output.", nargs='?', type=str, default="muonGenOutput.txt")
args = parser.parse_args()


print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("%   Muon Generation for Chroma Simulations  %")
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n")

# Coordinate system to be based on the detector geometry.
# All elements will take their positions with respect to the instantiated detector

### Detector Parameters ###
OD_Radius = 6.1722 #m
OD_Height = 13.300 #m
OD_Position = np.array([0.,0.,0.])
#Instantiation
print("Instantiating Detector:")
OD = det.Detector(OD_Radius, OD_Height, "nEXO_OD", OD_Position) #Position at Center
print(str(OD))


### Generator Parameters ###
Gen_Radius = 20 #m
Gen_Position = np.array([0.,0.,5.0 + OD_Height/2]) #20 m above Detector
#Instantiation
print("Instantiating Generator:")
MuonGen = gen.Generator(Gen_Radius, Gen_Position)
print(str(MuonGen))


### Open File ###

outputFile = open(args.outputFile, 'a')


### Generate Muons ###
muons = MuonGen.generateMuons(args.numOfMuons)
count = 0
for i in range(args.numOfMuons):
    #outputFile.write(str(muons[i]))
    if not OD.testIntersection(muons[i]) is None:
        outputFile.write(str(OD.testIntersection(muons[i]))+ "\n")
        #outputFile.write("\n")
        count += 1

outputFile.write(str(count))
