#!/usr/bin/python3

import sys
import csv
import math
import random
import numpy as np


def calcDist(lat1, long1, lat2, long2):
    y1 = float(lat1)*math.pi/180
    y2 = float(lat2)*math.pi/180
    x1 = float(long1)*math.pi/180
    x2 = float(long2)*math.pi/180
    dy = y2 - y1
    dx = x2 - x1

    a = math.sin(dy/2) * math.sin(dy/2) 
    + math.cos(y1) * math.cos(y2) * math.sin(dx/2) * math.sin(dx/2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    R = 6371.0

    return R * c


n = 0
if len(sys.argv) > 1:
    n = int(sys.argv[1])

placenames = []
lats = []
longs = []
with open('places.csv') as fo:
    lines = csv.reader(fo, delimiter=',')
    for row in lines:
        placenames.append(row[0])
        lats.append(row[1])
        longs.append(row[2])

places = {}
nl = len(placenames)
if n > 1: # generate n random places from the input file
    for i in range(n):
        j = random.randint(1, nl-1)
        places[placenames[j]] = (lats[j], longs[j]) 
else:
    for j in range(1, nl):
        places[placenames[j]] = (lats[j], longs[j]) 

n = len(places)
names = list(places.keys())
coords = list(places.values())
dl = []
for i in range(n):
    for j in range(i+1, n):
        d = calcDist(coords[i][0], coords[i][1], coords[j][0], coords[j][1])
        dl.append((d, i, j))
nd = len(dl)
ar = np.array(dl, dtype=[('dist', 'f8'), ('p1', 'i4'), ('p2', 'i4')])
da = np.sort(ar, order='dist')

for i in range(nd):
    print("%32s%32s%12.2f km" % (names[da[i]['p1']], names[da[i]['p2']], da[i]['dist']))

davg = np.average(da[:]['dist'])
print("Average distance: %4.2d km. Closest pair: %s – %s %4.2d km." 
    % (davg, names[da[0]['p1']], names[da[0]['p2']], da[0]['dist']))

