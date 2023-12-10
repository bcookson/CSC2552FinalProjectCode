import json
from datetime import datetime
subreddit_list = []
f = open("../../subreddit_list.csv")
for name in f:
    name = name.strip()
    subreddit_list.append(name)
f.close()
u = open("../../toronto_left_users")
user_set = set()
for user in u:
    user_set.add(user.strip().split(",")[0])


toronto_post_by_day = {}
toronto_comment_by_day = {}
world_post_by_day = {}
world_comment_by_day = {}
for subreddit_name in subreddit_list:
    print("Started {}".format(subreddit_name))
    parents = open("../../../data/"+subreddit_name+"_submissions_2022", "r")
    f = open("../../../data/"+subreddit_name+"_submissions_2022_filtered", "r")
    c = open("../../../data/"+subreddit_name+"_comments_2022_filtered", "r")

    parent_map = {}
    for line in parents:
        line = json.loads(line)
        parent_map[line['name']] = line['domain']

    for line in f:
        line = json.loads(line)
        ts = int(line['created_utc'])
        post_date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        if post_date not in toronto_post_by_day: 
            toronto_post_by_day[post_date] = {}
            world_post_by_day[post_date] = {}
        if line['author'] in user_set:
            if line['author'] in toronto_post_by_day[post_date]:
                toronto_post_by_day[post_date][line['author']].append(line['domain'])
            else:
                toronto_post_by_day[post_date][line['author']] = [line['domain']]
        # else:
        #     if line['author'] in world_post_by_day[post_date]:
        #         world_post_by_day[post_date].append(line['domain'])
        #     else:
        #         world_post_by_day[post_date] = [line['domain']]

    # o = open("domains/toronto_{}_submissions".format(subreddit_name),"w+")
    # for day in toronto_post_by_day:
    #     o.write("{};{}\n".format(day,str(toronto_post_by_day[day])))

    for line in c:
        line = json.loads(line)
        ts = int(line['created_utc'])
        post_date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        if post_date not in toronto_post_by_day: 
            toronto_post_by_day[post_date] = {}
        if line['parent_id'] in parent_map:
            if line['author'] in user_set:
                if line['author'] in toronto_post_by_day[post_date]:
                    toronto_post_by_day[post_date][line['author']].append(parent_map[line['parent_id']])
                else:
                    toronto_post_by_day[post_date][line['author']] = [parent_map[line['parent_id']]]
            # else:
            #     if post_date in world_comment_by_day:
            #         world_comment_by_day[post_date].append(parent_map[line['parent_id']])
            #     else:
            #         world_comment_by_day[post_date] = [parent_map[line['parent_id']]]


    # o3 = open("domains/toronto_{}_comments".format(subreddit_name),"w+")
    # for day in toronto_comment_by_day:
    #     o3.write("{};{}\n".format(day,str(toronto_comment_by_day[day])))

    # o4 = open("domains/world_{}_comments".format(subreddit_name),"w+")
    # for day in world_comment_by_day:
    #     o4.write("{};{}\n".format(day,str(world_comment_by_day[day])))


    # o.close()
    # o2.close()
    # o3.close()
    # o4.close()
    f.close()

    print("Started {}".format(subreddit_name))

print(len([x for x in toronto_post_by_day]))
o = open("toronto_left_user_domains.csv".format(subreddit_name),"w+")
for day in toronto_post_by_day:
    o.write("{};{}\n".format(day,json.dumps(toronto_post_by_day[day])))
u.close()
