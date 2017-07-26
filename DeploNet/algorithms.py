import quality
import global_variables

# return the quality obtained by a random deployment in the scenario
def random_deployment():
	list_drones = quality.init(global_variables.num_drones)
	global_variables.partial = 0
	result, = quality.evaluate(list_drones)
	return list_drones, result

def simple_grid():
	list_drones = quality.init_grid(global_variables.num_drones)
	global_variables.partial = 0
	result, = quality.evaluate(list_drones)
	return list_drones, result
