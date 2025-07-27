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

def do_bellows(name, page_x, page_y, length, top, bot, other, folds, side_space, slack, do_zigzag=1, up_down=0, connective=2):
	dwg = svgwrite.Drawing(name, ("%6.1fmm"%page_x, "%6.1fmm"%page_y), profile='full')
	inkscape = Inkscape(dwg)
	dwg.viewbox(0, 0, page_x, page_y)	
	cut = inkscape.layer(label="CUT")
	dwg.add(cut)
	score = inkscape.layer(label="SCORE")
	dwg.add(score)
	n_folds = sum(folds)
	slat_y = length / n_folds
	slat_offset = (other / n_folds)/2
	if (up_down):
		slat_2 = (slat_y+slat_offset)/2
		slat_1 = (slat_y-slat_offset)/2
	else:
		slat_1 = (slat_y+slat_offset)/2
		slat_2 = (slat_y-slat_offset)/2
	top_margin=5
	
	# overall shape
	extra_around_cut = side_space
	cut.add(dwg.polygon( (((page_x-top)/2-extra_around_cut,top_margin),
		((page_x+top)/2+extra_around_cut, top_margin), 
		((page_x+bot)/2+extra_around_cut,top_margin+length),
		((page_x-bot)/2-extra_around_cut, top_margin+length)), stroke='black',fill='none'))
	# individual stiffeners or slats
	def do_slatpair(cursor, next_cursor, slat_1, slat_2, slack, connective):

		if (do_zigzag):
			y_pos = cursor+slat_1-slack
			y2_pos = cursor+slat_1+slat_2-slack

			width1=top+(cursor/length)*(bot-top)-2*side_space
			width2=top+(y_pos/length)*(bot-top)
			width3=top+(y2_pos/length)*(bot-top)-2*side_space
			
			cut.add(dwg.rect(((page_x-width2)/2+connective,y_pos+top_margin),(width2-connective*2,slack), stroke='black',fill='none'))
			score.add(dwg.line( ((page_x-width1)/2,cursor+top_margin),((page_x-width2)/2,y_pos+top_margin),stroke='green'))
			score.add(dwg.line( ((page_x+width1)/2,cursor+top_margin),((page_x+width2)/2,y_pos+top_margin),stroke='green'))
			score.add(dwg.line( ((page_x-width2)/2,y_pos+top_margin+slack), ((page_x-width3)/2,y2_pos+top_margin),stroke='green'))
			score.add(dwg.line( ((page_x+width2)/2,y_pos+top_margin+slack), ((page_x+width3)/2,y2_pos+top_margin),stroke='green'))
			#
			score.add(dwg.line( ((page_x-width2)/2,y_pos+top_margin),((page_x-width2)/2,y_pos+top_margin+slack),stroke='green'))
			score.add(dwg.line( ((page_x+width2)/2,y_pos+top_margin),((page_x+width2)/2,y_pos+top_margin+slack),stroke='green'))
			score.add(dwg.line( ((page_x-width3)/2,y2_pos+top_margin),((page_x-width3)/2,y2_pos+top_margin+slack),  stroke='green'))
			score.add(dwg.line( ((page_x+width3)/2,y2_pos+top_margin), ((page_x+width3)/2,y2_pos+top_margin+slack),stroke='green'))

			y_pos = y2_pos
			# width1=top+(cursor/length)*(bot-top) - connective*2
			width2=top+(y_pos/length)*(bot-top)-2*side_space - connective*2
			cut.add(dwg.rect(((page_x-width2)/2,y_pos+top_margin),(width2,slack), stroke='black',fill='none'))
		else:	
			for y_pos in ( cursor+slat_1-slack, cursor+slat_1+slat_2-slack):
				width=top+(y_pos/length)*(bot-top)-2*connective			
				cut.add(dwg.rect(((page_x-width)/2,y_pos+top_margin),(width,slack), stroke='black',fill='none'))
	cursor = 0
	for f in folds:
		nextc = cursor + length*f/n_folds
		do_slatpair(cursor, nextc, slat_1*f, slat_2*f, slack, connective)
		cursor = nextc
	
	# score line
	if (not do_zigzag):
		score.add(dwg.line( ((page_x-top)/2,top_margin), ((page_x-bot)/2, top_margin+length), stroke='green'))
		score.add(dwg.line( ((page_x+top)/2,top_margin), ((page_x+bot)/2, top_margin+length), stroke='green'))

	dwg.save()
	

def main():
	# page size for svg canvas
	page_x = 8.5*inch
	page_y = 14*inch
	# file names for the two sides
	b1_name="bellows1.svg"
	b2_name="bellows2.svg"
	# overall length of the bellows, from film plane to lensboard, unfolded
	length = 270  # was 350
	# width of the bellows at top and bottom, on the main face of the bellows
	b1_top = 156  # extra half fold
	b1_bot = 55
	# width of the bellows at top and bottom, on the side face of the bellows
	b2_top = 95 # expect to cut a half fold at top
	b2_bot = 45
	# an array of fold lengths is passed as "folds". A normal bellows has N 1's for N pairs of slats, but  you can 
	# have shorter or longer ones in the list. Normally you might have some shorter ones at the ends for clearance.
	n_folds = 18
	folds = [1]*n_folds
	folds = [.6,.7,.85]+([1]*12)+[.75]
	
	# room between edge of the slat and the corner of the bellows fabric on each side. 
	# The zig-zag occupies this space. On non-zig-zag it's just an extra tab to hold it together before gluing, then torn off.
	side_space = 7
	# the space between slats where folds are located.
	slat_slack = 1
	# do_zigzag enables slats that reach to the edge, diagonally making folds
	# halves makes half slats for extra clearance. 
	# connective is the width of a little tab to join two slats
	connective = 2
	do_bellows(b1_name,page_x, page_y, length, b1_top, b1_bot, b2_top-b2_bot, folds, side_space, slat_slack, do_zigzag=1, up_down=0, connective = connective)
	do_bellows(b2_name,page_x, page_y, length, b2_top, b2_bot, b1_top-b1_bot, folds, side_space, slat_slack, do_zigzag=0, up_down=1, connective = connective)

main()
