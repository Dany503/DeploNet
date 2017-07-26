#!/usr/bin/env python2.7

import random
import sys
import math
import quality
import global_variables
import plots
import copy
import miscelleneous

def choose_one_direction(l2, max_speed):
	""" It selects a new moving direction for just one dorne"""
	random.seed()
	r = random.randint(0, len(l2))
	l2[r].angle = random.random() * 2 * math.pi
	l2[r].angle = random.random() * 2 * math.pi

def choose_directions(l2, max_speed):
	""" It selects a new moving direction for the drones"""
	random.seed()
	for drone in l2:
		drone.angle = random.random() * 2 * math.pi
		drone.speed = random.random() * max_speed

def choose_directions_single(l2, max_speed):
	""" It selects a new moving direction for a drone """
	random.seed()
	selected_drone = random.randint(0, (len(l2)-1))
	#print selected_drone
	l2[selected_drone].angle = random.random() * 2 * math.pi
	l2[selected_drone].speed = random.random() * max_speed
	return selected_drone

# we update the positions of just one drone
def update_drones_positions_single(l1, selected):
	l1[selected].previous_x = l1[selected].node_x
	l1[selected].previous_y = l1[selected].node_y
	l1[selected].node_x =  l1[selected].node_x +  l1[selected].speed * math.cos(l1[selected].angle)
	if  l1[selected].node_x > 1000 or  l1[selected].node_x < 0:
		 l1[selected].node_x = l1[selected].previous_x

	l1[selected].node_y = l1[selected].node_y +  l1[selected].speed * math.sin(l1[selected].angle)
	if  l1[selected].node_y > 1000 or  l1[selected].node_y < 0:
		l1[selected].node_y = l1[selected].previous_y

	
def update_drones_positions(l1, tabu):
	""" Update the positions of drones according to the their speed and moving direction"""
	for i in l1:
		# first save previous coordinates
		i.previous_x = i.node_x
		i.previous_y = i.node_y
		repeat = 0
		i.node_x = i.node_x + i.speed * math.cos(i.angle)
		if i.node_x > 1000 or i.node_x < 0:
			i.node_x = i.previous_x # limit of the scenario 

		i.node_y = i.node_y + i.speed * math.sin(i.angle)
		if i.node_y > 1000 or i.node_y < 0:
			i.node_y = i.previous_y # limit of the scenario

		if tabu == 1: # this will be for tabu algorithm, not implemented
			current_position = (int(i.node_x), int(i.node_y))
			for k in i.positions:
				if k == current_position:
					repeat = 1

		if repeat == 1:
			for j in l1: # all drones go back
				j.node_x = j.previous_x
				j.node_y = j.previous_y
		else:
			pass
			 #i.positions.append(current_position)

def step_back(l1, max_speed):
	""" This function place back the drones in the previous position and choose a new moving direction"""
	for i in l1:
		i.node_x = i.previous_x
		i.node_y = i.previous_y

	choose_directions(l1, max_speed)

# move back just one drone
def step_back_single(l1, selected, max_speed):
	""" This function place back the drone selected  in the previous position and choose a new moving direction"""
	l1[selected].node_x = l1[selected].previous_x
	l1[selected].node_y = l1[selected].previous_y
	selected = choose_directions_single(l1, max_speed)

	return selected

# we update the movememts of the drones
def update_movements(l1):
	""" update the movement list of each drones """ 
	for i in l1:
		i.x_list.append(i.node_x)
		i.y_list.append(i.node_y)

