# posindex_start.py: generate a plot of the vector field around a 3d magnetic null.
# A yellow transparend sphere is located at the origin, and the vector field of the
# null is shown by it's integral curves, as well as vectors located on the surface
# of a ball around the null
#
#
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


startlen = .35

# generate the points at which vectors are to be evaluated
ncirc=15
ncircvec=50
vecpoints = [[np.array((np.sqrt(1-z**2)*np.cos(t), np.sqrt(1-z**2)*np.sin(t), z))
                        for t in np.linspace(np.pi, 3*np.pi, ncircvec+1)[:ncircvec]]
                            for z in np.cos(np.linspace(0,np.pi,ncirc+2)[1:-1])]
vecpoints.append([np.array((0,0,1))])
vecpoints.append([np.array((0,0,-1))])

#generate the points from which streamlines are to be traced
nstreams=15
streampoints = []
for r in np.linspace(0.01, 1.5, 3):
    streampoints.extend(ig.circlePoints(np.array((0,0,1)), radius = r, slide=8,
        npoints = nstreams, rot=r))
    streampoints.extend(ig.circlePoints(np.array((0,0,1)), radius = r, slide=-8,
        npoints = nstreams, rot=r))

fn=partial(ig.ZeroField, index=-1)
#def fn(xx): return np.array((0,0,1))


vecs = []
vc = cm.get_cmap('plasma', 10) # vertical colors
for i in range(len(vecpoints)):
    cdict = {'red':   [[0.0,  vc(i)[0], vc(i)[0]],
                       [1.0,  .5, .5]],
             'green': [[0.0,  vc(i)[1], vc(i)[1]],
                       [1.0,  .5, .5]],
             'blue':  [[0.0,  vc(i)[2], vc(i)[2]],
                       [1.0,  .5, .5]]}
    cmap = matplotlib.colors.LinearSegmentedColormap('map'+str(i), segmentdata=cdict)
    norm = plt.Normalize(vmin=0, vmax=ncircvec)
    s_m = plt.cm.ScalarMappable(cmap = cmap, norm = norm)
    for pointindex in range(len(vecpoints[i])):
        point=vecpoints[i][pointindex]
        color = s_m.to_rgba(pointindex)[:-1] # throw out the a of rgba
        vecs.append(bz.vec(np.array((0,0,0)), fn(point), length=1, thin=3, color=color))



bpy.data.scenes['Scene'].render.filepath = '../negindex_end.png'
bpy.ops.render.render(write_still=True)
