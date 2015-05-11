from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron, LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import datetime
import numpy as np

WT = ('HZ', 'FU', 'BLSN', 'VCTS', 'DZ', 'BR', 'FG', 'BCFG', 'DU',
      'FZRA', 'TS', 'RA', 'PL', 'GR', 'FZDZ', 'VCFG', 'FG+', 'TSRA',
      'FZFG', 'BLDU', 'MIFG', 'SQ', 'UP', 'SN')

def get_dow(date):
    date = str(date).strip()
    if "-" in date:
        da = date.split("-")
        y = da[0]
        m = da[1]
        d = da[2]
    elif "/" in date:
        da = date.split("/")
        y = da[2]
        m = da[0]
        d = da[1]
    date = datetime.datetime(int(y), int(m), int(d)).date()
    return date.timetuple().tm_wday

def date_to_doy(date):
    if "-" in date:
        da = date.split("-")
        y = da[0]
        m = da[1]
        d = da[2]
    elif "/" in date:
        da = date.split("/")
        y = da[2]
        m = da[0]
        d = da[1]
    date = datetime.datetime(int(y), int(m), int(d)).date()
    return date.timetuple().tm_yday

def do_LR(x, y, testx):
    print "LR.."
    reg = LinearRegression()
    reg.fit(x, y)
    print "done fitting"
    return reg.predict(testx)

def do_gbr(x, y, testx):
    print "gbr.."
    reg = GradientBoostingRegressor(n_estimators=20)
    reg.fit(x, y)
    print "done fitting"
    return reg.predict(testx)

def do_knn(x, y, testx, n):
    knnc = KNeighborsClassifier(n_neighbors=n)
    knnc.fit(x, y)
    return clf.predict(testx)

def do_perceptron(x, y, testx):
    print "perceptron.."
    clf = Perceptron()
    clf.fit(x, y)
    print "done fitting"
    return clf.predict(testx)

def set_to_dict(set):
    d = dict()
    cnt = 0
    for i in set:
        d[i] = cnt
        cnt += 1

def str_to_int(str, dict):
    if str == None or dict == None:
        return 0
    return dict[str]

train = pd.read_csv("data/features.csv")
train['dow'] = train['date'].map(lambda x: get_dow(str(x)))
train['date'] = train['date'].apply(lambda x: date_to_doy(str(x)))
train.fillna(0, inplace=True)
a = list(set(train.codesum.values))
sfoo = set()
for i in a:
    c = i.split(" ")
    for j in c:
        sfoo.add(j)
print sfoo
for t in WT:
    train[t] = train['codesum'].map(lambda x: t in str(x))
"""departs = set_to_dict(list(set(train.depart.values)))
codesums = set_to_dict(list(set(train.codesum.values)))
sunrises = set_to_dict(list(set(train.sunrise.values)))
train['depart'] = train['depart'].apply(lambda x: str_to_int(str(x), departs))
train['codesum'] = train['codesum'].apply(lambda x: str_to_int(str(x), codesums))
train['sunrise'] = train['sunrise'].apply(lambda x: str_to_int(str(x), sunrises))"""
units = train["units"]
train = train.drop("units", 1)
train = train.drop("codesum", 1)
train = train.drop("depart", 1)
train = train.drop("sunrise", 1)
train = train.drop("sunset", 1)
train = train.drop("stnpressure", 1)
train = train.drop("sealevel", 1)
train = train.drop("resultspeed", 1)
train = train.drop("resultdir", 1)
train = train.drop("avgspeed", 1)
train = train.drop("dewpoint", 1)
train = train.drop("tmax", 1)
train = train.drop("tmin", 1)
from sklearn.cross_validation import train_test_split
train, test, units, results = train_test_split(train, units, test_size=0.2)
"""test = pd.read_csv("data/test_features.csv")
test = test.drop("sunrise", 1)
test = test.drop("depart", 1)
test = test.drop("codesum", 1)
test = test.drop("date", 1)"""
#test.fillna(0, inplace=True)

#a = do_perceptron(train, units, test)
a = do_gbr(train,units,test)
b = np.sqrt(mean_squared_error(a, results))
