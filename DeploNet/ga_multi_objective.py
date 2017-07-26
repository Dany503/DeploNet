#!/usr/bin/env python2.7

import quality
import global_variables
import copy
import random

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,1.0,1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", quality.init_geometric, global_variables.num_drones_genetic)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_bool)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#toolbox.register("evaluate", quality.evaluate)
toolbox.register("evaluate_weighted", quality.evaluate_multiobjective)
toolbox.register("mate", tools.cxTwoPoint)
#toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.10)
#toolbox.register("mutate2", swap_mutation)

#toolbox.register("select1", tools.selTournamentDCD)
toolbox.register("select1", tools.selRoulette)
toolbox.register("select", tools.selNSGA2)


# This function swap the coordinates of the drones
def swap_mutation(individual, probability):
	for j in range(0, len(individual)):
		if (random.random() <= probability): 
			x = individual[j].node_x
			y = individual[j].node_y
			# make a swap between coordinates x and y
			individual[j].node_x = y
			individual[j].node_y = x
	return individual

# this function shift a given quantity the coordinates of a drone
def shift_mutation(individual, probability):
	old_individual = copy.deepcopy(individual)
	shift_max = 5 # maximum shift
	shift = random.randint(0,shift_max)

	for j in range(0, len(individual)):
		if (random.random() <= probability): # mutate
			x = individual[j].node_x
			y = individual[j].node_y
			if(random.randint(0,1)==0): # add shift
				if(random.randint(0,1)== 0): # affect x
					x = x + shift
					if x > 1000:
						x = x- shift
				else:
					y = y + shift
					if y > 1000:
						y = y - shift

			else: #sub shift
				if(random.randint(0,1) == 0):
					x = x - shift
					if x < 0:
						x = x + shift
				else:
					y = y - shift
					if y < 0:
						y = y + shift

			individual[j].node_x = x
			individual[j].node_y = y
	q = quality.check_drones_conectivity(individual)
	if (q == -1):
		return old_individual

	return individual

toolbox.register("mutate2", swap_mutation)
toolbox.register("mutate3", shift_mutation)
toolbox.register("mutate4", tools.mutGaussian)

# this is the actual implementation of the genetic algorithm
def genetic_algorithm():
    random.seed()
    
    global_variables.partial = 1
    
    n_individual = 100
    #n_individual = 240
    #n_individual = 10
    CXPB, MUTPB, NGEN = 0.6, 0.05, 80
    
    # initial population
    pop = toolbox.population(n= n_individual)
    pareto = tools.ParetoFront() # create the pareto front
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate_weighted, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    pop = toolbox.select(pop, len(pop)) # to create the distance among individuals
    print("  Evaluated %i individuals" % len(pop))
    per_xover = global_variables.crossover_value
    per_mut = global_variables.mutation_value    
    pareto.update(pop)
    
    # Begin the evolution
    for g in range(NGEN):
        print("-- Generation %i --" % g)
        
        offspring = list()
        # Select the next generation individuals
        offspring_crossover = toolbox.select1(pop, int(n_individual*per_xover))
        offspring_mutation = toolbox.select1(pop, int(n_individual*per_mut))
        # Clone the selected individuals
        
        offspring_crossover = list(map(toolbox.clone, offspring_crossover))
        offspring_mutation = list(map(toolbox.clone, offspring_mutation))
        
        # crossover
        for child1, child2 in zip(offspring_crossover[::2], offspring_crossover[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        
        #mutation
        for mutant in offspring_mutation:
            if random.random() < MUTPB:
                #toolbox.mutate(mutant)
                toolbox.mutate3(mutant, 0.10)
                #toolbox.mutate4(mutant, mutant, 10, 0.10)
                del mutant.fitness.values

        offspring = offspring_crossover + offspring_mutation # we add elitism

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate_weighted, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        
        pop = toolbox.select(pop + offspring, len(pop))
        pareto.update(pop)
        

    print("-- End of (successful) evolution --")
    return pareto
		