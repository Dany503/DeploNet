#!/usr/bin/env python2.7

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import global_variables 
import copy
import quality
import scenarios
import math
import pandas as pd

def positions_from_file(fil, num, k, nodes, UAVs, fig):
    """ It plots the solution"""
    #global list_victim
    #global list_partial_victims
    f = open(fil, 'r')
    scenarios.generate_victim_positions_traces()
    scenarios.partial_knowledge_generation(k)
    #print list_victims    
    
    list_drones = list()
    for line in f:
        fields = line.split(",")
        list_drones.append(global_variables.Drone(int(fields[0]), float(fields[1]), float(fields[2])))
    
    for i in list_drones:
        print i.id, i.node_x, i.node_y
    
    #CO= quality.evaluate_coverage(list_drones)
    #G= quality.create_drones_graph(list_drones)
    #print quality.check_graph_connectivity(G)
    #for i in list_drones:
    #    print i.neighbordrones
    
    #F= quality.evaluate_weighted(list_drones)
    CO= quality.evaluate_coverage(list_drones)
    print "coverage", CO            
    #FTO= quality.evaluate_tolerance(list_drones)
    #print FTO
    #RO= quality.evaluate_redundancy(list_drones)
    #print "redundancy", RO
        
    ground_x = list() # victims' positions
    ground_y = list()
    
    ground_x_covered = list() # victims' positions
    ground_y_covered = list()
    
    UAV_x = list() # drones' positions 
    UAV_y = list()
	
    UAV_ground_x = list() # links among drones and victims 
    UAV_ground_y = list()

    UAV_UAV_x = list() # links among drones
    UAV_UAV_y = list() 
	
    for i in global_variables.list_partial_victims:
        ground_x.append(i.node_x)
        ground_y.append(i.node_y)

    for j in list_drones:
        UAV_x.append(j.node_x)
        UAV_y.append(j.node_y)
    
    #print UAV_x, UAV_y
    #print ground_x, ground_y    
    UAV_ground_x, UAV_ground_y, ground_x_covered, ground_y_covered = plot_links(list_drones, 1)
    UAV_UAV_x, UAV_UAV_y = plot_links_drones(list_drones)
    #print UAV_ground_x

    # plotting drones connectivity
    #fig = plt.figure(figsize= (10,20), dpi = 300)
    ax1 = fig.add_subplot(4,2,num)
    #s1= ax1.scatter(ground_x, ground_y, c = 'y', label = "ground_nodes", marker = 'o')
    s1= ax1.scatter(UAV_x, UAV_y, c = 'r', label = "UAV", marker = 'x')
    for i in range (0, len(UAV_UAV_x)):
        if i % 2 == 0:
		x1 = UAV_UAV_x[i]
		x11 = UAV_UAV_x[i+1]
		y1 = UAV_UAV_y[i]
		y11 = UAV_UAV_y[i+1]
		ax1.plot([x1, x11],[y1, y11], 'r--', label = "UAV-UAV links", marker = '_')
    ax1.set_xlabel("X [m]", fontsize = 11)
    ax1.set_ylabel("Y [m]", fontsize = 11)
    ax1.axis([-50, 1050, -50, 1050])
    ax1.set_title(UAVs, fontsize = 12)
    ax1.grid("on")
    
    ax2 = fig.add_subplot(4,2,num+1)
    s2= ax2.scatter(ground_x, ground_y, c = 'c', label = "ground_nodes", marker = 'x')
    s3= ax2.scatter(ground_x_covered, ground_y_covered, c = 'm', label = "ground_nodes", marker = 'x')
    ax2.scatter(UAV_x, UAV_y, c = 'r', label = "UAV", marker = 'x')
    for i in range (0, len(UAV_ground_x)):
        if i % 2 == 0:
            x1 = UAV_ground_x[i]
            x11 = UAV_ground_x[i+1]
            y1 = UAV_ground_y[i]
            y11 = UAV_ground_y[i+1]
            ax2.plot([x1, x11],[y1, y11], 'g--', label = "UAV-ground links", marker = '_')
    ax2.set_xlabel("X [m]", fontsize = 11)
    ax2.set_ylabel("Y [m]", fontsize = 11)
    ax2.axis([-50, 1050, -50, 1050])
    ax2.set_title(nodes, fontsize = 12)
    ax2.grid("on")
	#l = ["unknown victims", "known victims", "drones"]
	#c = ['b', 'k', 'r', 'y', 'g', 'r']
	#m = ['o', 'o', 'o', '_', '_', '_']
    UAV_links = mlines.Line2D([], [], color='red', linestyle='--', label='Blue stars')
    GN_links = mlines.Line2D([], [], color='green', linestyle='--', label='Blue stars')
    if num==1:
        fig.legend(handles=[s1, s2, s3, UAV_links, GN_links], labels=['UAV', 'GN','Cov-GN','UAV-links','GN-links'], loc ='upper center')
    #fig.legend(handles=[s1, s2, s3, s4, s5, s6], ('UAV', 'GN','Cov-GN','UAV-links', 'GN-GN.links'), loc= 'upper right')
    fig.savefig("Positions.png")
	#plt.show() 

