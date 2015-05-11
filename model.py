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

train = pd.read_csv("data/featurestrain.csv")
test = pd.read_csv("data/featurestest.csv")
train['dow'] = train['date'].map(lambda x: get_dow(str(x)))
train['date'] = train['date'].apply(lambda x: date_to_doy(str(x)))
train.fillna(0, inplace=True)
test['dow'] = test['date'].map(lambda x: get_dow(str(x)))
test['date'] = test['date'].apply(lambda x: date_to_doy(str(x)))
test.fillna(0, inplace=True)
a = list(set(train.codesum.values))
for t in WT:
    train[t] = train['codesum'].map(lambda x: t in str(x))
for t in WT:
    test[t] = test['codesum'].map(lambda x: t in str(x))
"""departs = set_to_dict(list(set(train.depart.values)))
codesums = set_to_dict(list(set(train.codesum.values)))
sunrises = set_to_dict(list(set(train.sunrise.values)))
train['depart'] = train['depart'].apply(lambda x: str_to_int(str(x), departs))
train['codesum'] = train['codesum'].apply(lambda x: str_to_int(str(x), codesums))
train['sunrise'] = train['sunrise'].apply(lambda x: str_to_int(str(x), sunrises))"""
#units = pd.concat([train["units"], train["store_nbr"]], axis=1, keys=["units", "store_nbr"])
units = train["units"]
results = test["units"]
train = train.drop("codesum", 1)
test = test.drop("codesum", 1)
"""test = pd.read_csv("data/test_features.csv")
test = test.drop("sunrise", 1)
test = test.drop("depart", 1)
test = test.drop("codesum", 1)
test = test.drop("date", 1)"""
#test.fillna(0, inplace=True)

#a = do_perceptron(train, units, test)
#a = do_gbr(train,units,test)
#b = np.sqrt(mean_squared_error(a, results))

# for each test point, train only on store_nbr
for i in range(1, 46):
    traindata = train[train.store_nbr == i]
    unitdata = traindata["units"]
    traindata.drop("units", 1)
    testdata = test[test.store_nbr == i]
    resultdata = testdata["units"]
    testdata.drop("units", 1)
    items = list(set(testdata.item_nbr.values))

    a = do_gbr(traindata,unitdata,testdata)
    print "%d: " % i
    print np.sqrt(mean_squared_error(a,resultdata))
    tot = 0.0
    resultdata = resultdata.values
    for j in range(0, len(a)):
        tot += abs(a[j] - resultdata[j])
        print "(%d %d)"% (a[j], resultdata[j]),
    print tot
