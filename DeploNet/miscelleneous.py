#!/usr/bin/env python2.7

import smtplib

def find_max(listofitems):
    """ Returns the index of the max in a list"""
    maximum = max(listofitems)
    for i, j in enumerate(listofitems):
        if j == maximum:
            index = i
            break
    return index

def get_positions(list_drones):
	""" Returns a list which contains the positions of drones """
	positions = []
	for i in list_drones:
		positions.append((int(i.node_x), int(i.node_y)))
	return positions

def statistics(list_best):
    """ this function calculates the statistic over a list of individuals"""
    length = len(list_best)
    mean = sum(list_best) / length
    sum2 = sum(x*x for x in list_best)
    std = abs(sum2 / length - mean**2)**0.5
    global_max = max(list_best) 
    index = find_max(list_best)
    minimum = min(list_best)
    stat = {'maximum': global_max, 'minimum': minimum, 'mean': mean, 'std': std, 'index': index}
    return stat

def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("danypracticas2016@gmail.com", "danypracticas")
 
    msg = "Simulations finished"
    server.sendmail("danypracticas2016@gmail.com", "d.gutierrez.reina@gmail.com", msg)
    server.quit()