def positions(best_global, best_local, type_global, type_local):
	""" It plots the solution"""
	#global list_victim
	#global list_partial_victims
	
	list_x = [] # victims' positions
	list_y = []

	partial_x = [] # partial victim's positions
	partial_y = []

	best_global_x = [] # drones' positions after global optimization
	best_global_y = []

	best_local_x = [] # drones' positions after local optimization
	best_local_y = []

	x_links_global = [] # links among drones and victims after genetic algorithm 
	y_links_global = []

	x_links_local = [] # links among drones and victims after hill climbing
	y_links_local = []

	x_links_drones_global = [] # links among drones after genetic algorithm
	y_links_drones_global = [] 

	x_links_drones_local = [] # links among drones after hill climbing
	y_links_drones_local = []

	for i in global_variables.list_victims:
		list_x.append(i.node_x)
		list_y.append(i.node_y)

	for h in global_variables.list_partial_victims:
		partial_x.append(h.node_x)
		partial_y.append(h.node_y)

	for j in best_global:
		best_global_x.append(j.node_x)
		best_global_y.append(j.node_y)
	
	for k in best_local:
		best_local_x.append(k.node_x)
		best_local_y.append(k.node_y)

	x_links_global, y_links_global = plot_links(best_global, 1)
	x_links_local, y_links_local = plot_links(best_local, 0)

	x_links_drones_global, y_links_drones_global = plot_links_drones(best_global)
	x_links_drones_local, y_links_drones_local = plot_links_drones(best_local)

	# plotting drones connectivity
	fig = plt.figure(figsize= (13,10), dpi = 300)
	ax1 = fig.add_subplot(2,2,1)
	s1= ax1.scatter(list_x, list_y, c = 'y', label = "unknown victims", marker = 'o')
	s2= ax1.scatter(partial_x, partial_y, c = 'k', label = "known victims", marker = 'o')
	s3= ax1.scatter(best_global_x, best_global_y, c= 'r', label = type_global + " drones positions", marker = 'H', s = 80)
	for i in range (0, len(x_links_drones_global)):
		if i % 2 == 0:
			x1 = x_links_drones_global[i]
			x11 = x_links_drones_global[i+1]
			y1 = y_links_drones_global[i]
			y11 = y_links_drones_global[i+1]
			ax1.plot([x1, x11],[y1, y11], 'r--', label = type_global + " drones links", marker = '_')
	ax1.set_title(type_global + " algorithm solution: links among drones", fontsize = 12)
	ax1.set_xlabel("X [m]", fontsize = 11)
	ax1.set_ylabel("Y [m]", fontsize = 11)
	ax1.axis([-50, 1050, -50, 1050])

	ax2 = fig.add_subplot(2,2,2)
	ax2.scatter(list_x, list_y, c = 'y', label = "unknown victims", marker = 'o')
	ax2.scatter(partial_x, partial_y, c = 'k', label = "known drones", marker = 'o')
	ax2.scatter(best_local_x, best_local_y, c = 'r', label = type_local + " drones positions", marker = 'H', s = 80)
	for i in range (0, len(x_links_drones_local)):
		if i % 2 == 0:
			x1 = x_links_drones_local[i]
			x11 = x_links_drones_local[i+1]
			y1 = y_links_drones_local[i]
			y11 = y_links_drones_local[i+1]
			ax2.plot([x1, x11],[y1, y11], 'r--', label = type_local + " drones links", marker = '_')
	ax2.set_title(type_local + " solution: links among drones", fontsize = 12)
	ax2.set_xlabel("X [m]", fontsize = 11)
	ax2.set_ylabel("Y [m]", fontsize = 11)
	ax2.axis([-50, 1050, -50, 1050])

	# plotting links between drones and victims
	ax3 = fig.add_subplot(2,2,3)
	ax3.scatter(list_x, list_y, c= 'y', label = "unknown victims", marker = 'o')
	ax3.scatter(partial_x, partial_y, c= 'k', label = "known victims", marker = 'o')	
	ax3.scatter(best_global_x, best_global_y, c= 'r', label= type_global + " drones positions", marker = 'H', s= 80)
	for i in range (0, len(x_links_global)):
		if i % 2 == 0:
			x1 = x_links_global[i]
			x11 = x_links_global[i+1]
			y1 = y_links_global[i]
			y11 = y_links_global[i+1]
			ax3.plot([x1, x11],[y1, y11], 'y--', label = "genetic victims links", marker = '_')
	ax3.set_title(type_global + " algorithm solution: links among drones and victims", fontsize = 12)
	ax3.set_xlabel("X [m]", fontsize = 11)
	ax3.set_ylabel("Y [m]", fontsize = 11)
	ax3.axis([-50, 1050, -50, 1050]) 

	ax4 = fig.add_subplot(2,2,4)
	ax4.scatter(list_x, list_y, c= 'y', label = "unknown victims", marker = 'o')
	ax4.scatter(partial_x, partial_y, c= 'k', label = "known victims", marker = 'o')	
	ax4.scatter(best_local_x, best_local_y, c = 'r', label = type_local + " drones positions", marker = 'H', s = 80)
	for i in range (0, len(x_links_local)):
		if i % 2 == 0:
			x1 = x_links_local[i]
			x11 = x_links_local[i+1]
			y1 = y_links_local[i]
			y11 = y_links_local[i+1]
			ax4.plot([x1, x11],[y1, y11], 'g--', label= type_local + " victims links", marker = '_')
	ax4.set_title(type_local + " solution: links among drones and victims", fontsize = 12)
	ax4.set_xlabel("X [m]", fontsize = 11)
	ax4.set_ylabel("Y [m]", fontsize = 11)
	ax4.axis([-50, 1050, -50, 1050])
	#l = ["unknown victims", "known victims", "drones", "genetic victims links", "climbing victims links", "drones links"]
	l = ["unknown victims", "known victims", "drones"]
	c = ['b', 'k', 'r', 'y', 'g', 'r']
	m = ['o', 'o', 'o', '_', '_', '_']  
	fig.legend([s1, s2, s3],l, loc = 'upper left', numpoints = 1, ncol = 1, prop = {'size':11})
	fig.savefig("Positions.png")
	#plt.show()

