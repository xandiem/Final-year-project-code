from os.path import dirname, join, abspath
from pyrep import PyRep
from pyrep.robots.mobiles.youbot import YouBot
from pyrep.objects.shape import Shape
from pyrep.const import PrimitiveShape
from random import randint
import numpy as np
import json
import os
import sys    
import termios
import fcntl
import time
import pygame

#setup CoppeliaSim and launch the scene file
SCENE_FILE = join(dirname(abspath(__file__)), 'scene.ttt')
pr = PyRep()
pr.launch(SCENE_FILE, headless=False) 
pr.start()  # Start the simulation
json_dictionary = {}
agent = YouBot()
HEIGHT = 0.1 
#joystick setup

pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
pygame.init()
help(agent)
#function for joystick axis movement
#moves the robot accordingly

def joystick_movement():
	#pygame code to look for event occurrence
	for event in pygame.event.get():
		#print(event)
		#check to ensure its joystick axis motion(nothing else)
		if event.type == pygame.JOYAXISMOTION:
			pos_list = []
			pos_rearranged = []
			#get all axes of the joystick
			axes = joystick.get_numaxes()
			#go through x,y,z axes
			for i in range(axes-1):
				#get the joystick pos
				axis = joystick.get_axis(i)
				value = axis * (10)
				#add value to array
				pos_list.append(value)
			#rearrange axes as x is second parameter in velocity method
			xvalue = pos_list[0]
			if xvalue != 0.0:
				xvalue = -xvalue
			pos_rearranged.append(pos_list[1])
			pos_rearranged.append(xvalue)
			pos_rearranged.append(pos_list[2])
			print(pos_list)
			print(pos_rearranged)
			#set the velocity to list
			agent.set_base_angular_velocites(pos_rearranged)

def robot_set_position():	
	starting_pose = agent.get_2d_pose()
	agent.set_2d_pose(starting_pose)
	position_min, position_max = [0.5, 1.0, 0.1], [-0.5, -1.0, 0.1]
	pos = list(np.random.uniform(position_min, position_max))
	agent.set_position(pos)

def rectangular_room_generation():
	#generate random to insert into the shape generation	
	value_x = randint(50,80)/10
	value_y = randint(50,80)/10
	#store set of points
	top = Shape.create(type=PrimitiveShape.CUBOID,
                           size=[value_x, 0.05, HEIGHT],
                     color=[0.8, 0.8, 0.8],
                     position=[0.0, 2.0, HEIGHT/2],
                     static=True, respondable=True)
	left = Shape.create(type=PrimitiveShape.CUBOID,
                            size=[0.05, value_y, HEIGHT],
                     color=[0.8, 0.8, 0.8],
                     position=[-value_x/2, 2-(value_y/2), HEIGHT/2],
                     static=True, respondable=True)
	right = Shape.create(type=PrimitiveShape.CUBOID,
                             size=[0.05, value_y, HEIGHT],
                     color=[0.8, 0.8, 0.8],
                     position=[value_x/2, 2-(value_y/2), HEIGHT/2],
                     static=True, respondable=True)
	bottom = Shape.create(type=PrimitiveShape.CUBOID,
			size=[value_x, 0.05, HEIGHT],
                     color=[0.8, 0.8, 0.8],
                     position=[0.0, 2-(value_y), HEIGHT/2],
                     static=True, respondable=True)
	#call set robot to put robot in the room
	robot_set_position()
	json_dictionary.update({
		"scenario":{
                'points': [(value_x/2, 2.0),
                    	(-value_x/2, 2.0),
                    	(-value_x/2, 2-value_y),
                    	(-value_x/2, 2-value_y)],
		"robot_pose": agent.get_2d_pose().tolist(),
		"robot_pos" : agent.get_position().tolist()
		}
        })

