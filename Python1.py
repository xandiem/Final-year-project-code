from os.path import dirname, join, abspath
from pyrep import PyRep
from pyrep.objects.shape import Shape
from pyrep.const import PrimitiveShape
from random import randint
import json
import os
import sys    
import termios
import fcntl
import time

#setup CoppeliaSim and launch the scene file
SCENE_FILE = join(dirname(abspath(__file__)), 'scene.ttt')
pr = PyRep()
pr.launch(SCENE_FILE, headless=False) 
pr.start()  # Start the simulation

#rectangle method for room generation 
def rectangular_room_generation():
	#generate random to insert into the shape generation	
	value_x = randint(30,80)/10
	value_y = randint(30,80)/10
	#store set of points
	#top_cuboid = [(-value_x/2,2.0,2.0), (value_x/2,2.0,2.0), (-value_x/2,2.0, 0.0), 				(value_x/2,2.0,0.0)]
	top = Shape.create(type=PrimitiveShape.CUBOID,
                     size=[value_x, 0.05, 2.0],
                     color=[0.8, 0.8, 0.8],
		      		 position=[0.0, 2.0, 1.0],
                     static=True, respondable=False)
	#left_cuboid = [(-value_x/2,2.0,2.0), (-value_x/2,2.0-(value_y),2.0), (-value_x/2,2.0, 				0.0), (-value_x/2,2.0-(value_y),0.0)]
	left = Shape.create(type=PrimitiveShape.CUBOID,
	              		  size=[0.05, value_y, 2.0],
                  		color=[0.8, 0.8, 0.8],
		      			  		position=[-value_x/2, 2-(value_y/2), 1.0],
                      static=True, respondable=False)
	#right_cuboid = [(value_x/2,2.0,2.0), (value_x/2,2.0-(value_y),2.0), (value_x/2,2.0, 				0.0), (value_x/2,2.0-(value_y),0.0)]
	right = Shape.create(type=PrimitiveShape.CUBOID,
                       size=[0.05, value_y, 2.0],
                       color=[0.8, 0.8, 0.8],
		                 	 position=[value_x/2, 2-(value_y/2), 1.0],
                       static=True, respondable=False)
	#bottom_cuboid = [(-value_x/2,2.0-(value_y),2.0), (value_x/2,2-(value_y),2.0), 				(-value_x/2,2.0-(value_y),0.0), (value_x/2,2-(value_y),0.0)]
	bottom = Shape.create(type=PrimitiveShape.CUBOID,
                      	size=[value_x, 0.05, 2.0],
                      	color=[0.8, 0.8, 0.8],
		      							position=[0.0, 2-(value_y), 1.0],
                      	static=True, respondable=False)
	print("value_x", value_x)
	print("valuey: ", value_y)
	data = {
		'shape': 'lroom',
    	'point1': (value_x/2, 2.0),
    	'point2': (-value_x/2, 2.0),
    	'point3': (-value_x/2, 2-value_y),
    	'point4': (-value_x/2, 2-value_y)
	}
	with open('data.json', 'a') as f:
		json.dump(data, f)
	#shape = [(value_x/2, 2.0), (-value_x/2, 2.0), (-value_x/2, 2-value_y), 
	#		(-value_x/2, 2-value_y)]
	#print(shape)
	print(data)
	
def t_room_generation():
	#generate random to insert into the shape generation
	rand = randint(30,80)/10
	#print("troom: ", rand + "")
	top = Shape.create(type=PrimitiveShape.CUBOID,
                      size=[rand, 0.05, 2.0],
                      color=[0.8, 0.8, 0.8],
		      		  position=[0.0, 2.0, 1.0],
                      static=True, respondable=False)
	top_left = Shape.create(type=PrimitiveShape.CUBOID,
	              			size=[0.05, rand/2, 2.0],
                      		color=[0.8, 0.8, 0.8],
		      				position=[-rand/2, 2-(rand/4), 1.0],
                      		static=True, respondable=False)
	top_right = Shape.create(type=PrimitiveShape.CUBOID,
                      		 size=[0.05, rand/2, 2.0],
                      		 color=[0.8, 0.8, 0.8],
		      								 position=[rand/2,2-(rand/4), 1.0],
                      		 static=True, respondable=False)
	middle_left = Shape.create(type=PrimitiveShape.CUBOID,
                      			 size=[rand/3, 0.05, 2.0],
                      			 color=[0.8, 0.8, 0.8],
		      									 position=[-(rand/3), 2-(rand/2), 1.0],
                      			 static=True, respondable=False)
	middle_right = Shape.create(type=PrimitiveShape.CUBOID,
                      				size=[rand/3, 0.05, 2.0],
                      				color=[0.8, 0.8, 0.8],
		      						position=[rand/3, 2-(rand/2), 1.0],
                      				static=True, respondable=False)
	bottom_left = Shape.create(type=PrimitiveShape.CUBOID,
	              				size=[0.05, rand/2, 2.0],
                      			color=[0.8, 0.8, 0.8],
		      					position=[-rand/2+(rand/3), 2-(0.75*rand), 1.0],
                      			static=True, respondable=False)
	bottom_right = Shape.create(type=PrimitiveShape.CUBOID,
                      				size=[0.05, rand/2, 2.0],
                      				color=[0.8, 0.8, 0.8],
		      						position=[rand/2-(rand/3), 2-(0.75*rand), 1.0],
                      				static=True, respondable=False)
	bottom = Shape.create(type=PrimitiveShape.CUBOID,
                      	size=[rand/3, 0.05, 2.0],
                      	color=[0.8, 0.8, 0.8],
		      			position=[0.0, 2-rand, 1.0],
                      	static=True, respondable=False)
	data = {
		'shape': 'troom',
    	'point1': (rand/2, 2.0),
    	'point2': (-rand/2, 2.0),
    	'point3': (-rand/2, 2.0-rand/2),
    	'point4': (-rand/2+(rand/3), 2.0-rand/2),
    	'point5': (-rand/2+rand/3, 2.0-rand),
    	'point6': (rand/2-rand/3, 2.0-rand),
    	'point7': (rand/2-rand/3, 2.0-rand/2),
    	'point8': (rand/2, 2-rand/2)
	}
	with open('data.json', 'a') as f:
		json.dump(data, f)
	#shape = [(rand/2, 2.0), (-rand/2, 2.0), (-rand/2, 2.0-(rand/2)), 
			#(-rand/2+(rand/3), 2.0-(rand/2)), (-rand/2+rand/3, 2.0-rand),
			#(rand/2-rand/3, 2.0-rand), ((rand/2-rand/3), 2.0-rand/2), 
			#(rand/2, 2-rand/2)]
	print("rand: " , rand)
	print(data)
	
