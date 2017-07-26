#!/usr/bin/env python2.7

import random
import math
import global_variables
import copy
import networkx as nx

#checks the drones connectivityi, it returns -1 if the network is not connected

def create_drones_graph(individual):
    """ Create a graph using networkx using the links among drones
        Individual is the list of drones     
    """
    G = nx.Graph() # the graph of drones
    for i in individual:
        i.neighbordrones = list()
        G.add_node(i.id)
        
    for i in individual:
        for j in individual:
            if (i.id != j.id) and (j.id > i.id):
                x = (i.node_x - j.node_x) * (i.node_x - j.node_x)
                y = (i.node_y - j.node_y) * (i.node_y - j.node_y)
                distance = math.sqrt(x + y) # cal
                if distance <= 250:
                    i.neighbordrones.append(j.id)
                    j.neighbordrones.append(i.id)
                    G.add_edge(j.id,i.id) 
    return G

def check_graph_connectivity(G):
    """
        It checks the connectivity of the network using networkx module
    """
    return nx.is_connected(G)

def fault_tolerenace(G):
    """ It evaluate the fault tolerance of the network of drones. It is calculated as
    the lenght of the set of drones that disconnect the network 
    """
    return len(nx.minimum_node_cut(G))
        
def check_drones_conectivity(individual):
	""" It evaluates the connectivity of drones"""
	connections = 0
	#j = 0
     	
	# to initiate list of neighbors and to give an id 
	for h in individual:
		h.neighbordrones= list()
	#	j = j + 1

	# check out connections
	for i in individual:
		for j in individual:
			if (i.id != j.id) and (j.id > i.id):
				x = (i.node_x - j.node_x) * (i.node_x - j.node_x)
				y = (i.node_y - j.node_y) * (i.node_y - j.node_y)
				distance = math.sqrt(x + y)
				if distance <= 250:
					connections = connections + 1 # update connections
					i.neighbordrones.append(j.id)
					j.neighbordrones.append(i.id)

	# check out connected network condition
	list_connect = list()
	list_connect.append(individual[0].id)
	for k in individual[0].neighbordrones:
		for l in individual:
			if l.id != 0 and l.id == k:
				for z in l.neighbordrones:
					if z in list_connect:
						pass
					else:
						list_connect.append(z)
	
	if len(list_connect) < len(individual):
		return -1 # if not connected network
	else:
		return connections			

def victims_coverage(individual):
    """ It calculates the number of victims covered by the drones"""
    current_victims = list()
    list_covered = list()
    list_covered_total = list()
    coverage = 0

    if global_variables.partial == 1:
        current_victims = copy.deepcopy(global_variables.list_partial_victims) 	
    else:
        current_victims = copy.deepcopy(global_variables.list_victims)
        
    for i in individual:
		i.coveredvictims = list()
  
	# check out connectivity
    for i in individual:
        for j in current_victims:
            x = (i.node_x - j.node_x) * (i.node_x - j.node_x)
            y = (i.node_y - j.node_y) * (i.node_y - j.node_y)
            distance = math.sqrt(x + y)
            if distance <= 250:
                if j.id in list_covered:
                    continue
                else:
                    #if len(i.coveredvictims) < global_variables.num_max_connections:
                    list_covered.append(j.id)
                    i.coveredvictims.append(j.id)

    for i in individual:    
        list_covered_total.extend(i.coveredvictims)    
        
    coverage = len(list_covered_total)    
    #quality = global_variables.victim_points * len(list_covered_total) + connections * global_variables.coverage_points
    return coverage

def victims_connections(individual):
	""" It calculates the number of possible connections between drones and victims"""
	current_victims = list()
	connections = 0

	if global_variables.partial == 1:
		current_victims = copy.deepcopy(global_variables.list_partial_victims) 	
	else:
		current_victims = copy.deepcopy(global_variables.list_victims)

	# initialize drone's covered arrays
	for i in individual:
		i.coveredvictims = list()

	# check out connectivity
	for i in individual:
		for j in current_victims:
			x = (i.node_x - j.node_x) * (i.node_x - j.node_x)
			y = (i.node_y - j.node_y) * (i.node_y - j.node_y)
			distance = math.sqrt(x + y)
			if distance <= 250:
				connections = connections + 1				
	return connections

def evaluate_coverage(individual):
    quality = 0
    G = create_drones_graph(individual)
    if check_graph_connectivity(G) == True:
        quality = victims_coverage(individual)
    else:
        quality = -1
    return quality, 

def evaluate_tolerance(individual):
    quality = 0
    G = create_drones_graph(individual)
    if check_graph_connectivity(G) == True:
        quality = fault_tolerenace(G)
    else:
        quality = -1
    return quality, 

