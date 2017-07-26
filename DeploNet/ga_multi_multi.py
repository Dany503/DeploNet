import quality
import global_variables
import genetic
import random
import copy


from deap import base
from deap import creator
from deap import tools

import matplotlib.pyplot as plt

print_all = 1 # global variable to use print 
#n_individuals = 100  

#we create the attribute fitness, This is general for all individuals
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

#we create the inividual
creator.create("Individual", list, fitness=creator.FitnessMax)

# POP_1, POP_2, POP_3
toolbox1 = base.Toolbox() # global toolbox
toolbox1.register("attr_bool", quality.init_geometric, global_variables.num_drones)

# initilize
toolbox1.register("individual", tools.initIterate, creator.Individual, toolbox1.attr_bool)
toolbox1.register("population", tools.initRepeat, list, toolbox1.individual)
toolbox1.register("evaluate_coverage", quality.evaluate_coverage)
toolbox1.register("evaluate_tolerance", quality.evaluate_tolerance)
toolbox1.register("evaluate_redundancy", quality.evaluate_redundancy)
#toolbox1.register("evaluate_weighted", quality.evaluate_weighted)

# crossover
toolbox1.register("mate", tools.cxTwoPoint)
# mutation
toolbox1.register("mutate", genetic.shift_mutation)
# selection
toolbox1.register("select", tools.selTournament, tournsize=3)
#toolbox.register("select", tools.selRoulette) 
# elitism
toolbox1.register("select2", tools.selBest) 

# POP_4
creator.create("Multiobjective", base.Fitness, weights=(1.0,1.0,1.0))
creator.create("Individual_Multiobjetive", list, fitness=creator.Multiobjetive)
toolbox2 = base.Toolbox() # global toolbox
toolbox2.register("attr_bool", quality.init_geometric, global_variables.num_drones)

# initilize
toolbox2.register("individual", tools.initIterate, creator.Individual, toolbox1.attr_bool)
toolbox2.register("population", tools.initRepeat, list, toolbox1.individual)
toolbox2.register("evaluate_weighted", quality.evaluate_multiobjective)

# crossover
toolbox2.register("mate", tools.cxTwoPoint)
# mutation
toolbox2.register("mutate", genetic.shift_mutation)
# selection
toolbox2.register("select", tools.selTournamentDCD)
toolbox2.register("select2", tools.selNSGA2)
# elitism
 