def ground_nodes():
    """ It plots the solution"""
    
    k_values = [0.4, 0.6, 0.8, 1]
    list_x_global = [list() for i in range(len(k_values))]
    list_y_global = [list() for i in range(len(k_values))]
    scenarios.generate_victim_positions_traces()
    for i, k in enumerate(k_values):
        #list_victims_partical_victims = []
        #list_partial_victims = []
        list_x = list()
        list_y = list()        
        scenarios.partial_knowledge_generation(k)
        for j in global_variables.list_partial_victims:
            list_x.append(j.node_x)
            list_y.append(j.node_y)
        list_x_global[i].append(list_x)
        list_y_global[i].append(list_y)

    # plotting drones connectivity
    fig = plt.figure(figsize= (13,10), dpi = 300)
    ax1 = fig.add_subplot(2,2,1)
    ax1.scatter(list_x_global[0], list_y_global[0], c = 'k', label = "known victims", marker = 'o')	
    ax1.set_title("a) 50 ground nodes", fontsize = 12)
    ax1.set_xlabel("X [m]", fontsize = 11)
    ax1.set_ylabel("Y [m]", fontsize = 11)
    ax1.axis([-50, 1050, -50, 1050])
    ax1.grid(True)

    ax2 = fig.add_subplot(2,2,2)
    ax2.scatter(list_x_global[1], list_y_global[1], c = 'k', label = "known victims", marker = 'o')	
    ax2.set_title("b) 75 ground nodes", fontsize = 12)
    ax2.set_xlabel("X [m]", fontsize = 11)
    ax2.set_ylabel("Y [m]", fontsize = 11)
    ax2.axis([-50, 1050, -50, 1050])
    ax2.grid(True)
    
    ax3 = fig.add_subplot(2,2,3)
    ax3.scatter(list_x_global[2], list_y_global[2], c = 'k', label = "known victims", marker = 'o')	
    ax3.set_title("c) 100 ground nodes", fontsize = 12)
    ax3.set_xlabel("X [m]", fontsize = 11)
    ax3.set_ylabel("Y [m]", fontsize = 11)
    ax3.axis([-50, 1050, -50, 1050])
    ax3.grid(True)

    ax4 = fig.add_subplot(2,2,4)
    ax4.scatter(list_x_global[3], list_y_global[3], c = 'k', label = "known victims", marker = 'o')	
    ax4.set_title("d) 125 ground nodes", fontsize = 12)
    ax4.set_xlabel("X [m]", fontsize = 11)
    ax4.set_ylabel("Y [m]", fontsize = 11)
    ax4.axis([-50, 1050, -50, 1050])
    ax4.grid(True)
	
	  
    fig.savefig("Positions.png")
	

