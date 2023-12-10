from bs4 import BeautifulSoup
import requests

domain_list = []
f = open("world_domain_list.csv")
for name in f:
    name = name.strip().split(",")
    domain_list.append(name[0])
f.close()

article_names = ["center","left","leftcenter","right-center","right","conspiracy","fake-news","pro-science","satire"]
list_articles = ["https://mediabiasfactcheck.com/{}/".format(x) for x in article_names]
bias_dict = {}
link_dict = {}


for i in range(len(list_articles)):
    article = list_articles[i]
    name = article_names[i]
    page = requests.get(article)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("a")
    for a in links:
        bias_dict[a.text] = name
        link_dict[a.text] = a['href']

f = open("found_domains.csv","w+")
f2 = open("unfound_domains.csv","w+")
for domain in domain_list:
    found = False
    for key in bias_dict.keys():
        if domain in key:
            f.write("{},{},{}\n".format(domain,bias_dict[key],link_dict[key]))
            found = True
            print(domain + ": Found")
            break
    if not found:
        f2.write(domain + "\n")
        print(domain + ": NOT Found")



    
