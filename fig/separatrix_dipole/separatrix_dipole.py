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


#guide field properties:
strength = 0.5
direction = np.array((-1, 0, -1))

fn = partial(ig.Dipole_guide, d=direction, strength = strength)

#generate the starting points of the streamline
nulls = ig.Dipole_nulls(strength, direction)
npoints=60
startpoints = []
null1 = ig.zeroPoints(nulls[0], ig.Dipole(nulls[0]), sign=-1, npoints=npoints)
null2 = ig.zeroPoints(nulls[1], ig.Dipole(nulls[1]), sign=1, npoints=npoints)


n1fan = ig.stream_multi(null1.fanpoints, vvfn=fn, tol=1e-7, iterMax=300000,  hMin=2e-6, lMax = 100, intdir='back')
n1spine= ig.stream_multi(null1.fanpoints, vvfn=fn, tol=1e-7, iterMax=300000,  hMin=2e-6, lMax = 100, intdir='forward')

n2fan = ig.stream_multi(null1.backward, vvfn=fn, tol=1e-7, iterMax=300000,  hMin=2e-6, lMax = 100, intdir='forward')
n2spine = ig.stream_multi(null2.backward, vvfn=fn, tol=1e-7, iterMax=300000,  hMin=2e-6, lMax = 100, intdir='back')

fieldlines = []
for stream in n1fan:
        fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color = (0.        , 0.37109375, 0.49609375) , radius=0.01))
for stream in n1spine:
        fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color = 'c', radius=0.01))

for stream in n2fan:
        fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color =  (.639, .757, .678), radius=0.01))
for stream in n2spine:
        fieldlines.append(bz.plot(stream.x, stream.y, stream.z, color = 'c', radius=0.01))


bpy.data.scenes['Scene'].render.filepath = './mainfig.png'
bpy.ops.render.render(write_still=True)