def hill_climbing(lista_drones, global_max):
	""" Hill climbing algorithm. It receives the list of drones and the global maximum"""
	
	#global partial
	#global_variables.partial = 1 # we evaluate hill climbing for the initial deployment problem
	global_variables.partial = 0	
	records = []
	records.append(global_max)
	first_max = global_max
	max_list = copy.deepcopy(lista_drones) # watch up
	max_speed = 10 # meters/seconds
	simulation_time = 50000 # seconds
	#choose_directions(lista_drones, max_speed) # here we selec the type of movement
	selected = choose_directions_single(lista_drones, max_speed)
	current_quality = 0.0
	prueba = lista_drones
	best_time = 0

	print "---------- START CLIMBING OPTIMIZATION ----------"

	for i in range (0, simulation_time):
		update_drones_positions(lista_drones, 0)
		#update_drones_positions_single(lista_drones, selected)
		current_quality = quality.evaluate(lista_drones)
		if (current_quality <= global_max):
			#selected= step_back_single(lista_drones, selected, max_speed)
			step_back(lista_drones, max_speed)
			#print "go back"
		else:
			print "----------------previous quality %f" % global_max
			global_max = current_quality
			#records.append(global_max)
			prueba = copy.deepcopy(lista_drones)
			print "----------------new quality %f" % global_max
			plots.print_drones_data(lista_drones, 0)
			best_time = i # we update the time at which we find the best solution so far
			print "-----------------------------------------------"
			print "-----------------------------------------------"
	
	# we print some information about how the positions are updated.
	print "quality before hill climbing %f" % first_max
	print "List of victims covered %s" % quality.calc_victims_covered(max_list) 
	print "total number of victims covered %d" % len(quality.calc_victims_covered(max_list))
	print "-------INITIAL POSITIONS----------------------"
	plots.print_drones_data(max_list, 0)
	print "----------------------------------------------"
	print "----------------------------------------------" 
	
	print "final quality hill climbing %f" % global_max
	print "List of victims covered %s" % quality.calc_victims_covered(prueba)
	print "total number of victims covered %d" % len(quality.calc_victims_covered(prueba))
	print "-------FINAL POSITIONS----------------------"
	plots.print_drones_data(prueba, 0)
	print "----------------------------------------------"
	print "----------------------------------------------"
	return prueba, records

# this is not implemented --> FUTURE WORK
def tabu_search(lista_drones, global_max):
	""" Tabu search algorithm. It receives the list of drones and the global maximum"""
	
	#global partial
	global_variables.partial = 1
	records = []
	records.append(global_max)
	movement_list = []
	tabu_list = [] # store the positions that have already visited
	first_max = global_max # we store the first maximum gloabal
	max_list = copy.deepcopy(lista_drones) # make a copy of the original postions of the drones
	max_speed = 10 # meters/seconds
	simulation_time = 10000 # seconds
	choose_directions(lista_drones, max_speed)
	current_quality = 0.0
	repetido = 0

	print "---------- START TABU SEARCH OPTIMIZATION ----------"

	for i in range (0, simulation_time):
		update_drones_positions(lista_drones, 0)
		current_quality = quality.evaluate(lista_drones)
		current_positions = miscelleneous.get_positions(lista_drones)
		if current_positions in tabu_list:
			repetido = repetido + 1
			print "REPETIDOOOOOOOOOOOOOOOOOOOOOOOO"
		else:
			if (current_quality <= global_max):
				step_back(lista_drones, max_speed)
				#print "go back"
			else:
				print current_positions
				update_movements(lista_drones)
				movement_list.append(current_positions)
				print "----------------previous quality %f" % global_max
				global_max = current_quality
				records.append(global_max)
				prueba = copy.deepcopy(lista_drones)
				print "----------------new quality %f" % global_max
				plots.print_drones_data(lista_drones, 0)
				print "-----------------------------------------------"
				print "-----------------------------------------------"
		tabu_list.append(current_positions)

	print "repetido %d" % repetido
	print "quality before tabu search %f" % first_max
	print "List of victims covered %s" % quality.calc_victims_covered(max_list) 
	print "total number of victims covered %d" % len(quality.calc_victims_covered(max_list))
	print "-------INITIAL POSITIONS----------------------"
	plots.print_drones_data(max_list, 0)
	print "----------------------------------------------"
	print "----------------------------------------------" 
	
	print "final quality tabu search %f" % global_max
	print "List of victims covered %s" % quality.calc_victims_covered(prueba)
	print "total number of victims covered %d" % len(quality.calc_victims_covered(prueba))
	print "-------FINAL POSITIONS----------------------"
	plots.print_drones_data(prueba, 0)
	print "----------------------------------------------"
	print "----------------------------------------------"
	plots.plot_movements(lista_drones)
	return prueba, records

