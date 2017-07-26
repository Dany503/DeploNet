#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import operator
import random
import global_variables
import quality
import numpy
import math

from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Particle", list, fitness=creator.FitnessMax, speedx=list, speedy = list, 
    smin=None, smax=None, best=None, record = list, record_best = list, identificador = int)
# velocidad de la particula, velocidad minima, velocidad maxima, y mejor estado en el que ha estado

identificador_global = 0

def generate(size, pmin, pmax, smin, smax):
	print "Generate the Particles"
	global identificador_global
	part = creator.Particle(quality.init(size))
	part.speedx = [random.uniform(smin, smax) for _ in range(size)]
	part.speedy = [random.uniform(smin, smax) for _ in range(size)]
	part.smin = smin
	part.smax = smax
	part.identificador = identificador_global
	identificador_global = identificador_global + 1
	return part

#this function gets the xi and y coordinates for the drones and put them in a list
def get_cor(drones):
	list_x = []
	list_y = []
	for i in drones:
		list_x.append(i.node_x)
		list_y.append(i.node_y)
	return list_x, list_y 

#this function put the new x and y coordinates in the drones objects
def put_cor(list_x, list_y, drones):
	k = 0
	for i, j in zip(list_x, list_y):
		drones[k].node_x = i
		drones[k].node_y = j
		k = k + 1
	return drones

def cal_dif(best, part):
	list_x_best, list_y_best = get_cor(best)
	list_x_part, list_y_part = get_cor(part)

	print "best x %s" % list_x_best
	print "part x %s" % list_x_part
	
	dif_x = map(operator.sub, list_x_best, list_x_part)
	dif_y = map(operator.sub, list_y_best, list_y_part)
	return dif_x, dif_y

# we have to check that the drones do not get out of the scenario
def updateParticle(part, best, phi1, phi2):
	print "UPDATE PARTICLES POSITIONS"
	print "len part %d" % len(part)
	print "phi1 %d" % phi1
	print "phi2 %d" % phi2
	u1 = list()
	u2 = list()
	for i in range(len(part)):
		u1.append(random.uniform(0,phi1))
		u2.append(random.uniform(0,phi2))
	dif_local_x, dif_local_y = cal_dif(part.best, part)
	dif_global_x, dif_global_y = cal_dif(best, part)

	print "dif local x %s" % dif_local_x
	print "dif global x %s" % dif_global_x
	print "dif local y %s" % dif_local_y
	print "dif global y %s" % dif_global_y
	print "u1 %s" % u1
	print "u2 %s" % u2

	v_u1_x = map(operator.mul, u1, dif_local_x)
	v_u2_x = map(operator.mul, u2, dif_global_x)
	v_u1_y = map(operator.mul, u1, dif_local_y)
	v_u2_y = map(operator.mul, u2, dif_global_y)

	part.speedx = list(map(operator.add, part.speedx, map(operator.add, v_u1_x, v_u2_x)))
	part.sppedy = list(map(operator.add, part.speedy, map(operator.add, v_u1_y, v_u2_y)))
	
	for i, speed in enumerate(part.speedx):
		if speed < part.smin:
			part.speedx[i] = part.smin
		elif speed > part.smax:
			part.speedx[i] = part.smax
	
	for i, speed in enumerate(part.speedy):
		if speed < part.smin:
			part.speedy[i] = part.smin
		elif speed > part.smax:
			part.speedy[i] = part.smax
	j= 0
	for i in range(len(part)): # we update all the positions of the drones
		print "x old %f" % part[i].node_x
		print "y old %f" % part[i].node_y
		part[i].node_x = part[i].node_x + part.speedx[j]
		part[i].node_y = part[i].node_y + part.speedy[j]
		j = j + 1
		print "x new %f" % part[i].node_x
		print "y new %f" % part[i].node_y
	print "--------------------------------------------------------"

	#part[:] = list(map(operator.add, part, part.speed))

toolbox = base.Toolbox()
toolbox.register("particle", generate, size=global_variables.num_drones, pmin=0, pmax=1000, smin=0, smax=15) # size= 2 es porque la funcion a optimizar tiene dos parametros
toolbox.register("population", tools.initRepeat, list, toolbox.particle)
toolbox.register("update", updateParticle, phi1=5.0, phi2=5.0) # phi1 y phi2 tiene que ver con el peso que se le da a la mejor posicion obtenida por la particula y la mejor posicion de la mejor particula
toolbox.register("evaluate", quality.evaluate)

def pso_algorithm():
	pop = toolbox.population(n=5)
	GEN = 5
	best = None
	list_max = []

	for part in pop:
		part.best = creator.Particle(part)
		part.best.fitness.values = -1, # iniciamos con un fitness negativo

	for g in range(GEN):
		print "-----------------------GENERATION %f -----------------------" % g
		for part in pop:
			part.fitness.values = toolbox.evaluate(part) # evaluamos todas las particulas
			part.record.append(part.fitness.values)
			part.record_best.append(part.best.fitness.values)
			print "**** particle %d" % part.identificador
			print "**** FITNESS OBTAINED %f" % part.fitness.values

			if part.best.fitness < part.fitness: # check the best particle position
				print "IMPROVED LOCAL"
				print "++> best local stored %f" % part.best.fitness.values
				part.best = creator.Particle(part)
				part.best.fitness.values = part.fitness.values
				print "++> new best local %f" % part.best.fitness.values
				x_l, y_l = get_cor(part.best)
				print "++> coordinates of the best local %s" % x_l
				x_p, y_p = get_cor(part)
				print "++> coordinates of the particle %s" % x_p
			else: 
				print "dont improved"
				print "best local stored %f" % part.best.fitness.values
				x_l, y_l = get_cor(part.best)
				print "++> coordinates of the best local %s" % x_l
				x_p, y_p = get_cor(part)	
				print "++> coodinates of the particle %s" % x_p

			if not best or best.fitness < part.fitness: # check the best particle
				if best:
					print "--> the best global fitness stored %f" % best.fitness.values
				best = creator.Particle(part)
				best.fitness.values = part.fitness.values
				print "--> the best global fitness %f" % best.fitness.values
				list_max.append(part.fitness.values) # store the best particles so far
			
			toolbox.update(part, best)
	
	for part in pop:
		print "Particle %d" % part.identificador
		print "fitnes for each iteration"
		print part.record
		print "the best local fitness"
		print part.record_best

	print "?????? best fitness %f" % best.fitness.values
	return best, best.fitness.values[0] 
        # Gather all the fitnesses in one list and print the stats
        #logbook.record(gen=g, evals=len(pop), **stats.compile(pop))
        #print(logbook.stream)

