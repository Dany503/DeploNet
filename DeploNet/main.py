import scenarios
import genetic
import ga_multi_population
import ga_multi_objective
import local
import plots
import miscelleneous
import global_variables
import quality
import algorithms
import pso
from deap import tools

import pandas as pd
#import networkx as nx
from optparse import OptionParser

# this function runs only the global search --> Initial deployment
def only_global(f, type_algorithm, knowledge, fil):
    #iterations_genetic = 120
    #iterations_genetic = 30 # how many times we run the algorithm
    iterations_genetic = 30
    iterations_pso = 1

    list_best_individuals = list() # list of best individuals
    list_best_fitness = list() # list of best fitnesses
    list_generations = list() # list of generations
    list_evolution_max = list()
    list_covergence = list()
    
    list_best_individuals_f1 = list() # list of best individuals
    list_best_fitness_f1 = list() # list of best fitnesses
    list_generations_f1 = list() # list of generations
    list_evolution_max_f1 = list()
    list_id_f1 = list()
    list_covergence_f1 = list()

    list_best_individuals_f2 = list() # list of best individuals
    list_best_fitness_f2 = list() # list of best fitnesses
    list_generations_f2 = list() # list of generations
    list_evolution_max_f2 = list()
    list_id_f2 = list()
    list_covergence_f2 = list()
    
    list_best_individuals_f3 = list() # list of best individuals
    list_best_fitness_f3 = list() # list of best fitnesses
    list_generations_f3 = list() # list of generations
    list_evolution_max_f3 = list()
    list_id_f3 = list()
    list_covergence_f3 = list()

    
    list_best_individuals_f4 = list() # list of best individuals
    list_best_fitness_f4 = list() # list of best fitnesses
    list_generations_f4 = list() # list of generations
    list_evolution_max_f4 = list()
    list_id_f4 = list()
    list_covergence_f4 = list()

    results_f1 = list()
    results_f2 = list()
    results_f3 = list()
    results_f4 = list()
    res = list()
    
    # scenario generation
    
    scenarios.generate_victim_positions_traces()
    scenarios.partial_knowledge_generation(knowledge)
    
    if type_algorithm == "genetic":
        for i in range (0, iterations_genetic):
            individual, fitness, generation, evol_max, convergence = genetic.genetic_algorithm()
            list_best_individuals.append(individual)
            list_best_fitness.append(fitness)
            list_generations.append(generation)
            list_evolution_max.append(evol_max)
            list_covergence.append(convergence)
            #print convergence
        
        print list_covergence
        stat = miscelleneous.statistics(list_best_fitness)
        stat_convergence = miscelleneous.statistics(list_covergence)
        data_results = pd.DataFrame([stat], columns = ["maximum", "minimum","mean", "std", "index"])
        data_convergence = pd.DataFrame([stat_convergence], columns = ["maximum", "minimum","mean", "std", "index"])          
        data_results.to_csv(fil+"results.csv") 
        data_convergence.to_csv(fil+"convergence.csv")           
        f.write("The best solution of population 1\n")        
        plots.print_drones_data(list_best_individuals[stat["index"]], list_evolution_max[stat["index"]], f)
    
    if type_algorithm == "pso":
        for i in range(0, iterations_pso):
            individual, fitness, = pso.pso_algorithm()
            list_best_individuals.append(individual)
            list_best_fitness.append(fitness)
    
    if type_algorithm == "multi_population":
        for i in range(0, iterations_genetic):
            res = ga_multi_population.ga_multi_population()
            for i,r in enumerate(res):
                if i ==0:
                    results_f1.append(r)
                if i ==1:
                    results_f2.append(r)
                if i ==2:
                    results_f3.append(r)
                if i ==3:
                    results_f4.append(r)
                    
    if type_algorithm == "multi_population":
        for r in results_f1:
            list_best_fitness_f1.append(r.best_fitness)
            list_best_individuals_f1.append(r.best)
            list_evolution_max_f1.append(r.best_evolution)
            list_id_f1.append(r.id)
            list_covergence_f1.append(r.convergence_generation)
        
        for r in results_f2:
            list_best_fitness_f2.append(r.best_fitness)
            list_best_individuals_f2.append(r.best)
            list_evolution_max_f2.append(r.best_evolution)
            list_id_f2.append(r.id)
            list_covergence_f2.append(r.convergence_generation)

        for r in results_f3:
            list_best_fitness_f3.append(r.best_fitness)
            list_best_individuals_f3.append(r.best)
            list_evolution_max_f3.append(r.best_evolution)
            list_id_f3.append(r.id)
            list_covergence_f3.append(r.convergence_generation)
        
        for r in results_f4:
            list_best_fitness_f4.append(r.best_fitness)
            list_best_individuals_f4.append(r.best)
            list_evolution_max_f4.append(r.best_evolution)
            list_id_f4.append(r.id)
            list_covergence_f4.append(r.convergence_generation)
    
        stat1 = miscelleneous.statistics(list_best_fitness_f1)
        stat2 = miscelleneous.statistics(list_best_fitness_f2)
        stat3 = miscelleneous.statistics(list_best_fitness_f3)
        stat4 = miscelleneous.statistics(list_best_fitness_f4)
    
        stat_convergence1 = miscelleneous.statistics(list_covergence_f1)
        stat_convergence2 = miscelleneous.statistics(list_covergence_f2)
        stat_convergence3 = miscelleneous.statistics(list_covergence_f3)
        stat_convergence4 = miscelleneous.statistics(list_covergence_f4)
    
        data_results = pd.DataFrame([stat1, stat2, stat3, stat4], columns = ["maximum", "minimum","mean", "std", "index"])	
        data_results.to_csv(fil+"results.csv")    
    
        data_convergence = pd.DataFrame([stat_convergence1, stat_convergence2, stat_convergence3, stat_convergence4], columns = ["maximum", "minimum","mean", "std", "index"])   
        data_convergence.to_csv(fil+"convergence.csv")
    
        f.write("The best solution of population 1\n")
        plots.print_drones_data(list_best_individuals_f1[stat1["index"]], list_evolution_max_f1[stat1["index"]], f)
        f.write("The best solution of population 2\n")
        plots.print_drones_data(list_best_individuals_f2[stat2["index"]], list_evolution_max_f2[stat2["index"]], f)
        f.write("The best solution of population 3\n")
        plots.print_drones_data(list_best_individuals_f3[stat3["index"]], list_evolution_max_f3[stat3["index"]], f)
        f.write("The best solution of population 4\n")
        plots.print_drones_data(list_best_individuals_f4[stat4["index"]], list_evolution_max_f4[stat4["index"]], f)
    
    if type_algorithm == "multi_objective":
        pareto_global = tools.ParetoFront()
        for i in range (0, iterations_genetic):
            pareto = ga_multi_objective.genetic_algorithm()
            pareto_global.update(pareto)
        plots.print_pareto(pareto_global, f)
    #plots.evolution_global(list_evolution_max[index], type_global)

