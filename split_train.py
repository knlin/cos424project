import pandas as pd
import random
import datetime
from datetime import timedelta

def str_to_dt(str):
    s = str.split("-")
    d = datetime.datetime(int(s[0]), int(s[1]), int(s[2])).date()
    return d

def is_within_3(line, storm_list, keys):
    l = line.split(",")
    date = l[0]
    ddate = str_to_dt(date)
    store = int(keys[l[1]])
    for i in [-3, -2, -1, 0, 1, 2, 3]:
        if (str(ddate + timedelta(days=i)), store) in storm_list:
            return True
    return False

def split_weather():
    with open("data/key.csv") as f:
        content = f.readlines()

    normalkey = dict()
    for i in content:
        a = i.split(",")
        a[0] = a[0].strip()
        a[1] = a[1].strip()
        normalkey[a[0]] = a[1]
    with open("data/train.csv") as f:
        content = f.readlines()
    train_list = []
    content = content[1:]
    for i in content:
        a = i.split(",")
        d = a[0].split("/")
        a[0] = str(datetime.datetime(int(d[2]), int(d[0]), int(d[1])).date())
        train_list.append(a)
    weather = pd.read_csv('data/weatherOriginal.csv')
    weather_train = weather[weather.date < '2012-08-01']
    snow = weather_train[weather_train.snowfall >= '2.0']
    snow = snow[snow.snowfall != 'M']
    snow = snow[snow.snowfall != 'T']

    rain = weather_train[weather_train.preciptotal >= '1.0']
    rain = rain[rain.preciptotal != 'M']
    rain = rain[rain.preciptotal != 'T']

    storm_stations = set()
    storm_dict = dict()
    storm_list = []
    for i in snow.index.values:
        storm_stations.add( (snow.ix[i].station_nbr, snow.ix[i].date) )
    for i in rain.index.values:
        storm_stations.add( (rain.ix[i].station_nbr, rain.ix[i].date) )
    print len(storm_stations)

    for i in storm_stations:
        storm_list.append((i[1], i[0]))
        if i[1] in storm_dict:
            storm_dict[i[1]].append(int(i[0]))
        else:
            storm_dict[i[1]] = [i[0]]
    print len(storm_dict)
    print storm_dict
    print storm_list

    train_real = []
    test_real = []
    with open("data/train2.csv") as f:
        content = f.readlines()
    content = content[1:]
    f = open("data/train_split.csv", "w")
    f2 = open("data/test_split.csv", "w")
    for i in content:
        if is_within_3(i, storm_list, normalkey):
            test_real.append(i)
            f2.write(i.strip() + "\n")
        else:
            train_real.append(i)
            f.write(i.strip() + "\n")
    f.close()
    f2.close()
    print type(storm_list[0][1])
    print len(storm_list)

split_weather()
