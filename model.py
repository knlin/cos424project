from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Perceptron, LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import datetime
import numpy as np
import math

regressions = dict()
regressions["LR"] = LinearRegression()
regressions["KNN"] = KNeighborsRegressor(n_neighbors=5)
regressions["PR"] = Perceptron()
regressions["LS"] = Lasso()
regressions["RI"] = Ridge()
regressions["EN"] = ElasticNet()
regressions["GBR"] = GradientBoostingRegressor()
regressions["AB"] = AdaBoostRegressor()
regressions["DT"] = DecisionTreeRegressor()

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

def do_regression(r, x, y, testx):
    reg = regressions[r]
    reg.fit(x, y)
    return reg.predict(testx)

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
units = train["units"]
results = test["units"]
train = train.drop("codesum", 1)
test = test.drop("codesum", 1)

# train by store
MSE = 0.0
for i in range(1, 46):
    traindata = train[train.store_nbr == i]
    unitdata = traindata["units"]
    traindata.drop("units", 1)
    testdata = test[test.store_nbr == i]
    resultdata = testdata["units"]
    testdata.drop("units", 1)
    items = list(set(testdata.item_nbr.values))

    a = do_regression("GBR", traindata,unitdata,testdata)
    MSE += mean_squared_error(a, resultdata)
    tot = 0.0
    resultdata = resultdata.values
    for j in range(0, len(a)):
        tot += abs(a[j] - resultdata[j])
    print "absolute error for store %d: %d" % (i, tot)
print "RMSE: %d" % math.sqrt(MSE)
