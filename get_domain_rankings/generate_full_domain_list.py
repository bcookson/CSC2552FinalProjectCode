from bs4 import BeautifulSoup
import requests

bias_dict = {'LEFT-CENTER':['LEFT-CENTER (by Saudi standards)','LEFT CENTER','LEFT-CENTER','LEFt-CENTER','LEFT LEANING PRO-SCIENCE','LEFT-CENTER – PRO-SCIENCE','PRO-SCIENCE (LEFT-LEANING)'],
 'RIGHT-CENTER':['RIGHT CENTER','RIGHT-CENTER'],
 'LEFT':['LEFT – PSEUDOSCIENCE','LEFT','LEFT LEANING','LEFT-PSEUDOSCIENCE','LEFT SATIRE','LEFT-CONSPIRACY/PSEUDOSCIENCE'],
 'CENTER':['LEAST BIASED','LEAST-BIASED','PRO-SCIENCE','SCIECE','PRO- SCIENCE','UNRATED'],
 'RIGHT':['RIGHT','RIGHT PSEUDOSCIENCE','RIGHT-SATIRE','RIGHT-PSEUDOSCIENCE','RIGHT CONSPIRACY/PSEUDOSCIENCE','RIGHT CONSPIRACY','RIGHT CONSPIRACY-PSEUDOSCIENCE','RIGHT-CONSPIRACY/PSEUDOSCIENCE','RIGHT-CONSPIRACY-PSEUDOSCIENCE','RIGHT – CONSPIRACY','RIGHT – CONSPIRACY AND PSEUDOSCIENCE'], 
 'FAR-LEFT':['FAR LEFT','FAR-LEFT'],
 'FAR-RIGHT':['Extreme Right','EXTREME RIGHT','FAR RIGHT','Far Right','FAR-RIGHT CONSPIRACY-PSEUDOSCIENCE','FAR RIGHT CONSPIRACY-PSEUSDOSCIENCE']}

info_dict =  {'VERY-HIGH':['VERY-HIGH','Very High','VERY HIGH','LEAST BIASED','LEAST-BIASED','Least Biased'],
  'HIGH':['HIGH\xa0CREDIBILITY','HIGH','HIGH CREDIBILITY','High'],
  'MOSTLY-FACTUAL':['MOSTLY FACTUAL'],
  'MIXED':['MIXED'],
  'LOW':['LOW CREDIBILITY'],
  'VERY-LOW':['VERY LOW','Fake News']
 }

domain_map = {}
f = open("found_domains.csv")
for line in f:
    line = line.strip().split(",")
    domain = line[0]
    link = line[2]
    domain_map[domain] = link
f.close()

unknown_biases = set()
unknown_infos = set()

w = open("full_domain_biases.csv","w+")
w2 = open("errors.csv","w+")
for domain in domain_map:
    try:
        link = domain_map[domain]
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")
        p = soup.find_all("p")
        p = [x for x in p if "Bias Rating:" in x.text]
        p = p[0].text.split('\n')
        bias = 'UNKNOWN'
        facts = 'UNKNOWN'
        for x in p:
            if 'bias rating' in x.lower():
                x = x.split(':')
                temp_bias = x[1].strip()
                if temp_bias not in bias_dict.keys():
                    for k in bias_dict:
                        if temp_bias in bias_dict[k]:
                            bias = k
                else:
                    bias = temp_bias
                if bias == 'UNKNOWN': unknown_biases.add(temp_bias)
            elif 'factual reporting' in x.lower():
                x = x.split(':')
                temp_facts = x[1].strip()
                if temp_facts not in info_dict.keys():
                    for k in info_dict:
                        if temp_facts in info_dict[k]:
                            facts = k
                else:
                    facts = temp_facts
                if facts == 'UNKNOWN': unknown_infos.add(temp_facts)
        w.write("{},{},{}\n".format(domain,bias,facts))
        print("{},{},{}".format(domain,bias,facts))
    except:
        print("ERROR: {}".format(domain))
        w2.write(domain + "\n")
w.close()
w2.close()