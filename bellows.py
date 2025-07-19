# A python function to create the cut lines for bellows stiffeners as an svg file.
# Also will create a pair of score lines for convenience in holding the slats together
# until they are glued in place. The edge beyond the score line can then be trimmed off.

# all measurements in mm
#
# uses the now-moribund library svgwrite, 
# https://svgwrite.readthedocs.io/en/latest/
# https://github.com/mozman/svgwrite
# pip install svgwrite

import svgwrite
from svgwrite.extensions import Inkscape
inch=25.4

def do_bellows(name, page_x, page_y, length, top, bot, other, n_folds, side_space, slack, do_zigzag=1):
	dwg = svgwrite.Drawing(name, ("%6.1fmm"%page_x, "%6.1fmm"%page_y), profile='full')
	inkscape = Inkscape(dwg)
	dwg.viewbox(0, 0, page_x, page_y)	
	cut = inkscape.layer(label="CUT")
	dwg.add(cut)
	score = inkscape.layer(label="SCORE")
	dwg.add(score)
	slat_y = length / n_folds
	slat_offset = (other / n_folds)/2
	slat_1 = (slat_y+slat_offset)/2
	slat_2 = (slat_y-slat_offset)/2
	top_margin=10
	
	# overall shape
	extra_around_cut = do_zigzag*side_space
	cut.add(dwg.polygon( (((page_x-top)/2-extra_around_cut,top_margin),
		((page_x+top)/2+extra_around_cut, top_margin), 
		((page_x+bot)/2+extra_around_cut,top_margin+length),
		((page_x-bot)/2-extra_around_cut, top_margin+length)), stroke='black',fill='none'))
	# individual stiffeners or slats
	for i in range(n_folds):
		cursor=length*i/n_folds
		next_cursor=length*(i+1)/n_folds

		if (do_zigzag):
			y_pos = cursor+slat_1-slack
			y2_pos = cursor+slat_1+slat_2-slack

			width1=top+(cursor/length)*(bot-top)-2*side_space
			width2=top+(y_pos/length)*(bot-top)
			width3=top+(y2_pos/length)*(bot-top)-2*side_space
			cut.add(dwg.rect(((page_x-width2)/2,y_pos+top_margin),(width2,slack), stroke='black',fill='none'))
			score.add(dwg.line( ((page_x-width1)/2,cursor+top_margin),((page_x-width2)/2,y_pos+top_margin),stroke='green'))
			score.add(dwg.line( ((page_x+width1)/2,cursor+top_margin),((page_x+width2)/2,y_pos+top_margin),stroke='green'))
			score.add(dwg.line( ((page_x-width2)/2,y_pos+top_margin+slack), ((page_x-width3)/2,y2_pos+top_margin),stroke='green'))
			score.add(dwg.line( ((page_x+width2)/2,y_pos+top_margin+slack), ((page_x+width3)/2,y2_pos+top_margin),stroke='green'))
			y_pos = y2_pos
			width1=top+(cursor/length)*(bot-top)
			width2=top+(y_pos/length)*(bot-top)-2*side_space
			cut.add(dwg.rect(((page_x-width2)/2,y_pos+top_margin),(width2,slack), stroke='black',fill='none'))
		else:	
			for y_pos in ( cursor+slat_1-slack, cursor+slat_1+slat_2-slack):
				width=top+(y_pos/length)*(bot-top)-2*side_space			
				cut.add(dwg.rect(((page_x-width)/2,y_pos+top_margin),(width,slack), stroke='black',fill='none'))
	
	# score line
	if (not do_zigzag):
		score.add(dwg.line( ((page_x-top)/2+side_space,top_margin), ((page_x-bot)/2+side_space, top_margin+length), stroke='green'))
		score.add(dwg.line( ((page_x+top)/2-side_space,top_margin), ((page_x+bot)/2-side_space, top_margin+length), stroke='green'))

	dwg.save()
	

def main():
	# page size for svg canvas
	page_x = 8.5*inch
	page_y = 14*inch
	# file names for the two sides
	b1_name="bellows1.svg"
	b2_name="bellows2.svg"
	# overall length of the bellows, from film plane to lensboard, unfolded
	length = 350
	# width of the bellows at top and bottom, on the main face of the bellows
	b1_top = 152.5  # extra half fold
	b1_bot = 55
	# width of the bellows at top and bottom, on the side face of the bellows
	b2_top = 97 # expect to cut a half fold at top
	b2_bot = 45
	# number of pairs of slats of the bellows along each face. 
	n_folds = 18
	# room between edge of the slat and the corner of the bellows fabric on each side. 
	# The zig-zag occupies this space.
	side_space = 7
	# the space between slats where folds are located.
	slat_slack = 1.5

	do_bellows(b1_name,page_x, page_y, length, b1_top, b1_bot, b2_top-b2_bot, n_folds, side_space, slat_slack, do_zigzag=1)
	do_bellows(b2_name,page_x, page_y, length, b2_bot, b2_top, b1_top-b1_bot, n_folds, side_space, slat_slack, do_zigzag=0)

main()