def t_room_generation():
	#generate random to insert into the shape generation
	rand = randint(50,80)/10
	top = Shape.create(type=PrimitiveShape.CUBOID,
                           size=[rand, 0.05, HEIGHT],
                      color=[0.8, 0.8, 0.8],
                      position=[0.0, 2.0, HEIGHT/2],
                      static=True, respondable=True)
	top_left = Shape.create(type=PrimitiveShape.CUBOID,
                                size=[0.05, rand/2, HEIGHT],
                      color=[0.8, 0.8, 0.8],
                      position=[-rand/2, 2-(rand/4), HEIGHT/2],
                      static=True, respondable=True)
	top_right = Shape.create(type=PrimitiveShape.CUBOID,
                                 size=[0.05, rand/2, HEIGHT],
                      color=[0.8, 0.8, 0.8],
                      position=[rand/2,2-(rand/4), HEIGHT/2],
                      static=True, respondable=True)
	middle_left = Shape.create(type=PrimitiveShape.CUBOID,
                                   size=[rand/3, 0.05, HEIGHT],
                      color=[0.8, 0.8, 0.8],
                      position=[-(rand/3), 2-(rand/2), HEIGHT/2],
                      static=True, respondable=True)
	middle_right = Shape.create(type=PrimitiveShape.CUBOID,
                                    size=[rand/3, 0.05, HEIGHT],
                      color=[0.8, 0.8, 0.8],
                      position=[rand/3, 2-(rand/2), HEIGHT/2],
                      static=True, respondable=True)
	bottom_left = Shape.create(type=PrimitiveShape.CUBOID,
                                   size=[0.05, rand/2, HEIGHT],
                      color=[0.8, 0.8, 0.8],
                      position=[-rand/2+(rand/3), 2-(0.75*rand), HEIGHT/2],
                      static=True, respondable=True)
	bottom_right = Shape.create(type=PrimitiveShape.CUBOID,
                                    size=[0.05, rand/2, HEIGHT],
                      color=[0.8, 0.8, 0.8],
                      position=[rand/2-(rand/3), 2-(0.75*rand), HEIGHT/2],
                      static=True, respondable=True)
	bottom = Shape.create(type=PrimitiveShape.CUBOID,
                              size=[rand/3, 0.05, HEIGHT],
                      color=[0.8, 0.8, 0.8],
                      position=[0.0, 2-rand, HEIGHT/2],
                      static=True, respondable=True)
	robot_set_position()
	json_dictionary.update({
		"scenario":{
                	'points':[(rand/2, 2.0),
				(-rand/2, 2.0),
                    		(-rand/2, 2.0-rand/2),
                    		(-rand/2+(rand/3), 2.0-rand/2),
                    		(-rand/2+rand/3, 2.0-rand),
                    		(rand/2-rand/3, 2.0-rand),
                    		(rand/2-rand/3, 2.0-rand/2),
                    		(rand/2, 2-rand/2)],
			"robot_pose": agent.get_2d_pose().tolist(),
			"robot_pos" : agent.get_position().tolist()
			}
        })	

def l_room_generation():
	#generate random to insert into the shape generation
	rand = randint(50,80)/10
	top = Shape.create(type=PrimitiveShape.CUBOID,
                           size=[rand/2, 0.05, HEIGHT],
                     color=[0.8, 0.8, 0.8],
                     position=[0.0, 2.0, HEIGHT/2],
                     static=True, respondable=True)
	middle_left = Shape.create(type=PrimitiveShape.CUBOID,
                                   size=[0.05, rand, HEIGHT],
                     color=[0.8, 0.8, 0.8],
                     position=[-(rand/4), 2-(rand/2), HEIGHT/2],
                     static=True, respondable=True)
	middle_right = Shape.create(type=PrimitiveShape.CUBOID,
                                    size=[0.05, rand/2, HEIGHT],
                     color=[0.8, 0.8, 0.8],
                     position=[rand/4,2-(rand/4), HEIGHT/2],
                     static=True, respondable=True)
	bottom_right = Shape.create(type=PrimitiveShape.CUBOID,
                                    size=[rand/2, 0.05, HEIGHT],
                     color=[0.8, 0.8, 0.8],
                     position=[rand/2, 2-(rand/2), HEIGHT/2],
                     static=True, respondable=True)
	right = Shape.create(type=PrimitiveShape.CUBOID,
                             size=[0.05, rand/2, HEIGHT],
                     color=[0.8, 0.8, 0.8],
                     position=[(3/4*rand), 2-(3/4*rand), HEIGHT/2],
                     static=True, respondable=True)
	bottom = Shape.create(type=PrimitiveShape.CUBOID,
                              size=[rand, 0.05, HEIGHT],
                     color=[0.8, 0.8, 0.8],
                     position=[rand/4, 2-rand, HEIGHT/2],
                     static=True, respondable=True)
	robot_set_position()
	#points recorded starting from top right corner- anti clockwise round
	json_dictionary.update({
		"scenario":{
                	'points': [(rand/4, 2.0),
               			(-rand/4, 2.0),
                    		(-rand/4, 2-rand),
                    		(-rand/4 + rand, 2.0-rand),
                    		(-rand/4+rand, 2-rand/2),
                    		(rand/4, 2-rand/2)],
			"robot_pose": agent.get_2d_pose().tolist(),
			"robot_pos" : agent.get_position().tolist()
			
		}
        })
#Selects the "type" of room to create at random
random_value = randint(1,3)
if random_value == 1:
	rectangular_room_generation()
elif random_value == 2:
	t_room_generation()
else:
	l_room_generation()
#method for closing the programme properly
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

#main event loop
timestamp = 0
updates = []
	
while True:
	got=getch()
	if got == 27:
		print('exiting nicely')
		json_dictionary.update({
			"updates": updates
		})
		with open('data.json', 'a') as f:
			json.dump(json_dictionary, f, indent=2)
		pr.stop()
		pr.shutdown()
	else:
		pr.step()
		joystick_movement()
		timestamp += 1
		updates.append({
			"timestamp": timestamp,
			"curr_pose": agent.get_2d_pose().tolist()
		})
		
	time.sleep(0.01)