def evaluate_redundancy(individual):
    quality = 0
    G = create_drones_graph(individual)
    if check_graph_connectivity(G) == True:
        quality = victims_connections(individual)
    else:
        quality = -1
    return quality, 
    
def evaluate_multiobjective(individual):
    coverage = 0.0
    tolerance = 0.0
    redundancy = 0.0
    G = create_drones_graph(individual)
    if check_graph_connectivity(G) == True:
        coverage = victims_coverage(individual)
        tolerance = fault_tolerenace(G)
        redundancy = victims_connections(individual)
    else:
        coverage = -1
        tolerance = -1
        redundancy = -1
    return coverage, tolerance, redundancy

def evaluate_weighted(individual):
    quality = 0
    G = create_drones_graph(individual)
    if check_graph_connectivity(G) == True:
        q1 = victims_coverage(individual)
        q2 = fault_tolerenace(G)
        q3 = victims_connections(individual)
        quality = (q1*1000) + (q2*100) + q3 
    else:
        quality = -1
    return quality, 
    
def evaluate(individual):
    """ It evaluates the quality of a potential solution. It first checks out whether it is a valid solution or not and then it calculates the quality"""
    quality = 0
    quality = check_drones_conectivity(individual)
    if quality > 0:
        quality = victims_coverage(individual) 
    return quality, 

total = 0 # global variable that counts the number of individuals that meet the connectivity condition 
# initiate the drones' positions

def init(num_drones):
	accomplished = 0
	global total
	while accomplished == 0:
		list_drones =  list()
		for i in range (0, num_drones):
			x_cor = random.random() * 1000
			y_cor = random.random() * 1000 
			list_drones.append(global_variables.Drone(i,x_cor,y_cor))
		if check_drones_conectivity(list_drones) < 0:
			accomplished = 0
		else:
			accomplished = 1
			total = total + 1
			print "we got one, total number %d" % total			
	return list_drones

def init_geometric(num_drones):
    r = 250
    list_drones =  list()
    for i in xrange(num_drones):
        if i ==0:
            list_drones.append(global_variables.Drone(i,random.uniform(0, 1000),random.uniform(0, 1000)))
        else:
            drone = random.randint(0,len(list_drones) - 1)
            if random.randint(0,10) > 5: #flip a coin 
                x = list_drones[drone].node_x + random.uniform(0,r)  # add
                if x > 1000:
                    x = 1000
            else:
                x =  list_drones[drone].node_x - random.uniform(0,r) # substract
                if x < 0:
                    x = 0
            aux = x - list_drones[drone].node_x
            delta_y = math.sqrt((r*r) - (aux*aux))
            if random.randint(0,10) > 5:    
                y = list_drones[drone].node_y + random.uniform(0, delta_y)
                if y > 1000:
                    y = 1000
            else:
                y = list_drones[drone].node_y - random.uniform(0, delta_y)
                if y < 0:
                    y = 0
            list_drones.append(global_variables.Drone(i,x,y))
    return list_drones


def init_grid(num_drones):
	list_x = list()
	list_y = list()
	accomplished = 0
	global total
	for i in range(0,1100,150):
		list_x.append(i)
		list_y.append(i)
	while accomplished == 0:
		list_drones = []
		for i in range (0, num_drones):
			ind_x = random.randint(0,len(list_x)-1)
			ind_y = random.randint(0,len(list_y)-1)
			x_cor = list_x[ind_x]
			y_cor = list_y[ind_y]
			list_drones.append(global_variables.Drone(total,x_cor,y_cor))
		if check_drones_conectivity(list_drones) < 0:
			accomplished = 0
		else:
			accomplished = 1
			total = total + 1
			print "we got one, total number %d" % total
	return list_drones

def init_modified(list_drones_genetic, num_drones):
    """ this function is used if different number of drones is used during the initial deployment
    and the adaptation to the real conditions"""
    
    accomplished = 0
    global total
    while accomplished == 0:
        list_drones =  list()
        for j in list_drones_genetic:
            x = j.node_x
            y = j.node_y
            list_drones.append(global_variables.Drone(total,x,y))
            
        for i in range (len(list_drones_genetic), num_drones):
            x_cor = random.random() * 1000
            y_cor = random.random() * 1000 
            list_drones.append(global_variables.Drone(total,x_cor,y_cor))
        if check_drones_conectivity(list_drones) < 0:
            accomplished = 0
        else:
            accomplished = 1
            total = total + 1
            print "we got one, total number %d" % total
            
    return list_drones

