default:   beamer

beamer:
	pdflatex -synctex=1 -interaction=nonstopmode -enable-write18 nulls.tex
#	bibtex chaoscrash
#	pdflatex -synctex=1 -interaction=nonstopmode  -enable-write18 nulls.tex
#	pdflatex -synctex=1 -interaction=nonstopmode -enable-write18 nulls.tex

indexFig:
	cd fig/indexFig; blender -b  scene_lowres.blend -P 3d_lines.py 