# this function runs only the local search --> Adatation to the real conditions
def only_local(option, f):
    
    knowledge = 0
    iterations_local = 50 # number of trials
    scenarios.generate_victim_positions_traces()
    scenarios.partial_knowledge_generation(knowledge)
    
    list_best_individuals = list()
    list_best_fitness = list()
    list_evolution_max = list()
    list_best_time = list()

    for i in range(0,iterations_local):
        list_drones = quality.init(global_variables.num_drones) # random selection
        global_variables.partial = 1
        result_global = quality.evaluate(list_drones)
        global_variables.partial = 1 # we evaluate the hill climbing

        type_global = "Genetic Algorithm"
        if option == "Hill":
            type_local = "Hill Climbing"
            list_drones_climbing, records= local.hill_climbing(list_drones, result_global)
            list_best_individuals.append(list_drones_climbing)
            #list_best_time.append(best_time)
            q, = quality.evaluate(list_drones_climbing)
            list_best_fitness.append(q)		
            list_evolution_max.append(records)
            
    length = len(list_best_fitness)
    mean = sum(list_best_fitness) / length
    sum2 = sum(x*x for x in list_best_fitness)
    std = abs(sum2 / length - mean**2)**0.5
   
    index = miscelleneous.find_max(list_best_fitness)
		
    f.write(type_local)
    f.write("\n")	
    f.write("Results \n")
    f.write("Max, Min, Mean, Std \n")
    f.write(str(max(list_best_fitness)) + "," + str(min(list_best_fitness)) + "," + str(mean) + "," + str(std))
    f.write(str(list_best_fitness))	
    plots.print_drones_data(list_best_individuals[index], f)
    plots.evolution_local(list_evolution_max[index], type_local)
    plots.positions(list_drones, list_best_individuals[index], type_global, type_local)
    

