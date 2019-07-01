# Topological_Nulls

Code to completely generate the poster: 'Magnetic Nulls from the Topological Perspective' presented ad EPS2019 by Chris Smiet et al. 

Prerequisites: Blender, LaTeX. 


Setup: 
download this repo *recursively* (BlendaViz: 
git clone --recurse-submodules git@github.com:smiet/Topological_Nulls.git
Install Blender. 
Find out where on your filesystem Blender has their configuration files (f.ex.:~/.config/blender/2.79/scripts/modules) 
Tell blender where to find the code: 
$cd [path-to-blender-config]/scripts/addons/modules
(in that folder link to the needed codes:)
ln -s [path-to-this-repo]/code/BlenDaViz
ln -s [path-to-this-repo]/code/integrate
ln -s [path-to-this-repo]/code/functions
