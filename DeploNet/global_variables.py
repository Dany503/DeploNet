#!/usr/bin/env python2.7

list_victims = list()
list_partial_victims = list()
num_drones = 18 # number of drones
num_drones_genetic = 18
num_max_connections = 15 # maximum number of clients that a drone can handle
victim_points = 100 # points per victim
#coverage_points = float(victim_point / (num_drones * num_max_connections))
coverage_points = float(victim_points) / (num_drones * num_drones * 125)
partial = 1 # should be one in case that K<1
crossover_value = 0
mutation_value = 0
m_rate = 5


class Drone(object):
    """ It defines a drone"""
    def __init__(self, id_node, x, y):
        """ it initializes a drone"""
        self.id = id_node # drone's id
        self.node_x = x # drone's coordinates
        self.node_y = y
        self.previous_x = 0.0 # previous drone's coordinate, used by hill climbing algorithm
        self.previous_y = 0.0
        self.coveredvictims = list() # array of victims covered
        self.neighbordrones = list() # array of drones covered
        self.angle = 0.0 # defines moving direction, used by hill climbing algorithm
        self.speed = 0.0
        self.x_list = list()
        self.y_list = list()
        self.positions = list() # list of positions of the drones		
      
class Victim(object):
    """ It defines a victim"""
    def __init__(self, id_victim, x, y):
        """ it initializes a victim"""
        self.id = id_victim # victim's id
        self.node_x = x # victim's coordinates
        self.node_y = y