# this is not implemented --> FUTURE WORK
def calculate_annealing_probability(temperature, current_quality, global_max):
	""" Calculate the probability of accepting worse solutions"""
	g1 = global_max
	c1 = current_quality
	aux =0
	print "temperature %f"  % temperature
	if temperature > 0:
		aux = (g1 - c1)/temperature
		print "aux %f" % aux
		probability = math.exp(-1* float(aux))
	else:
		probability = 0 # frozen solution
	if probability > 1:
		probability = 1
	print "PROBABILITY %f" % probability
	return probability

# this is not implemented --> FUTURE WORK
def update_annealing_temperature(temperature, deviation, simulation_time):
	#deviation = 1000
	Tmax = deviation / 0.0953
	Tmin = deviation / 4.651
	step = (Tmax - Tmin) / simulation_time
	new_temperature = temperature - step
	if new_temperature < 0:
		new_temperature = 0
	#print "tmax %f" % Tmax
	#print "tmin %f" % Tmin
	#print "simulation tome %d" % simulation_time
	#print  "new temperatue %f" % new_temperature
	return new_temperature 

# this is not implemented --> FUTURE WORK
def simulated_annealing(lista_drones, global_max, deviation):
	""" Simulated annealing algorithm. It receives the list of drones and the global maximum"""
	
	max_speed = 10 # meters/seconds
	simulation_time = 10000 # seconds
	global_variables.partial = 0
	temperature = float(deviation) / 0.0953

	records = []
	records_positions = []
	records_probability = []
	records_temperature = []
	records_aux = []

	global_max2, = global_max
	first_max = global_max
	max_list = copy.deepcopy(lista_drones) # watch up
	records.append(global_max2)
	records_positions.append(max_list)
	choose_directions(lista_drones, max_speed)

	print "---------- START SIMULATED ANNEALING OPTIMIZATION ----------"
	for i in range (0, simulation_time):
		update_drones_positions(lista_drones)
		current_quality,  = quality.evaluate(lista_drones)
		if current_quality <= global_max2 and current_quality > 0:
			probability = calculate_annealing_probability(temperature, current_quality, global_max2)
			print probability
			records_probability.append(probability)
			#records_aux.append(aux) 
			if (probability >= random.random()): # we should avoid non valid solutions
				print "----------------accepting a WORSE solution--------"
				print "----------------previous quality %f" % global_max2
				global_max2 = current_quality
				records.append(global_max2)
				prueba = copy.deepcopy(lista_drones)
				records_positions.append(prueba)
				print "----------------new quality %f" % global_max2
				plots.print_drones_data(lista_drones, 0)
				print "-----------------------------------------------"
				print "-----------------------------------------------"
			else:
				step_back(lista_drones, max_speed)
		else:
			if (current_quality > 0):
				print "----------------accepting a BETTER solution--------"
				print "----------------previous quality %f" % global_max2
				global_max2 = current_quality
				prueba = copy.deepcopy(lista_drones)
				records.append(global_max2)
				records_positions.append(prueba)
				print "----------------new quality %f" % global_max2
				plots.print_drones_data(prueba, 0)
				print "-----------------------------------------------"
				print "-----------------------------------------------"

		temperature = update_annealing_temperature(temperature, deviation, simulation_time)
		records_temperature.append(temperature)
		print "temperature %f" % temperature
	
	#plots.evolution_local(records_aux, "probability")
	index = miscelleneous.find_max(records)

	print "quality before simulated annealing %f" % first_max 
	print "List of victims covered %s" % quality.calc_victims_covered(max_list) 
	print "total number of victims covered %d" % len(quality.calc_victims_covered(max_list))
	print "-------INITIAL POSITIONS----------------------"
	plots.print_drones_data(max_list, 0)
	print "----------------------------------------------"
	print "----------------------------------------------" 
	
	print "final quality simulated annealing %f" % records[index]
	print "List of victims covered %s" % quality.calc_victims_covered(records_positions[index])
	print "total number of victims covered %d" % len(quality.calc_victims_covered(records_positions[index]))
	print "-------FINAL POSITIONS----------------------"
	plots.print_drones_data(records_positions[index], 0)
	print "----------------------------------------------"
	print "----------------------------------------------"
	return records_positions[index], records