def l_room_generation():
	#generate random to insert into the shape generation
	rand = randint(30,80)/10
	#print("lroom: " + rand+ "")
	top = Shape.create(type=PrimitiveShape.CUBOID,
                     size=[rand/2, 0.05, 2.0],
                     color=[0.8, 0.8, 0.8],
		      		 position=[0.0, 2.0, 1.0],
                     static=True, respondable=False)
	middle_left = Shape.create(type=PrimitiveShape.CUBOID,
	              				size=[0.05, rand, 2.0],
                      			color=[0.8, 0.8, 0.8],
		      					position=[-(rand/4), 2-(rand/2), 1.0],
                      			static=True, respondable=False)
	middle_right = Shape.create(type=PrimitiveShape.CUBOID,
                      				size=[0.05, rand/2, 2.0],
                      				color=[0.8, 0.8, 0.8],
		      						position=[rand/4,2-(rand/4), 1.0],
                      				static=True, respondable=False)
	bottom_right = Shape.create(type=PrimitiveShape.CUBOID,
                      				size=[rand/2, 0.05, 2.0],
                      				color=[0.8, 0.8, 0.8],
		      						position=[rand/2, 2-(rand/2), 1.0],
                      				static=True, respondable=False)
	right = Shape.create(type=PrimitiveShape.CUBOID,
                       	size=[0.05, rand/2, 2.0],
                       	color=[0.8, 0.8, 0.8],
		      			position=[(3/4*rand), 2-(3/4*rand), 1.0],
                       	static=True, respondable=False)
	bottom = Shape.create(type=PrimitiveShape.CUBOID,
	              		size=[rand, 0.05, 2.0],
                        color=[0.8, 0.8, 0.8],
		      			position=[rand/4, 2-rand, 1.0],
                        static=True, respondable=False)
    #points recorded starting from top right corner- anti clockwise round
	#data = {}
  #data['shape'] = []  	
	data = {
		'shape': 'lroom',
    	'point1': (rand/4, 2.0),
    	'point2': (-rand/4, 2.0),
    	'point3': (-rand/4, 2-rand),
    	'point4': (-rand/4 + rand, 2.0-rand),
    	'point5': (-rand/4+rand, 2-rand/2),
    	'point6': (rand/4, 2-rand/2)
	}
	with open('data.json', 'a') as f:
		json.dump(data, f)
	print(data)
	#shape = [(rand/4, 2.0), (-rand/4, 2.0), (-rand/4, 2-rand), (-rand/4 + rand, 2.0-rand),
	#		(-rand/4+rand, 2-(rand/2)), (rand/4, 2-rand/2)]
	print("rand is: " , rand)
	#print(shape)

#Selects the "type" of room to create at random
random_value = randint(1,3)
print(random_value)
if random_value == 1:
	rectangular_room_generation()
	#myData={room}
	#sim.writeCustomDataBlock(sim.handle_scene,"myTag",sim.packTable(myData))
elif random_value == 2:
	t_room_generation()
else:
	l_room_generation()
	
def getch():
	fd = sys.stdin.fileno()
	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)
	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
	
	try:
		while 1:
			try:
				c = sys.stdin.read(1)
				break
			except IOError:
				pass
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
	if len(c)>0:
		return ord(c)
	return -1

while True:
	got=getch()
	if got == 27:
		print('exiting nicely')
		pr.stop()
		pr.shutdown()
	else:
		pr.step()
	time.sleep(0.01)
#	#done = True
#print('Done ...')
#input('Press enter to finish ...')
#pr.stop()  # Stop the simulation
#pr.shutdown()  # Close the application
