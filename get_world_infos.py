import json
from datetime import datetime

flag = 'INFO'

subreddit_list = []
f = open("subreddit_list.csv")
for name in f:
    name = name.strip()
    subreddit_list.append(name)
f.close()

domain_dict = {}
f = open("get_domain_rankings/full_domain_biases.csv")
for line in f:
    line = line.strip().split(",")
    if flag == 'BIAS':
        domain_dict[line[0]] = line[1]
    else:
        domain_dict[line[0]] = line[2]
f.close()

info_rankings =  {'VERY-HIGH':0,'HIGH':1,'MOSTLY-FACTUAL':2,'MIXED':3,'LOW':4,'VERY-LOW':5}
bias_rankings = {'FAR-RIGHT':-3,'RIGHT':-2,'RIGHT-CENTER':-1,'CENTER':0,'LEFT-CENTER':1,'LEFT':2,'FAR-LEFT':3}

ranking_dict = info_rankings
if flag == 'BIAS': ranking_dict = bias_rankings

world_files = ["../domains/world_{}_submissions".format(x) for x in subreddit_list] + ["../domains/world_{}_comments".format(x) for x in subreddit_list]

world_date_dict = {}
for file in world_files:
    f = open(file)
    for line in f:
        line = line.split(";")
        d = line[0]
        l = line[1].replace("'",'"').replace("None",'"None"')
        l = json.loads(l)
        if d in world_date_dict:
            world_date_dict[d] = world_date_dict[d] + l
        else:
            world_date_dict[d] = l
    f.close()
    
world_date_dict = {x:[y for y in world_date_dict[x] if y in domain_dict] for x in world_date_dict}
world_score_dict = {}
for date in world_date_dict:
    world_score_dict[date] = 0
    score = 0
    for domain in world_date_dict[date]:
        if domain in domain_dict and domain_dict[domain] in ranking_dict:
            if flag == 'COUNT':
                score += 1
            else:
                score += ranking_dict[domain_dict[domain]]
    if flag == 'COUNT':
        world_score_dict[date] += score
    else:   
        world_score_dict[date] += score/len(world_date_dict[date])

w = open("world_info_scores.csv","w+")
for day in world_score_dict:
    w.write("{},{}\n".format(day,world_score_dict[day]))
w.close()