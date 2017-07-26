#!/usr/bin/env python2.7

import random
import global_variables 

def generate_victim_positions(num_victims):
	""" It selects randomly the positions of victims"""
	random.seed(10)
	#global list_victims
	for i in range (0, num_victims):
		x_cor = random.random() * 1000
		y_cor = random.random() * 1000
		global_variables.list_victims.append(global_variablesVictim(i,x_cor,y_cor))

# victims's positions based on paper DESE		
def generate_victim_positions_traces():
    """ used in paper DESE and applied soft computing"""
    #global list_victims
    global_variables.list_victims = list()
    print "Generate the positions of victims"
    x = open("x_positions.txt",'r')
    y = open("y_positions.txt", 'r')
    ident = 0
    for i, j in zip(x, y):
        global_variables.list_victims.append(global_variables.Victim(ident,float(i),float(j)))
        ident = ident + 1
        #print ident
    
def partial_knowledge_generation(knowledge):
    """ generates a new list of victims based on knowledge parameter and the complete list of victims"""
    #global list_victims
    #global list_partial_victims
    global_variables.list_partial_victims = list()         
    new_number_victims = float(knowledge) * len(global_variables.list_victims)
    new_number_victims = int(new_number_victims) # it must be an integer
    while len(global_variables.list_partial_victims) < new_number_victims:
        new_victim = global_variables.list_victims[random.randint(0,(new_number_victims -1))]
        if new_victim in global_variables.list_partial_victims:
		pass
        else:
		global_variables.list_partial_victims.append(new_victim)

def copy_drones_positions():
	""" copies drones positions from the file to be used in local optimization"""
	list_drones = []
	x = open("x_drones_positions.txt",'r')
	y = open("y_drones_positions.txt", 'r')
	ident = 0
	for i, j in zip(x, y):
		list_drones.append(global_variables.Drone(ident,float(i),float(j)))
		ident = ident + 1
	return list_drones

