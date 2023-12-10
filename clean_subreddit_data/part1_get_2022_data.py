import json

subreddit_list = []
f = open("subreddit_list.csv")
for name in f:
    name = name.strip()
    subreddit_list.append(name)
f.close()

for file_name in subreddit_list:
    f = open("data/"+file_name, "r")
    w = open("data/"+file_name+"_2022","w+")
    utc_start = 1641013200
    utc_end = 1672549199

    i = 0
    for line in f:
        jline = json.loads(line)
        ts = int(jline['created_utc'])
        if utc_start <= ts <= utc_end:
            w.write(line)
        i += 1
        if i%700000==0:print("{}GB".format(i/700000))

    f.close()
    w.close()
