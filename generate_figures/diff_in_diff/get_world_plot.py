import json
from datetime import datetime

flag = 'INFO'
subway_flag = 'DELAY'

subreddit_list = []
f = open("../../subreddit_list.csv")
for name in f:
    name = name.strip()
    subreddit_list.append(name)
f.close()

domain_dict = {}
f = open("../../get_domain_rankings/full_domain_biases.csv")
for line in f:
    line = line.strip().split(",")
    if flag == 'BIAS':
        domain_dict[line[0]] = line[1]
    else:
        domain_dict[line[0]] = line[2]
f.close()

stress_dict = {}
f = open("../../stress.csv")
for line in f:
    line = line.strip().split(",")
    stress_dict[line[0]] = line[1]
f.close()

world_scores = {}
if flag == 'INFO':
    f = open("../../world_info_scores.csv")
elif flag == 'BIAS':
    f = open("../../world_bias_scores.csv")
elif flag == 'COUNT':
    f = open("../../world_count_scores.csv")
for line in f:
    line = line.strip().split(",")
    world_scores[line[0]] = line[1]
f.close()

weather_dict = {}
temp_dict = {}
f = open('../../toronto_weather.csv')
next(f)
for line in f:
    line = line.strip().split(',')
    d = line[4].replace('"',"")
    try:
        p = float(line[23].replace('"',''))
    except:
        p = 0.0
    weather_dict[d] = p
    try:
        t = float(line[13].replace('"',''))
    except:
        t = 0.0
    temp_dict[d] = t 

day_dict = {}
f = open("toronto_user_domains.csv")
for line in f:
    line = line.strip().split(";")
    day = line[0]
    d = json.loads(line[1])
    day_dict[day] = d


world_day_dict = {}
f = open("world_user_domains.csv")
for line in f:
    line = line.strip().split(";")
    day = line[0]
    d = json.loads(line[1])
    world_day_dict[day] = d

info_rankings =  {'VERY-HIGH':0,'HIGH':1,'MOSTLY-FACTUAL':2,'MIXED':3,'LOW':4,'VERY-LOW':5}
bias_rankings = {'FAR-RIGHT':-3,'RIGHT':-2,'RIGHT-CENTER':-1,'CENTER':0,'LEFT-CENTER':1,'LEFT':2,'FAR-LEFT':3}

ranking_dict = info_rankings
if flag == 'BIAS': ranking_dict = bias_rankings

day_aves = {}
day_counts = {}
for day in sorted(list(day_dict.keys())):
    for user in day_dict[day]:
        user_score = 0
        user_count = 0
        for domain in day_dict[day][user]:
            if domain in domain_dict and domain_dict[domain] in ranking_dict:
                user_score += ranking_dict[domain_dict[domain]]
                user_count += 1
        if user_count > 0:
            if flag == "COUNT": user_score = user_count
            else: user_score = user_score/user_count
            day_sign = datetime.strptime("2022-04-12", "%Y-%m-%d") - datetime.strptime(day, "%Y-%m-%d")
            day_sign = day_sign.days
            day_flag = 1
            if day_sign > 0: day_flag = 0
            if -30 <= day_sign <= 30:
                if day not in day_aves: 
                    day_aves[day] = 0
                    day_counts[day] = 0
                day_aves[day] += user_score
                day_counts[day] += 1
toronto_day_aves = {x:day_aves[x]/day_counts[x] for x in day_aves}

day_aves = {}
day_counts = {}
for day in sorted(list(world_day_dict.keys())):
    for user in world_day_dict[day]:
        user_score = 0
        user_count = 0
        for domain in world_day_dict[day][user]:
            if domain in domain_dict and domain_dict[domain] in ranking_dict:
                user_score += ranking_dict[domain_dict[domain]]
                user_count += 1
        if user_count > 0:
            if flag == "COUNT": user_score = user_count
            else: user_score = user_score/user_count
            day_sign = datetime.strptime("2022-04-12", "%Y-%m-%d") - datetime.strptime(day, "%Y-%m-%d")
            day_sign = day_sign.days
            day_flag = 1
            if day_sign > 0: day_flag = 0
            if -30 <= day_sign <= 30:
                if day not in day_aves: 
                    day_aves[day] = 0
                    day_counts[day] = 0
                day_aves[day] += user_count
                day_counts[day] += 1
montreal_day_aves = {x:day_aves[x]/day_counts[x] for x in day_aves}

w = open('compare_world.csv',"w+")
for day in toronto_day_aves:
    w.write("{},{},{}\n".format(day,toronto_day_aves[day],montreal_day_aves[day]))
w.close()