def evolution_global(bests, type_global):
	""" It plots the evolution of the best individual of the local optimization"""
	fig = plt.figure()
	ax1 = fig.add_subplot(1,1,1)
	ax1.plot(bests)
	ax1.set_title(type_global + " -> Evolution of the best individual")
	ax1.set_xlabel("N. Generation")
	ax1.set_ylabel("Fitness function")
	fig.savefig("Evolution_Global.png")
	#plt.show()

def evolution_local(bests, type_local):
	""" It plots the evolution of the best individual of the local optimization"""
	fig = plt.figure()
	ax1 = fig.add_subplot(1,1,1)
	ax1.plot(bests)
	if type_local == "probability":
		ax1.set_title("Evolution of probability")
		ax1.set_xlabel("N. Generation")
		ax1.set_ylabel("Probability")
		fig.savefig("Evolution_Probability.png")
	else:	
		ax1.set_title(type_local + " -> Evolution of the best individual")
		ax1.set_xlabel("N. Generation")
		ax1.set_ylabel("Fitness function")
		fig.savefig("Evolution_Local.png")
	#plt.show()

def plot_links(bests, part):
    """ It plots the links between the drones and the victims"""
    x_links = []
    y_links = []
    x_covered = list()
    y_covered = list()
    current_victims = []
    #global list_victims
    #global list_partial_victims
    if part == 1:
        current_victims = copy.deepcopy(global_variables.list_partial_victims)
    else:
        current_victims = copy.deepcopy(global_variables.list_victims)
    
    #print "len lista ground nodes", len(current_victims)
    for ind in bests:
        #print ind.coveredvictims
        for cov in ind.coveredvictims:
            for vic in current_victims:
                if vic.id == cov: # we found the victim
                    x_links.append(ind.node_x)
                    x_links.append(vic.node_x)
                    x_covered.append(vic.node_x)
                    y_links.append(ind.node_y)
                    y_links.append(vic.node_y)
                    y_covered.append(vic.node_y)
    return x_links, y_links, x_covered, y_covered	

def plot_links_drones(drones):
    """ It plots the links between the drones"""
    x_links = list()
    y_links = list()
    for ind in drones:
        for cov in ind.neighbordrones:
            for dron in drones:
                if (cov == dron.id) and ind.id > dron.id:
                    x_links.append(ind.node_x)
                    x_links.append(dron.node_x)
                    y_links.append(ind.node_y)
                    y_links.append(dron.node_y)
    return x_links, y_links	

