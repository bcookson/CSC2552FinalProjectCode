import math
import datetime

def stress_function(x):
    return x

train_delay_file = open('subway-delay-clean1.csv')

next(train_delay_file)

train_pops = open('subway_ridership.csv')
next(train_pops)

valid_days = ['Monday','Tuesday','Wednesday','Thursday','Friday']

line_map = {'YU':'1','BD':'2','SHP':'4','SRT':'3'}
station_map = {}
car_map = {}

station_map_file = open('stations_map.csv')
for l in station_map_file:
    station_map[l.split(',')[0]] = l.split(',')[1].strip()

pops = {}
pop_max = 0

total_scores = {}


for l in train_pops:
    pops[l.split(',')[0] + "-" + l.split(',')[1]] = int(l.split(',')[2])
    pop_max = max(pop_max, int(l.split(',')[2]))

pops = {x:pops[x]/pop_max for x in pops}

for l in train_delay_file:
    l = l.split(',')
    if(l[2] in valid_days):
        station = (line_map[l[8].strip()] + "-" + station_map[l[3].strip()]).strip()
        delay = int(l[5])
        day = l[0]
        stress = stress_function(delay)*pops[station]
        if day in total_scores: total_scores[day] += stress
        else: total_scores[day] = stress

w = open("stress.csv","w+")
for day in sorted(total_scores.items(),key=lambda x: x[1]):
    w.write("{},{}\n".format(day[0],day[1]))
w.close()