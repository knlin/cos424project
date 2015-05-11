# how features.csv was created
import pandas as pd
keys = pd.read_csv("data/key.csv")
out = open("data/featuresV2.csv", "w")
with open("data/train.csv") as f:
    content = f.readlines()
with open("data/weatherArbitraryImpsV2.csv") as f:
    content2 = f.readlines()
out.write(content[0].strip())
out.write(content2[0].strip() + "\n")
content = content[1:]
content2 = content2[1:]
weather_dict = dict()
for i in content2:
    a = i.split(",")
    b = a[1].split("/")
    y = b[2]
    m = b[0]
    d = b[1]
    if len(m) < 2:
        m = "0"+m
    if len(d) < 2:
        d = "0"+d
    #weather_dict[(a[0],y + "-" + m + "-" + d)] = a[2:]
    weather_dict[(a[0],a[1])] = a[2:]
for i in content:
    a = i.split(",")
    out.write(i.strip())
    store = a[1]
    stat = int(keys[keys.store_nbr == int(store)].station_nbr)
    date = a[0].strip()
    w = weather_dict[(str(stat),date)]
    for i in w:
        out.write("," + i.replace("\"", ""))