def print_victim_positions():
	""" It prints out the victims' positions"""
	#global list_victims
	for i in global_variables.list_victims:
		print "node id %d" % i.id
		print i.node_x
		print i.node_y

def print_drones_connectivity(individual):
	""" It prints out the connectivity of drones"""
	for i in individual:
		for j in individual:
			if (i.id != j.id) and (j.id > i.id):
				x = (i.node_x - j.node_x) * (i.node_x - j.node_x)
				y = (i.node_y - j.node_y) * (i.node_y - j.node_y)
				distance = math.sqrt(x + y)
				if distance <= 250:
					print "Node: %d linked with Node: %d" % (i.id, j.id)

def print_drones_neighbors(individual):
	""" It prints out the connectivity of drones"""
	for i in individual:
		for j in i.neighbordrones:
			print "Node: %d linked with Node: %d" % (i.id, j)


def print_drones_data(best_individual, best_evolution, file_results):
    """ It prints out the coordinates of the drones and the fitness of the UAV network"""
    if(file_results):
        file_results.write("Id, X, Y")
        file_results.write('\n')
    for j in best_individual:
        if(file_results):
            cadena = str(j.id) + "," + str(j.node_x) + "," + str(j.node_y)
            file_results.write(cadena)
            file_results.write('\n')
        else:
            print "Id: %d, pos X: %f, pos Y: %f neighbor drones %d, N victims %d" % (j.id, j.node_x, j.node_y, len(j.neighbordrones), len
(j.coveredvictims))

    coverage = quality.evaluate_coverage(best_individual)
    tolerance = quality.evaluate_tolerance(best_individual)
    redudancy = quality.evaluate_redundancy(best_individual)
    file_results.write("Coverage \n")
    file_results.write(str(coverage))
    file_results.write('\n')
    file_results.write("Tolerance \n")
    file_results.write(str(tolerance))
    file_results.write('\n')
    file_results.write("Redundancy \n")
    file_results.write(str(redudancy))
    file_results.write('\n')
    file_results.write("Evolution of the best individual \n")
    file_results.write(str(best_evolution))
    file_results.write('\n')

def plot_movements(list_drones):
	fig = plt.figure()
	ax1 = fig.add_subplot(1,1,1)
	for i in list_drones:
		ax1.plot(i.x_list, i.y_list)
	ax1.set_title("Drones movements")
	ax1.set_xlabel("x")
	ax1.set_ylabel("y")
	fig.savefig("Moevements.png")	
 
def print_pareto(pareto, f):
    """ this function prints the pareto front in the input file"""
    f.write("Pareto front\n")
    for i in pareto:
        f.write(str(i.fitness.values[0]))
        f.write(",")
        f.write(str(i.fitness.values[1]))
        f.write(",")
        f.write(str(i.fitness.values[2]))
        f.write("\n")

