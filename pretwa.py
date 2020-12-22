import pygame	# the main workhorse
import os		# i KNOW I'll need to detect OS and handle paths, etc
import sys		# for sys.exit
import math 	# for square roots on hex and other polygons

# allows us to use the == QUIT later instead of pygame.locals.QUIT
from pygame.locals import * 

WH = (255,255,255)	# white
BL = (0,0,0)		# black
GY = (128,128,128)	# grey
RE = (255,0,0)		# red

# we use legs as segments so it's all relative to any size of scale
scale = 67

# leg segment sizes
leg1 = (8/7)		# 1.1428571429
leg2 = (8/7) * 2 	# 2.2857142857
leg3 = (8/7) * 3	# 3.4285714286
leg4 = (8/7) * 4	# 4.5714285714
leg5 = (8/7) * 5	# 
leg6 = (8/7) * 6	# 
leg7 = (8/7) * 7	# 
ctr  = (8/7) * 4	# 4.5714285714, for code readability

# line points
# NW to SE
nwx = ctr - .5 * leg3
nwy = ctr - (math.sqrt(3)/2)*leg3
sex = ctr + .5 * leg3
sey = ctr + (math.sqrt(3)/2)*leg3
 
# SW to NE
swx = ctr - .5 * leg3
swy = ctr + (math.sqrt(3)/2)*leg3
nex = ctr + .5 * leg3
ney = ctr - (math.sqrt(3)/2)*leg3

# relative game board size
W  = int(ctr * scale * 2)
H  = int(ctr * scale * 2)

# Lines are xy start and xy stop coordinates, in inches/scaled
lines = {
	1 : [nwx,nwy,sex,sey],	# NW to SE
	2 : [swx,swy,nex,ney],	# SW to NE
	3 : [leg1,leg4,leg7,leg4]# E to W
}
 
# Circles are x,y,size and fill
# this is starting circles
circles = {
	1 : [ctr,ctr,leg1,0],
	2 : [ctr,ctr,leg2,0],
	3 : [ctr,ctr,leg3,0]
}

counter = 1
dots = {
	counter : [ctr,ctr]
}
for leg in [leg1,leg2,leg3]:
	dx1 = ctr - .5 * leg
	dy1 = ctr - (math.sqrt(3)/2)*leg
	dots[counter] = [dx1,dy1]
	counter += 1
	
	dx1 = ctr + .5 * leg
	dy1 = ctr + (math.sqrt(3)/2)*leg
	dots[counter] = [dx1,dy1]
	counter += 1
 
	dx1 = ctr - .5 * leg
	dy1 = ctr + (math.sqrt(3)/2)*leg
	dots[counter] = [dx1,dy1]
	counter += 1
 
	dx1 = ctr + .5 * leg
	dy1 = ctr - (math.sqrt(3)/2)*leg;
	dots[counter] = [dx1,dy1]
	counter += 1
  
# all of the dots on the center line
for leg in [leg1,leg2,leg3,leg4,leg5,leg6,leg7]:
	dots[counter] = [leg,ctr]
	counter += 1

def main():
	# can't run pygame without init, just do it
	pygame.init()

	# clock required to limit fps
	FPS = pygame.time.Clock()

	# one of (possibly many) surfaces to draw on
	SURF = pygame.display.set_mode((W,H))

	# the title bar
	pygame.display.set_caption("Solomon's Game")

	# default colors start at black
	r1,g1,b1 = (0,0,0)
	r2,g2,b2 = (0,0,0)

	# default x and y, until you click
	lw = 5            # line width of polygons

	# used to pulse color
	flip_r1,flip_g1,flip_b1 = (1,1,1)
	flip_r2,flip_g2,flip_b2 = (1,1,1)

	#Game loop begins
	while True:
		# current color of pulse, r,g,b set at bottom of while 
		r1,flip_r1 = get_pulse(flip_r1,r1,1) # mix and match your pulse, red
		b2,flip_b2 = get_pulse(flip_b2,b2,5) # mix and match your pulse, red
		pulse1 = (r1,g1,b1)
		pulse2 = (r2,g2,b2)

		# fill our surface with white
		SURF.fill(GY)

		# event section
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:

				# update where we just clicked
				(x,y) = pygame.mouse.get_pos()

			if event.type == QUIT:
				# pygame has a buggy quit, do both
				pygame.quit()
				sys.exit()

		draw_board(SURF,pulse1,pulse2,lw)
		# update the screen object itself
		pygame.display.update()	# update entire screen if no surface passed

		# tick the fps clock
		FPS.tick(60)

'''
Give us some points and we draw a line
'''
def draw_lines(surf,pulse,x1,y1,x2,y2,lw):
	pygame.draw.line(surf,pulse,(x1,y1),(x2,y2),lw)


'''
moved out to clean up the main()
'''
def draw_board(surf,pulse1,pulse2,lw):
	# update screen object with the lines
	for xy in lines:
		draw_lines(surf, pulse1,
			lines[xy][0] * scale,
			lines[xy][1] * scale,
			lines[xy][2] * scale,
			lines[xy][3] * scale,lw
		)

	for xy in circles:
		pygame.draw.circle(surf, pulse1, (
				circles[xy][0] * scale, 
				circles[xy][1] * scale
				), 
			circles[xy][2] * scale, lw
		)

	for xy in dots:
		pygame.draw.circle(surf, pulse2, (
				dots[xy][0] * scale, 
				dots[xy][1] * scale
				), 
			10, 0
		)

'''
just pulse 255 to 0 back to 255 repeat 
set boundaries so we don't get invalid rgb value
input: state of the flip, and current color code
return: updated flip and color code
'''
def get_pulse(flipped,c,step):

	if flipped:
		if c < 255: c += step
		else:
			c = 255
			flipped = 0
	else:
		if c > step: c -= step
		else:
			c = 0
			flipped = 1

	if c > 255: c = 255
	if c < 0: c = 0

	return (c,flipped)



if __name__ == '__main__':
	# capture ctrl c
	try:
		main()
	except KeyboardInterrupt:
		# pygame has a buggy quit, do both
		pygame.quit()
		sys.exit()



