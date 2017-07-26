#!/usr/bin/env python2.7

import quality
import global_variables
import copy
import random

from deap import base
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", quality.init_geometric, global_variables.num_drones_genetic)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_bool)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#toolbox.register("evaluate", quality.evaluate)
toolbox.register("evaluate_weighted", quality.evaluate_weighted)
toolbox.register("mate", tools.cxTwoPoint)
#toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.10)
#toolbox.register("mutate2", swap_mutation)

#toolbox.register("mutate", tools.mutGaussian,0, 1000, indpb=0.10)
#toolbox.register("select1", tools.selRoulette)
toolbox.register("select1", tools.selTournament, tournsize=3)
toolbox.register("select2", tools.selBest)


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
    old_individual = copy.deepcopy(individual) #save copy
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
                        x = x - shift
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
    G = quality.create_drones_graph(individual)      
    q = quality.check_graph_connectivity(G)
    if (q == False):
        return old_individual
    return individual

toolbox.register("mutate2", swap_mutation)
toolbox.register("mutate3", shift_mutation)

# this is the actual implementation of the genetic algorithm
def genetic_algorithm():
    random.seed()
    list_max = list()
    convergence_generation = 0
    best_current_fitness  = 0
    
    global_variables.partial = 1
    
    #n_individual = 60
    n_individual = 60
    #n_individual = 10
    CXPB, MUTPB, NGEN = 0.6, 0.05, 150
    
    # initial population
    pop = toolbox.population(n= n_individual)
    
    # Evaluate the entire population
    #fitnesses = list(toolbox.map(toolbox.evaluate_weighted, pop))
    fitnesses = list(map(toolbox.evaluate_weighted, pop))
    #fitnesses = toolbox.map(quality.evaluate_weighted, [i[0] for i in pop])
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    best_current_fitness = max(fitnesses)
    print("  Evaluated %i individuals" % len(pop))
    per_xover = global_variables.crossover_value
    per_mut = global_variables.mutation_value
    per_elit = 0.1
    
    
    # Begin the evolution
    for g in range(NGEN):
        print("-- Generation %i --" % g)
        
        offspring = list()
        # Select the next generation individuals
        offspring_crossover = toolbox.select1(pop, int(n_individual*per_xover))
        offspring_mutation = toolbox.select1(pop, int(n_individual*per_mut))
        offspring_elit = toolbox.select2(pop, int(n_individual*per_elit))
        # Clone the selected individuals
        
        offspring_crossover = list(map(toolbox.clone, offspring_crossover))
        offspring_mutation = list(map(toolbox.clone, offspring_mutation))
        offspring_elit = list(map(toolbox.clone, offspring_elit))
        
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
                del mutant.fitness.values

        offspring = offspring_crossover + offspring_mutation + offspring_elit # we add elitism

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        #fitnesses = toolbox.map(quality.evaluate_weighted, invalid_ind)
        #fitnesses = toolbox.map(toolbox.evaluate_weighted, invalid_ind)
        fitnesses = map(toolbox.evaluate_weighted, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        
        pop[:] = offspring
        fits = [ind.fitness.values[0] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
        ind = tools.selBest(pop, 1)[0]
        list_max.append(ind.fitness.values)
        if ind.fitness.values > best_current_fitness:
            best_current_fitness = ind.fitness.values
            convergence_generation = g

    print("-- End of (successful) evolution --")
    best_ind = tools.selBest(pop, 1)[0]
    return best_ind, max(fits), pop, list_max, convergence_generation
		