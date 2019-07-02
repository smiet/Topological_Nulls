# mainfig.py: Illustration of the main idea of the isotrope field:
# Several streamlines of a dipole field is shown, with an earth at the center, and
# a few isotrope lines are drawn as well.
#
# All the field lines and vectors are calculated in this script, but the final product
# relies on some objects already being present in the .blend file (the earth, the semi-transparent
# sphere, and the plane). This could in principle also be coded, but alas, no time!
#
# coded by Christopher Berg Smiet on July 01
# Csmiet@pppl.gov
#
import os, sys, inspect       # For importing the submodules in a platform-independend robust way
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
import bpy                    # This module is only available inside of Blender's version of python, comment when debugging
from functools import partial # create new funtions from old functions (and strip the kwargs)
# Make sure that the path to BlenDaViz and the integration library are in the front of the path.
code_folder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../code")))
if code_folder not in sys.path:
     sys.path.insert(0, code_folder)

import integrate as ig
import BlenDaViz as bz

#Dipole field properties:
strength = 0.5
direction = np.array((-1, 0, -1))


ncircvec=30    # Number of field lines per circle
ndipolecircs=5
dipole_starts = []
for slide in np.linspace(.05, 1.5, ndipolecircs): #calculate the starting points for the dipole field lines
    dipole_starts.extend(ig.circlePoints(np.array((0,0,1)), slide=slide, radius=slide, npoints=ncircvec ))

streams = ig.stream_multi(dipole_starts, vvfn=ig.Dipole, tol=1e-7, iterMax=300000,  hMin=2e-6, lMax = 10)
streams.extend(ig.stream_multi(dipole_starts, vvfn=ig.Dipole, tol=1e-7, iterMax=300000,
                            hMin=2e-6, lMax = 10, intdir = 'back' ))
fieldlines = []
for stream in streams:
    if stream.sl>2:
        fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color = (1,1,1), radius=0.01))

isotrope_starts = ig.circlePoints(np.array((0,0,1)), slide=0.05, radius=0.05, npoints=int(ncircvec/3) )

istreams = ig.stream_multi(isotrope_starts, vvfn=ig.Dipole_isotropes, tol=1e-7, iterMax=300000,
                            hMin=2e-6, lMax = 10, intdir = 'back')
isotrope_starts_2 = [-1*start for start in isotrope_starts]
istreams.extend(ig.stream_multi(isotrope_starts_2, vvfn=ig.Dipole_isotropes, tol=1e-7,
                     iterMax=300000, hMin=2e-6, lMax = 10, intdir = 'forward'))


#todo: make spiffy colors
color = (1,0,0)
for stream in istreams:
    fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color = color, radius=0.05))

vecPoints=dipole_starts[0::3] #pythonic for every third element
for point in vecPoints:
    bz.vec(point, ig.Dipole(point), length=.1*ig.norm(ig.Dipole(point)), color=color)



bpy.data.scenes['Scene'].render.filepath = './mainfig.png'
bpy.ops.render.render(write_still=True)



#vecpoints = [[np.array((np.sqrt(1-z**2)*np.cos(t), np.sqrt(1-z**2)*np.sin(t), z))
#                        for t in np.linspace(np.pi, 3*np.pi, ncircvec+1)[:ncircvec]]
#                            for z in np.cos(np.linspace(0,np.pi,ncirc+2)[1:-1])]
#
#
#
#vecpoints.append([np.array((0,0,1))])
#vecpoints.append([np.array((0,0,-1))])
#
#fn=partial(ig.ZeroField, index=-1)
#
#vc = cm.get_cmap('plasma', 10) # vertical colors
#for i in range(len(vecpoints)):
#    cdict = {'red':   [[0.0,  vc(i)[0], vc(i)[0]],
#                       [1.0,  .5, .5]],
#             'green': [[0.0,  vc(i)[1], vc(i)[1]],
#                       [1.0,  .5, .5]],
#             'blue':  [[0.0,  vc(i)[2], vc(i)[2]],
#                       [1.0,  .5, .5]]}
#    cmap = matplotlib.colors.LinearSegmentedColormap('map'+str(i), segmentdata=cdict)
#    norm = plt.Normalize(vmin=0, vmax=ncircvec)
#    s_m = plt.cm.ScalarMappable(cmap = cmap, norm = norm)
#    for pointindex in range(len(vecpoints[i])):
#        point=vecpoints[i][pointindex]
#        color = s_m.to_rgba(pointindex)[:-1] # throw out the a of rgba
#        bz.vec(np.array((0,0,0)), fn(point), length=1, color=color, thin = 3)


bpy.data.scenes['Scene'].render.filepath = '../index_ball.png'
bpy.ops.render.render(write_still=True)
