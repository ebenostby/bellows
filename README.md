# bellows
A routine to draw camera bellows stiffeners as svg files.

Edit the bellows.py file for your own use, changing the
dimensions, run the program, and it will generate an svg file
containing the slats. The numbers in the file right now represent
the slats for a Zeiss Ikon Nixe 595, an uncommon camera that takes 122 film.

If you can't measure exactly (and even if you can), it's probably a good
idea to extend your new bellows by a slat at each end so you'll have something
to trim off, and to help you compensate for the inevitable difficulty in fitting.

No UI is provided (neither GUI nor CLI).

You need a copy of svgwrite, available via 
	pip install svgwrite
The Makefile will fetch svgwrite, put it in a local venv for python,
and execute the bellows command. Mostly this is so I don't have to 
remember what to do in 2 years when I make another bellows.

The bellows drawing is segmented into cut lines and score lines.
The score lines are intended to be strong enough that the edge
material can hold the slats in position for gluing, yet deep enough that 
the remaining material can be easily removed after the slats are glued into place.

I examine the resulting file in inkscape and cut it with a desktop cutter
(KNK,  e-clipse, etc) using Sure Cuts A Lot. You could just print it out and cut
it with a knife. The score lines and the cut lines are in different layers in the 
file. 

All this won't help you with the gluing and folding, but it's a start.