# this is the complete approach --> Initial + adaptation
def global_plus_local(f):
    """ This function runs the whole approach global + local search """
    iterations_genetic = 1 # iterations genetic algorithm
    knowledge = 0.8 # level of knowledge 
    list_best_individuals = list() # to store the best individual of each genetic algorithm run
    list_best_fitness = list()# to store the best fitness of the best individual of each run
    list_generations = list() # to store the generations
    list_drones_climbing = list()
    list_evolution_max = list()
    type_global = "Genetic"
    type_local = "Hill Climbing"

    f.write(type_global)
    f.write("\n")
    scenarios.generate_victim_positions_traces()
    scenarios.partial_knowledge_generation(knowledge)

    for i in range (0, iterations_genetic):
        individual, fitness, generation, evol_max = genetic.genetic_algorithm()
        list_best_individuals.append(individual)
        list_best_fitness.append(fitness)
        list_generations.append(generation)
        list_evolution_max.append(evol_max)

    length = len(list_best_fitness)
    mean = sum(list_best_fitness) / length
    sum2 = sum(x*x for x in list_best_fitness)
    std = abs(sum2 / length - mean**2)**0.5
    
    f.write("Results \n")
    f.write("Max, Min, Mean, Std \n")
    f.write(str(max(list_best_fitness)) + "," + str(min(list_best_fitness)) + "," + str(mean) + "," + str(std))
    f.write("\n")
    
    global_max = max(list_best_fitness)
    index = miscelleneous.find_max(list_best_fitness)
    
    plots.print_drones_data(list_best_individuals[index], f)

    # LOCAL
    f.write(type_local)
    f.write("\n")
    #list_dr = quality.init_modified(list_best_individuals[index], global_variables.num_drones) # To simulate different number of drones for the initial deployment and for the adaptation to the real conditions
    #list_drones_climbing, records = local.hill_climbing(list_dr, list_best_individuals[index].fitness.values)
    list_drones_climbing, records = local.hill_climbing(list_best_individuals[index], list_best_individuals[index].fitness.values)
    f.write("Results \n")
    f.write(str(quality.evaluate(list_drones_climbing)))	
    plots.print_drones_data(list_drones_climbing, f)	
    plots.positions(list_best_individuals[index], list_drones_climbing, type_global, type_local)	
    plots.evolution_local(records, type_local)	
    plots.evolution_global(list_evolution_max[index], type_global)
    
    print "######### FIRST DEPLOYMENT STATISTICS ################"    
    print("  Min %s" % min(list_best_fitness))
    print("  Max %s" % max(list_best_fitness))
    print("  Avg %s" % mean)
    print("  Std %s" % std)

# to run random deployment
def ran_deployment(f):
    scenarios.generate_victim_positions_traces()
    iteractions =  50
    list_solutions = list()
    list_fitness = list()
    for i in range(0, iteractions):
        sol, fit = algorithms.random_deployment()
        list_solutions.append(sol)
        list_fitness.append(fit)
	

    length = len(list_fitness)
    mean = sum(list_fitness) / length
    sum2 = sum(x*x for x in list_fitness)
    std = abs(sum2 / length - mean**2)**0.5
    f.write("Results \n")
    f.write("Max, Min, Mean, Std \n")
    f.write(str(max(list_fitness)) + "," + str(min(list_fitness)) + "," + str(mean) + "," + str(std))
    f.write("\n")
    
    global_max = max(list_fitness)
    index = miscelleneous.find_max(list_fitness)
    plots.print_drones_data(list_solutions[index], f)
    f.write("random deployment")
    f.write("\n")

# to run grid deployment
def grid_deployment(f):
    scenarios.generate_victim_positions_traces()
    iteractions = 50
    list_solutions = list()
    list_fitness = list()
    for i in range(0, iteractions):
        sol, fit = algorithms.simple_grid()
        list_solutions.append(sol)
        list_fitness.append(fit)
    length = len(list_fitness)
    mean = sum(list_fitness) / length
    sum2 = sum(x*x for x in list_fitness)
    std = abs(sum2 / length - mean**2)**0.5
    
    f.write("Results \n")
    f.write("Max, Min, Mean, Std \n")
    f.write(str(max(list_fitness)) + "," + str(min(list_fitness)) + "," + str(mean) + "," + str(std))
    f.write("\n")
    
    global_max = max(list_fitness)
    index = miscelleneous.find_max(list_fitness)
    
    plots.print_drones_data(list_solutions[index], f)
    f.write("simple grid deployment")
    f.write("\n")

    
# here in the main, we select the type of algorithm we want to run
def main(): 
    #global_plus_local(f)
    datos = pd.read_excel('simulation_dronet.xlsx', 'Hoja1', index_col=None, na_values=['NA'])
    #f = open(fil+"resultados.txt", 'w+')
    f = open("resultados.txt", 'w+')
    for i, row in datos.iterrows():
        k = float(row['K']) # k level
        ty = str(row['type']) # type of algorithm
        fil = str(row['file']) # name of the file to write results
        global_variables.crossover_value = float(row['crossover']) # crossover layout
        global_variables.mutation_value = float(row['mutation']) # mutation layout
        #global_variables.m_rate = float(row['m_rate'])
        f = open(fil+".txt", 'w+')
        #print k, ty, fil, global_variables.crossover_value
        only_global(f, ty, k, fil)
        f.close()
    #only_global(f, "multi_objective", 1, None)
    #only_local("Hill", f)
    #ran_deployment(f)
    #grid_deployment(f)
    miscelleneous.send_email()
    #plots.ground_nodes()

if __name__ == "__main__": 
    usage = "usage: To set experiment options -option arg" # TODO, as future work some parameters will be given by the main
    parser = OptionParser()
    (options, args) = parser.parse_args()
    main()


