default:   images poster

poster:
	pdflatex -synctex=1 -interaction=nonstopmode -enable-write18 nulls.tex
	bibtex nulls
	pdflatex -synctex=1 -interaction=nonstopmode  -enable-write18 nulls.tex
	pdflatex -synctex=1 -interaction=nonstopmode -enable-write18 nulls.tex

images: indexFig mainfig posindex negindex separatrix_dipole

indexFig:
	cd fig/indexFig; blender -b  scene_lowres.blend -P 3d_lines.py 

mainfig:
	cd fig/Mainfig; blender -b scene_earth.blend -P mainfig.py

posindex:
	cd fig/posindex; blender -b scene_ball_small.blend -P posindex_start.py; blender -b scene_ball_small.blend -P posindex_end.py

negindex:
	cd fig/negindex; blender -b scene_ball_small.blend -P negindex_start.py; blender -b scene_ball_small.blend -P negindex_end.py

separatrix_dipole:
	cd fig/separatrix_dipole; blender -b scene_earth_centered.blend -P separatrix_dipole.py


