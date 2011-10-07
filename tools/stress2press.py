#!/usr/bin/env python

# Script: stress2press.py
# Author: Mario Orsi (orsimario at gmail.com, www.soton.ac.uk/~orsi)
# Purpose: Reads a file containing stress components calculated
#          with the LAMMPS commands 'compute stress/atom' and
#          'fix ave/spatial', and converts to corresponding pressures
# Syntax: stress2press.py inputFile area
#         inputFile = LAMMPS output file generated by fix ave/spatial
#         area = surface area of slabs [Angstrom^2]
# Example: stress2press.py stress.zProfile 4650 > lpp.dat
# References: - Thompson et al, J Chem Phys 131, 154107 (2009)
#             - Orsi et al, J Phys Condens Matter 22, 155106 (2010),
#               section 5.2

import sys,os,string

if len(sys.argv) != 3:
  print "Syntax: stress2press.py inputFile area"
  sys.exit()

inFileName = sys.argv[1]
area = float(sys.argv[2])
inFile = open(inFileName, "r")
lines = inFile.readlines()
inFile.close()

# find slab thickness (delta):
for line in lines:
    if line[0] != '#': # ignore comments
        words = string.split(line)
        if len(words) == 2:
            nBins = int(words[1])
        else:
            if int(words[0]) == 1:
                coordLower = float(words[1])
            if int(words[0]) == nBins:
                coordUpper = float(words[1])
delta = abs( coordUpper - coordLower ) / ( nBins - 1 )
slabVolume = area * delta

# calc & output Pxx Pyy Pzz (file) and P_L-P_N profile (screen):
outFile = open('zPress_xyz.dat', 'w')
for line in lines:
    if line[0] != '#': # ignore comments
        words = string.split(line)
        if len(words) == 6:
            coord = float(words[1])
            nCount = float(words[2])
            xxStress = float(words[3]) * nCount / slabVolume
            yyStress = float(words[4]) * nCount / slabVolume
            zzStress = float(words[5]) * nCount / slabVolume      
            xxPress = -xxStress
            yyPress = -yyStress
            zzPress = -zzStress
            outFile.write('%f %f %f %f\n' % (coord,xxPress,yyPress,zzPress))
            latPressProf = 0.5*(xxPress+yyPress) - zzPress
            print coord, latPressProf # [A, atm]
outFile.close()
    
