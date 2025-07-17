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
inch=25.4

def do_bellows(name, page_x, page_y, length, top, bot, other, n_folds, side_space, slack):
	dwg = svgwrite.Drawing(name, ("%6.1fmm"%page_x, "%6.1fmm"%page_y), profile='tiny')
	dwg.viewbox(0, 0, page_x, page_y)	

	slat_y = length / n_folds
	slat_offset = (other / n_folds)/2
	slat_1 = (slat_y+slat_offset)/2
	slat_2 = (slat_y-slat_offset)/2
	top_margin=10
	
	# overall shape
	dwg.add(dwg.polygon( (((page_x-top)/2,top_margin),
		((page_x+top)/2, top_margin), 
		((page_x+bot)/2,top_margin+length),
		((page_x-bot)/2, top_margin+length)), stroke='black',fill='none'))
	# individual stiffeners or slats
	for i in range(n_folds):
		cursor=length*i/n_folds

		for y_pos in ( cursor+slat_1-slack, cursor+slat_1+slat_2-slack):
			width=top+(y_pos/length)*(bot-top)-2*side_space
			dwg.add(dwg.rect(((page_x-width)/2,y_pos+top_margin),(width,slack), stroke='black',fill='none'))
	
	# score line
	dwg.add(dwg.line( ((page_x-top)/2+side_space,top_margin), ((page_x-bot)/2+side_space, top_margin+length), stroke='green'))
	dwg.add(dwg.line( ((page_x+top)/2-side_space,top_margin), ((page_x+bot)/2-side_space, top_margin+length), stroke='green'))

	dwg.save()
	

def main():
	# page size for svg canvas
	page_x = 8.5*inch
	page_y = 14*inch
	# file names for the two sides
	b1_name="bellows1.svg"
	b2_name="bellows2.svg"
	# overall length of the bellows, from film plane to lensboard, unfolded
	length = 340
	# width of the bellows at top and bottom, on the main face of the bellows
	b1_top = 145
	b1_bot = 58
	# width of the bellows at top and bottom, on the side face of the bellows
	b2_top = 85
	b2_bot = 35
	# number of pairs of slats of the bellows along each face. 
	n_folds = 18
	# room between edge of the slat and the corner of the bellows fabric on each side. 
	# The zig-zag occupies this space.
	side_space = 10
	# the space between slats where folds are located.
	slat_slack = 1.5

	do_bellows(b1_name,page_x, page_y, length, b1_top, b1_bot, b2_top-b2_bot, n_folds, side_space, slat_slack)
	do_bellows(b2_name,page_x, page_y, length, b2_bot, b2_top, b1_top-b1_bot, n_folds, side_space, slat_slack)

main()