def plot_pareto(archivos):
    fig = plt.figure(figsize= (12,16), dpi = 300)
    colors = ['m', 'b', 'k', 'r']
    markers = ['*','+','o','^']

    for i, fil in enumerate(archivos):
        print i
        datos= pd.read_csv(fil, dtype= float, names= ["CO", "FTO", "RO"], delimiter=",", skiprows= 1)
        if i ==0:        
            ax1 = fig.add_subplot(4,3,1)
            s1= ax1.scatter(datos["FTO"], datos['CO'], c = colors[i], label = "CO-FTO", marker = markers[i])
            ax1.set_ylim(40, 130)
            ax1.set_xlabel("FTO")
            ax1.set_ylabel("CO") 
            ax1.grid(True)
            ax2 = fig.add_subplot(4,3,2)
            s2= ax2.scatter(datos["RO"], datos['CO'], c = colors[i], label = "CO-RO", marker = markers[i])
            ax2.set_ylim(40, 130)
            ax2.set_xlabel("RO")
            ax2.set_ylabel("CO")
            ax2.grid(True)
            ax3 = fig.add_subplot(4,3,3)
            s3= ax3.scatter(datos["RO"], datos['FTO'], c = colors[i], label = "FTO-RO", marker = markers[i])
            ax3.set_xlabel("FTO")
            ax3.set_ylabel("RO")
            ax3.grid(True)
            
        if i ==1:
            ax1 = fig.add_subplot(4,3,4)
            s1= ax1.scatter(datos["FTO"], datos['CO'], c = colors[i], label = "CO-FTO", marker = markers[i])
            ax1.set_ylim(40, 130)
            ax1.set_xlabel("FTO")
            ax1.set_ylabel("CO")
            ax1.grid(True)            
            ax2 = fig.add_subplot(4,3,5)
            s2= ax2.scatter(datos["RO"], datos['CO'], c = colors[i], label = "CO-RO", marker = markers[i])
            ax2.set_ylim(40, 130)
            ax2.set_xlabel("RO")
            ax2.set_ylabel("CO")
            ax2.grid(True)
            ax3 = fig.add_subplot(4,3,6)
            s3= ax3.scatter(datos["RO"], datos['FTO'], c = colors[i], label = "FTO-RO", marker = markers[i])
            ax3.set_xlabel("FTO")
            ax3.set_ylabel("RO")
            ax3.grid(True)

        if i == 2:
            ax1 = fig.add_subplot(4,3,7)
            s1= ax1.scatter(datos["FTO"], datos['CO'], c = colors[i], label = "CO-FTO", marker = markers[i])
            ax1.set_ylim(40, 130)
            ax1.set_xlabel("FTO")
            ax1.set_ylabel("CO")   
            ax1.grid(True)
            ax2 = fig.add_subplot(4,3,8)
            s2= ax2.scatter(datos["RO"], datos['CO'], c = colors[i], label = "CO-RO", marker = markers[i])
            ax2.set_ylim(40, 130)
            ax2.set_xlabel("RO")
            ax2.set_ylabel("CO")
            ax2.grid(True)
            ax3 = fig.add_subplot(4,3,9)
            s3= ax3.scatter(datos["RO"], datos['FTO'], c = colors[i], label = "FTO-RO", marker = markers[i])
            ax3.set_xlabel("FTO")
            ax3.set_ylabel("RO")
            ax3.grid(True)

        if i == 3:
            ax1 = fig.add_subplot(4,3,10)
            s1= ax1.scatter(datos["FTO"], datos['CO'], c = colors[i], label = "CO-FTO", marker = markers[i])
            ax1.set_ylim(40, 130)
            ax1.set_xlabel("FTO")
            ax1.set_ylabel("CO") 
            ax1.grid(True)
            ax2 = fig.add_subplot(4,3,11)
            s2= ax2.scatter(datos["RO"], datos['CO'], c = colors[i], label = "CO-RO", marker = markers[i])
            ax2.set_ylim(40, 130)
            ax2.set_xlabel("RO")
            ax2.set_ylabel("CO")
            ax2.grid(True)
            ax3 = fig.add_subplot(4,3,12)
            s3= ax3.scatter(datos["RO"], datos['FTO'], c = colors[i], label = "FTO-RO", marker = markers[i])
            ax3.set_xlabel("FTO")
            ax3.set_ylabel("RO")
            ax3.grid(True)

def main():
    """
    fig = plt.figure(figsize= (10,20), dpi = 300)
    #files = ["best_1.txt", "best_08.txt", "best_06.txt", "best_04.txt"]
    files = ["best_1_14.txt", "best_08_14.txt", "best_06_14.txt", "best_04_14.txt"]
    num= [1,3,5,7]
    k = [1,0.8,0.6,0.4]
    nodes = [" 125 GNs ", " 100 GNs ", " 75 GNs ", " 50 GNs "]
    UAVs = "14 UAVs"
    for i, j in enumerate(num):
        print i
        print files[i]
        positions_from_file(files[i],j,k[i], nodes[i], UAVs, fig)
    #plots.ground_nodes()
    """
    archivos = ["mobjective_1_c08_m01.txt", "mobjective_1_c07_m02.txt", "mobjective_1_c06_m03.txt", "mobjective_1_c05_m04.txt"]
    plot_pareto(archivos)
    
if __name__ == "__main__": 
    main()

