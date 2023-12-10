import json


utc_start = 1641013200
utc_end = 1672549199

user_set = set()

f = open("../data/toronto_submissions", "r")
for line in f:
    line = json.loads(line)
    a = line['author']
    t = int(line['created_utc'])
    if a != '[deleted]' and utc_start <= t <= utc_end:
        user_set.add(a)
f.close()

f = open("../data/toronto_comments", "r")
for line in f:
    line = json.loads(line)
    a = line['author']
    t = int(line['created_utc'])
    if a != '[deleted]' and utc_start <= t <= utc_end:
        user_set.add(a)
f.close()
print("TORONTO")

f = open("../data/askTO_submissions", "r")
for line in f:
    line = json.loads(line)
    a = line['author']
    t = int(line['created_utc'])
    if a != '[deleted]' and utc_start <= t <= utc_end:
        user_set.add(a)
f.close()

f = open("../data/askTO_comments", "r")
for line in f:
    line = json.loads(line)
    a = line['author']
    t = int(line['created_utc'])
    if a != '[deleted]' and utc_start <= t <= utc_end:
        user_set.add(a)
f.close()
print("ASKTORONTO")

f = open("../data/TTC_submissions", "r")
for line in f:
    line = json.loads(line)
    a = line['author']
    t = int(line['created_utc'])
    if a != '[deleted]' and utc_start <= t <= utc_end:
        user_set.add(a)
f.close()

f = open("../data/TTC_comments", "r")
for line in f:
    line = json.loads(line)
    a = line['author']
    t = int(line['created_utc'])
    if a != '[deleted]' and utc_start <= t <= utc_end:
        user_set.add(a)
f.close()
print("TTC")

f = open("toronto_users","w+")
for name in user_set:
    f.write(name + "\n")
f.close()


# user_dict = {}
# for line in f:
#     line = json.loads(line)
#     a = line['author']
#     if a != '[deleted]':
#         if a in user_dict: user_dict[a] += 1
#         else: user_dict[a] = 1


# items = [(x[0],x[1]) for x in user_dict.items()]