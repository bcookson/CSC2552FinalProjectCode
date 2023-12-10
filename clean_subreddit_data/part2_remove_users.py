import json

subreddit_list = []
f = open("subreddit_list.csv")
for name in f:
    name = name.strip()
    subreddit_list.append(name)
f.close()

user_list = set()
f = open("remove_user_list.csv")
for name in f:
    name = name.strip()
    user_list.add(name)
f.close()

file_types = ["data/{}_submissions_2022","data/{}_comments_2022"]
for name in subreddit_list:
    print("{} started".format(name))
    for file in [x.format(name) for x in file_types]:
        if "submissions" in file:
            write_name = "data/{}_submissions_2022_filtered".format(name)
        else:
            write_name = "data/{}_comments_2022_filtered".format(name)
        f = open(file)
        w = open(write_name,"w+")
        for line in f:
            jline = json.loads(line)
            a = jline['author']
            if a not in user_list:
                w.write(line)
        f.close()
        w.close()
    print("{} completed".format(name))