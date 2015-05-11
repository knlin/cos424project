from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Perceptron, LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostRegressor, RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import datetime
import numpy as np
import math

regressions = dict()
regressions["LR"] = LinearRegression()
regressions["KNN"] = KNeighborsRegressor(n_neighbors=5)
regressions["LS"] = Lasso()
regressions["RI"] = Ridge()
regressions["EN"] = ElasticNet()
regressions["GBR"] = GradientBoostingRegressor(max_depth = 5)
regressions["ADA"] = AdaBoostRegressor()
regressions["DT"] = DecisionTreeRegressor()
regressions["RF"] = RandomForestRegressor()

WT = ('HZ', 'FU', 'BLSN', 'VCTS', 'DZ', 'BR', 'FG', 'BCFG', 'DU',
      'FZRA', 'TS', 'RA', 'PL', 'GR', 'FZDZ', 'VCFG', 'FG+', 'TSRA',
      'FZFG', 'BLDU', 'MIFG', 'SQ', 'UP', 'SN')

def normalize_date(date):
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
    return date

def get_dow(date):
    date = normalize_date(date)
    return date.timetuple().tm_wday

def date_to_doy(date):
    date = normalize_date(date)
    return date.timetuple().tm_yday

def do_regression(r, x, y, testx):
    reg = regressions[r]
    reg.fit(x, y)
    return reg.predict(testx)

train = pd.read_csv("data/featurestrain.csv")
test = pd.read_csv("data/featurestest.csv")
train['dow'] = train['date'].map(lambda x: get_dow(str(x)))
#train['date'] = train['date'].apply(lambda x: date_to_doy(str(x)))
train.fillna(0, inplace=True)
test['dow'] = test['date'].map(lambda x: get_dow(str(x)))
#test['date'] = test['date'].apply(lambda x: date_to_doy(str(x)))
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
error = 0.0
errorl = 0.0

for i in range(1, 46):
    traindata = train[train.store_nbr == i]
    unitdata = traindata["units"]
    traindata = traindata.drop("units", 1)
    traindata = traindata.drop("date", 1)
    testdata = test[test.store_nbr == i]
    resultdata = testdata["units"]
    testdata = testdata.drop("units", 1)
    testdata = testdata.drop("date", 1)
    items = testdata.item_nbr.values
    #dates = testdata["date"].values

    a = do_regression("GBR", traindata,unitdata,testdata)
    a = map(abs, a)
    MSE += mean_squared_error(a, resultdata)
    tot = 0.0
    resultdata = resultdata.values
    for j in range(0, len(a)):
        errorl += math.pow(math.log(a[j]+1) - math.log(resultdata[j]+1), 2)
        error += math.pow(a[j] - resultdata[j], 2)
        tot += abs(a[j] - resultdata[j])
    print "absolute error for store %d (%d points): %d" % (i, len(testdata["tavg"]), tot)
error = float(error) / len(test["tavg"])
errorl = float(errorl) / len(test["tavg"])
print "RMSE: %f" % math.sqrt(error)
print "RMSLE: %f" % math.sqrt(errorl)

