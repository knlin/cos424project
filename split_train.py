import pandas as pd
import random

def split_weather():
    train = pd.read_csv('train.csv')
    keys = pd.read_csv('key.csv')
    with open("key.csv") as f:
        content = f.readlines()
    normalkey = dict()
    for i in content:
        a = i.split(",")
        a[0] = a[0].strip()
        a[1] = a[1].strip()
        normalkey[a[0]] = a[1]
    with open("train.csv") as f:
        content = f.readlines()
    train_list = []
    content = content[1:]
    import datetime
    for i in content:
        a = i.split(",")
        d = a[0].split("/")
        a[0] = str(datetime.datetime(int(d[2]), int(d[0]), int(d[1])).date())
        train_list.append(a)
    weather = pd.read_csv('weather.csv')
    weather_train = weather[weather.date <= '2012-08-01']
    snow = weather_train[weather_train.snowfall >= '1.0']
    snow = snow[snow.snowfall != 'M']

    rain = weather_train[weather_train.preciptotal >= '2.0']
    rain = rain[rain.preciptotal != 'M']

    storm_dates = set()
    storm_stations = set()
    storm_dict = dict()

    for i in snow.index.values:
        storm_dates.add( snow.ix[i].date )
        storm_stations.add( (snow.ix[i].station_nbr, snow.ix[i].date) )
    for i in rain.index.values:
        storm_dates.add( rain.ix[i].date )
        storm_stations.add( (rain.ix[i].station_nbr, rain.ix[i].date) )
    for i in storm_stations:
        if i[1] in storm_dict:
            storm_dict[i[1]].append(int(i[0]))
        else:
            storm_dict[i[1]] = [i[0]]
    real_train = []
    real_test = []
    for i in train_list:
        stat = normalkey[i[1]]
        if i[0] in storm_dict and int(stat) in storm_dict[i[0]]:
            real_test.append(i)
        else:
            real_train.append(i)
    print len(real_test)
    print len(real_train)
    return (real_train, real_test)

split_weather()
