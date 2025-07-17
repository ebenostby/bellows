# This Makefile serves as a reminder of how to ensure you've got 
# the svgwrite library and a venv to run it in for Python's sake
# 

bellows1.svg bellows2.svg:	bellows.py
	source venv/bin/activate; python bellows.py

bellows.py:	venv/lib/python3.13/site-packages/svgwrite

venv/lib/python3.13/site-packages/svgwrite:
	python3 -m venv venv
	source venv/bin/activate; pip install svgwrite
##all:
##	python -m venv venv/
##	source venv/bin/activate; pip install svgwrite; python bellows.py
