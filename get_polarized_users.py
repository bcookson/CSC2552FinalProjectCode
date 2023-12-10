import json
from datetime import datetime

subreddit_list = []
f = open("subreddit_list.csv")
for name in f:
    name = name.strip()
    subreddit_list.append(name)
f.close()

user_list = set()
f = open("toronto_users")
for name in f:
    name = name.strip()
    user_list.add(name)
f.close()


domain_dict = {}
f = open("get_domain_rankings/full_domain_biases.csv")
for line in f:
    line = line.strip().split(",")
    domain_dict[line[0]] = line[1]
f.close()

bias_rankings = {'FAR-LEFT':-3,'LEFT':-2,'LEFT-CENTER':-1,'CENTER':0,'RIGHT-CENTER':1,'RIGHT':2,'FAR-RIGHT':3}

user_dict = {x:0 for x in user_list}
user_counts = {x:0 for x in user_list}
for subreddit_name in subreddit_list:
    print("Started " + subreddit_name)
    parents = open("../data/"+subreddit_name+"_submissions_2022", "r")
    f = open("../data/"+subreddit_name+"_submissions_2022_filtered", "r")
    c = open("../data/"+subreddit_name+"_comments_2022_filtered", "r")

    parent_map = {}
    for line in parents:
        line = json.loads(line)
        parent_map[line['name']] = line['domain']
    parents.close()

    for line in f:
        line = json.loads(line)
        a = line['author']
        d = line['domain'] if 'domain' in line else ''
        if a in user_dict:
            user_counts[a] += 1
            if d in domain_dict and domain_dict[d] in bias_rankings:
                user_dict[a] += bias_rankings[domain_dict[d]]
    f.close()

    for line in c:
        line = json.loads(line)
        a = line['author']
        d = parent_map[line['parent_id']] if line['parent_id'] in parent_map else ''
        if a in user_dict and line['parent_id'] in parent_map:
            user_counts[a] += 1
            if d in domain_dict and domain_dict[d] in bias_rankings:
                user_dict[a] += bias_rankings[domain_dict[d]]
    c.close()

    print("Finished " + subreddit_name)

user_dict = {x:user_dict[x]/user_counts[x] if user_counts[x] > 0 else 0 for x in user_dict}
con = open("toronto_right_users","w+")
cen = open("toronto_center_users","w+")
lib = open("toronto_left_users","w+")
cen_con = open("toronto_center_right_users","w+")
cen_lib = open("toronto_center_left_users","w+")

for user in user_dict:
    if user_dict[user] < -0.5:
        lib.write("{},{}\n".format(user,user_dict[user]))
    elif user_dict[user] > 0.5:
        con.write("{},{}\n".format(user,user_dict[user]))
    else:
        cen.write("{},{}\n".format(user,user_dict[user]))

    if 0 > user_dict[user] >= -0.5:
        cen_lib.write("{},{}\n".format(user,user_dict[user]))

    if 0 < user_dict[user] <= 0.5:
        cen_con.write("{},{}\n".format(user,user_dict[user]))

lib.close()
con.close()
cen.close()
cen_con.close()
cen_lib.close()