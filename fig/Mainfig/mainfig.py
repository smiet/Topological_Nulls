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
# Make sure that the path to BlenDaViz and the integration library are in the front of the path.
code_folder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../../code")))
if code_folder not in sys.path:
     sys.path.insert(0, code_folder)

import integrate as ig
import BlenDaViz as bz


ncircvec=20    # Number of field lines per circle
ndipolecircs=4
nisotropes = 7
dipole_starts = []
for slide in np.linspace(.5, 1.5, ndipolecircs): #calculate the starting points for the dipole field lines
    dipole_starts.extend(ig.circlePoints(np.array((0,0,1)), slide=slide, radius=slide, npoints=ncircvec ))

streams = ig.stream_multi(dipole_starts, vvfn=ig.Dipole, tol=1e-7, iterMax=300000,  hMin=2e-6, lMax = 10)
streams.extend(ig.stream_multi(dipole_starts, vvfn=ig.Dipole, tol=1e-7, iterMax=300000,
                            hMin=2e-6, lMax = 10, intdir = 'back' ))
fieldlines = []
for stream in streams: #color the streamlines in sky-blue.
    if stream.sl>2:
        fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color = (0.        , 0.37109375, 0.49609375), radius=0.01))

isotrope_starts = ig.circlePoints(np.array((0,0,1)), slide=0.05, radius=0.05, npoints=nisotropes )

istreams = ig.stream_multi(isotrope_starts, vvfn=ig.Dipole_isotropes, tol=1e-7, iterMax=300000,
                            hMin=2e-6, lMax = 10, intdir = 'back')
isotrope_starts_2 = [-1*start for start in isotrope_starts]
istreams2 = ig.stream_multi(isotrope_starts_2, vvfn=ig.Dipole_isotropes, tol=1e-7,
                     iterMax=300000, hMin=2e-6, lMax = 10, intdir = 'forward')


#todo: make spiffy colors
cmap = plt.cm.get_cmap('gnuplot')
norm = plt.Normalize(vmin=0, vmax=nisotropes-1)
s_m = plt.cm.ScalarMappable(cmap = cmap, norm = norm)

color = (50,0,13) #color the isotropes in burgundy
for num, stream in enumerate(istreams):
    color = s_m.to_rgba(num)[:-1] # throw out the a of rgba
    fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color = color, radius=0.025))

for num, stream in enumerate(istreams2):
    color = s_m.to_rgba(num)[:-1] # throw out the a of rgba
    fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color = color, radius=0.025))

vecPoints= ig.circlePoints(np.array((0,0,1)), slide=1.5, radius=1.5, npoints=nisotropes )

for num, point in enumerate(vecPoints):
    color = s_m.to_rgba(num)[:-1] # throw out the a of rgba
    bz.vec(point, ig.Dipole(point), length=7*ig.norm(ig.Dipole(point)), color=color)



bpy.data.scenes['Scene'].render.filepath = '../mainfig.png'
bpy.ops.render.render(write_still=True)
