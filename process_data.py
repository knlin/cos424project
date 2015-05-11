import numpy as np
import csv
import datetime

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def read_data():
    with open("data/train.csv") as t, \
         open("data/weatherOriginal.csv") as w, \
         open("data/key.csv") as k, \
         open("data/train2.csv", 'wb') as t2:

        t_in = csv.reader(t)
        t_out = csv.writer(t2)
        t_out.writerow(next(t_in, None)) # skip header in input, write header to output
        train = []
        for row in t_in:
            train.append(row)
        print "Converting train.csv time format to match weather.csv..."
        for row in train:
            row[0] = datetime.datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d')
        print "Done."

        w_in = csv.reader(w)
        weather = []
        for row in w_in:
            weather.append(row)

        k_in = csv.reader(k)
        key = []
        for row in k_in:
            key.append(row)

        key_dict = {row[0]:row[1] for row in key}

        print "Writing to train2.csv..."
        for row in train:
            station_nbr = key_dict[row[1]]
            date = row[0]
            for j in weather:
                if station_nbr == j[0] and date == j[1]:
                    if ("SN" in j[12] or "SG" in j[12]) and is_number(j[13]) and float(j[13]) >= 2.0:
                        row.append('1')
                    elif ("RA" in j[12] and "SN" not in j[12]) and is_number(j[14]) and float(j[14]) >= 1.0:
                        row.append('1')
                    else:
                        row.append('0')
                    break
            t_out.writerow(row)
        print "Done."

        # snow = (
        #     (str_detect(codesum,"SN") || str_detect(codesum,"SG")) &&
        #     !is.na(as.numeric(as.character(snowfall))) &&
        #     as.numeric(as.character(snowfall)) >= inches_snow),
        # rain = (
        #     (str_detect(codesum,"RA") && !str_detect(codesum,"SN")) &&
        #     !is.na(as.numeric(as.character(preciptotal))) &&
        #     as.numeric(as.character(preciptotal)) >= inches_rain)

def get_storms(trainfile):
    train = []
    storms = []
    storm_count = 0
    prev_date = ''
    prev_store = ''

    with open(trainfile) as t:
        for row in csv.reader(t):
            train.append(row)
    # write list of storms (date, store_nbr)
    with open("data/storms_train.csv", 'wb') as s:
        s_out = csv.writer(s)
        s_out.writerow(['date', 'store_nbr'])
        for row in train[1:]:
            try:
                if row[4] == '1' and row[0] != prev_date and row[1] != prev_store:
                    storm_count += 1
                    prev_date = row[0]
                    prev_store = row[1]
                    s_out.writerow([row[0], row[1]])
            except IndexError:
                print row
    print "Number of storms: %d" % storm_count
    # import list of storms (date, store_nbr)
    with open("data/storms_train.csv") as s:
        for row in csv.reader(s):
            storms.append(row)
    # storm_dict = map from store_nbr to list of storm dates
    storm_dict = {}
    for row in storms:
        date      = row[0]
        store_nbr = row[1]
        if store_nbr in storm_dict:
            storm_dict[store_nbr].append(date)
        else:
            storm_dict[store_nbr] = [date]
    # write new feature "days_after_storm" to train3.csv
    print "Writing to train3.csv..."
    with open("train3.csv", 'wb') as t3:
        t_out = csv.writer(t3)
        train[0][-1] = "days_after_storm"
        t_out.writerow(train[0])
        date_format = '%Y-%m-%d'
        days_threshold = 100000
        for row in train[1:]:
            date      = datetime.datetime.strptime(row[0], date_format) # datetime.datetime.strptime(row[0], '%m/%d/%Y')
            store_nbr = row[1]
            days_after_storm = 213 # 1/1/2012-8/1/2012
            if store_nbr in storm_dict:
                for storm_date in storm_dict[store_nbr]:
                    storm_date = datetime.datetime.strptime(storm_date, date_format)
                    delta = date - storm_date
                    if abs(delta.days) < abs(days_after_storm):
                        days_after_storm = delta.days
            if days_after_storm > days_threshold:
                days_after_storm = days_threshold
            elif days_after_storm < -days_threshold:
                days_after_storm = -days_threshold
            row[-1] = days_after_storm
            row[0] = date.strftime('%-m/%-d/%Y')
            t_out.writerow(row)
    print "Done."

def main():
    # read_data()
    get_storms("data/train2.csv")

if __name__ == '__main__':
    main()