class Population(object):
    """ It generates a population objetc with the following attributes:
           pop: list of individuals
           pxover = crossover probability
           pmut = mutation probability
           per_xover = percentage of the offspring created by crossover
           per_mut = percentage of the offspring created by mutation
           per_elit = percentage of the offspring created by elitism
           n_individuals = number of individuals forming  the population
           id_population = identification of the population
           function = function used to evaluated the individuals (fitness function)
           best_current_fitness = best fitness obtained so far in the evolution
           covergence_generation = generation that obtains the best solution so far in the evolution
           xover_offspring = list of offspring individuals for crossover operation
           mut_offspring = lisf of offspring individuals for mutation operation
           elit_offspring = list of offspring individuals for elitism
           fits = list of fitness of the current population
           best_list = list that stores the best individual of each iteration
           toolbox = toolbox of deap
    """
    def __init__(self, pop, pxover, pmut, per_xover, per_mut, per_elit, n_individuals, id_population, function, toolbox, multiobjective):
        self.pop = pop 
        self.pxover = pxover 
        self.pmut = pmut
        self.per_xover = per_xover
        self.per_mut = per_mut
        self.per_elit = per_elit
        self.n_individuals = n_individuals
        self.id = id_population
        self.function = function
        self.toolbox = toolbox
        self.multiobjective = multiobjective
        self.best_current_fitness = None
        self.convergence_generation = None
        self.xover_offspring = list()
        self.mut_offspring = list()
        self.elit_offspring = list()
        self.offspring = list()
        self.fits = list()
        self.best_list = list()
        
    def initial_evaluation(self):
        """ This method executes the initial evaluation of the invidual of the population"""
        fitnesses = list(map(self.function, self.pop)) # create list of fitness
        for ind, fit in zip(self.pop, fitnesses):
            ind.fitness.values = fit # add the fitness to the individual
        if print_all == 1:
            print "Individuos evaluados %d" % len(self.pop)
            
    def crossover(self):
        """ This method executes the crossover operation"""
        self.xover_offspring = self.toolbox.select(self.pop, int(self.n_individuals*self.per_xover)) # crossover selection
        self.xover_offspring = list(map(self.toolbox.clone, self.xover_offspring))
        selected_individuals = len(self.xover_offspring)
        if print_all == 1:
            print "Individuals for crossover: ", selected_individuals
        if self.n_individuals % 2 != 0:
            print "Number of individuals for crossing must be divisible by 2"
            print "Current number of individual for crossing is %d" % self.n_individuals 
        for child1, child2 in zip(self.xover_offspring[::2], self.xover_offspring[1::2]):
            if random.random() < self.pxover: # crossover probability
                self.toolbox.mate(child1, child2)
                #toolbox.mate2(child1, child2)
                del child1.fitness.values # removing fitness
                del child2.fitness.values
                
    def mutation(self):
        """ This method executes the mutation operation"""
        self.mut_offspring = self.toolbox.select(self.pop, int(self.n_individuals*self.per_mut))
        selected_individuals = len(self.mut_offspring)
        if print_all == 1:
            print "Individuals for mutation: %d" % selected_individuals
        for mutant in self.mut_offspring: # mutation probability
            if random.random() < self.pmut:
                #toolbox.mutate(mutant)
                self.toolbox.mutate(mutant,0.1)
                del mutant.fitness.values
    
    def elitism(self):
        """ This method applies elitism"""
        self.elit_offspring = self.toolbox.select2(self.pop, int(self.n_individuals* self.per_elit))
        selected_individuals = len(self.elit_offspring)
        if print_all == 1:
            print "Individuals for elitism: %d" % selected_individuals

    def select_migration_elitism(self, rate):
        """ This method select the invidividual that migrate using elitism. It receives as input the % rate"""
        mig = tools.selBest(self.pop, int(self.n_individuals * rate))
        mig2 = copy.deepcopy(mig)
        return mig2
    
    def select_migration_random(self, rate):
        """ This method select the invidividual that migrate. It receives as input the % rate"""
        mig = list()
        for i in range(int(self.n_individuals * rate)):
            index = random.randint(0,len(self.pop)-1)
            mig.append(copy.deepcopy(self.pop[index]))
        return mig
    
    def insert_migration(self, migrants):
        """ This method inserts the new individual in the current population"""
        # IMPORTANT CHECK, when different fitness functions are used, the individuals
        # have to be evaluated under the new fitness function
        self.pop = self.pop + migrants
            
    def update_population(self):
        """ This methods update the current population
            1) evaluate the new offspring
            2) update population
            3) update the list of fitness
        """
        self.offspring = self.xover_offspring + self.mut_offspring + self.elit_offspring        
        invalid_ind = [ind for ind in self.offspring if not ind.fitness.valid]
        fitnesses = map(self.function, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        if print_all == 1:
            print "Evaluados %d individuos" % len(invalid_ind)
            
        # update the population
        self.pop[:] = self.offspring
        self.fits = [ind.fitness.values[0] for ind in self.pop]
    
    def update_population_nsga2(self):
        """ This methods update the current population
            1) evaluate the new offspring
            2) select next population using NSGAII
            3) update the list of fitness
        """
        self.offspring = self.xover_offspring + self.mut_offspring
        invalid_ind = [ind for ind in self.offspring if not ind.fitness.valid]
        fitnesses = map(self.function, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        self.pop = self.toolbox.select2(self.pop + self.offspring, len(self.pop))
        self.fits = [ind.fitness.values[0] for ind in self.pop]
        
    def update_best(self, generation):
        """ this method updates: 
        the list of best individuals throughout the evolution
        the best individual found so far in the evolution
        the convergence generation
        """
        ind = tools.selBest(self.pop, 1)[0]
        self.best_list.append(ind.fitness.values)
        if ind.fitness.values > self.best_current_fitness:
            self.best_current_fitness = ind.fitness.values
            self.convergence_generation = generation
        
    def statistics(self):
        """ This method calculates the statistics over the current list of fitness"""
        length = len(self.pop)
        mean = sum(self.fits) / length
        sum2 = sum(x*x for x in self.fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print "****STATISTICS****"
        print "Min %s" % min(self.fits)
        print "Max %s" % max(self.fits)
        print "Avg %s" % mean
        print "Std %s" % std
    
    def plot_best(self):
        plt.figure()
        plt.plot(self.best_list)
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        name = str(self.id_population)+".png"
        plt.savefig(name)        

class Results (object):
    """ the objects of this class store the results of the evolution"""
    def __init__(self,best, best_fitness, best_evolution, identification, generation):
        self.best = best
        self.best_fitness = best_fitness
        self.best_evolution = best_evolution
        self.id = identification
        self.convergence_generation = generation

def migration_ring(population_list, migration_rate):
    """ This function implements the ring migration scheme as described in 
    http://www.pohlheim.com/Papers/mpga_gal95/gal2_5.html#Multiple Populations
    The individuals are transferred between directionally adjacent subpopulations
    """
    mig_list = list()
    for p in population_list:
        mig_list.append(p.select_migration_elitism(migration_rate))
        #mig_list.append(p.select_migration_random(migration_rate))            
    # ring migration scheme
    for i, j in enumerate(population_list[0:-1]):
        j.pop = j.pop + mig_list[i+1]
        
    population_list[-1].pop = population_list[-1].pop + mig_list[0]
                
def migration_mesh(population_list, migration_rate, size):
    """ This fucntion implements the mesh migration ring as described in
    http://www.pohlheim.com/Papers/mpga_gal95/gal2_5.html#Multiple Populations
    The individuals may migrate from any subpopulation to another.
    """
    mig_list = list()
    for p in population_list:
        mig_list= mig_list + p.select_migration_elitism(migration_rate) # all migrant together
        #mig_list+=p.select_migration_random(migration_rate)
    
    for p in population_list:
        m_aux_list = list()
        for m in range(0, int(migration_rate*size)-1):
            m_aux_list.append(mig_list[random.randint(0,len(mig_list)-1)])
        p.pop = p.pop + m_aux_list

def migration_all_to_one(population_list, migration_rate):
    """ this function implements all_to_one migration, the best individuals of each isolated population
    go to the last population, which implement the weighting fitness function"""
    
    for i in range(0,len(population_list)-2): # the last population is always the one tha applies the weighting function
        population_list[-1].pop = population_list[-1].pop + population_list[i].select_migration_elitism(migration_rate)
        
def ga_multi_population():
    """ this function implement the multi-objective genetic algorithm"""
    random.seed() # seed for random numbers
    
    n_individuals = 60
    NGEN = 80 # number of generations is the same for all the populations   
    # we create the random lisf of inividual for each population
    pop1 = toolbox1.population(n_individuals) # focused on coverage 
    pop2 = toolbox1.population(n_individuals) # focused on fault tolerance
    pop3 = toolbox1.population(n_individuals) # focused on connections
    pop4 = toolbox2.population(n_individuals) # weighted 
    
    # layout of the offspring for each population
    per_xover = 0.5
    per_mut = 0.4
    per_elit = 0.1
    
    #per_xover1 = 0.8
    #per_mut1 = 0.1
    #per_elit1 = 0.1
    
    #per_xover2 = 0.7
    #per_mut2 = 0.2
    #per_elit2 = 0.1

    #per_xover3 = 0.6
    #per_mut3 = 0.3
    #per_elit3 = 0.1

    #per_xover4 = 0.5
    #per_mut4 = 0.4
    #per_elit4 = 0.1
    
    # probabilities of crossover and mutation
    p_xover= 0.6
    p_mut = 0.1
    
    #p_xover1= 0.6
    #p_mut1 = 0.05
    
    #p_xover2= 0.5
    #p_mut2 = 0.1
    
    #p_xover3= 0.4
    #p_mut3 = 0.15
    
    #p_xover4= 0.5
    #p_mut4 = 0.2
    
    function1 = toolbox1.evaluate_coverage
    function2 = toolbox1.evaluate_tolerance
    function3 = toolbox1.evaluate_redundancy
    #function1 = toolbox.evaluate_weighted
    #function2 = toolbox.evaluate_weighted
    #function3 = toolbox.evaluate_weighted
    function4 = toolbox2.evaluate_weighted
    
    # IMPORTANT CHECK per_xover + per_mut + per_elet = 1
    #pop, pxover, pmut, per_xover, per_mut, per_elit, n_individuals, id
    Pop1 = Population(pop1, p_xover, p_mut, per_xover, per_mut, per_elit, n_individuals, 1, function1, toolbox1, 0)
    Pop2 = Population(pop2, p_xover, p_mut, per_xover, per_mut, per_elit, n_individuals, 2, function2, toolbox1, 0)
    Pop3 = Population(pop3, p_xover, p_mut, per_xover, per_mut, per_elit, n_individuals, 3, function3, toolbox1, 0)
    Pop4 = Population(pop4, p_xover, p_mut, per_xover, per_mut, per_elit, n_individuals, 4, function4, toolbox2, 1)

    migration_rate = 0.1
    
    population_list = list() # this list stores all the populations
    population_list.append(Pop1)
    population_list.append(Pop2)
    population_list.append(Pop3)
    population_list.append(Pop4)
    
    migration = True
    print "START EVALUATION"
    
    
    
    # initial evaluations
    for p in population_list:
        p.initial_evaluation()
    
    # evolving the generations
    for g in range(NGEN):
        print "-- GENERATION %d --" % g
        
        if g%5 == 0 and migration == True:
            #migration_ring(population_list, migration_rate)
            #migration_mesh(population_list, migration_rate, n_individuals)
            migration_all_to_one(population_list, migration_rate)
        else:
            for p in population_list:
                p.crossover()
                p.mutation()
                if p.multiobjective ==0:
                    p.elitism()
                    p.update_population()
                    p.update_best(g)
                else:
                    p.update_population_nsga2()
                update_pareto()
                #p.statistics()            
            
    print "-- END OF EVOLUTION --"
    
    result_list = list()
    for p in population_list:
        best_sol = tools.selBest(p.pop, 1)[0] # best individual
        best_fit = best_sol.fitness.values[0] # best fitness
        best_list = p.best_list # best list of fitnesses
        result_list.append(Results(best_sol, best_fit,best_list,p.id, p.convergence_generation))
    
    return result_list
         
