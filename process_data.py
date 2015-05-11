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
         open("data/weather.csv") as w, \
         open("data/key.csv") as k, \
         open("data/train2.csv", 'wb') as t2, \
         open("data/weather2.csv", 'wb') as w2, \
         open("data/key2.csv", 'wb') as k2:

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
        w_out = csv.writer(w2)
        w_out.writerow(next(w_in, None))
        weather = []
        for row in w_in:
            weather.append(row)

        k_in = csv.reader(k)
        k_out = csv.writer(k2)
        k_out.writerow(next(k_in, None))
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

    with open("data/storms_train.csv", 'wb') as s:
        s_out = csv.writer(s)
        s_out.writerow(['date', 'store_nbr'])
        for row in train[1:]:
            if row[4] == '1' and row[0] != prev_date and row[1] != prev_store:
                storm_count += 1
                prev_date = row[0]
                prev_store = row[1]
                s_out.writerow([row[0], row[1]])

    print storm_count

    with open("data/storms_train.csv") as s:
        for row in csv.reader(s):
            storms.append(row)

    storm_dict = {}
    for row in storms:
        date      = row[0]
        store_nbr = row[1]
        if store_nbr in storm_dict:
            storm_dict[store_nbr].append(date)
        else:
            storm_dict[store_nbr] = [date]

    date_format = '%Y-%m-%d'
    for row in train[1:]:
        date      = datetime.datetime.strptime(row[0], date_format)
        store_nbr = row[1]
        days_till_storm = 99999
        if store_nbr in storm_dict:
            for storm_date in storm_dict[store_nbr]:
                storm_date = datetime.datetime.strptime(storm_date, date_format)
                delta = storm_date - date
                if abs(delta.days) < abs(days_till_storm):
                    days_till_storm = delta.days
            # if days_till_storm > 10:
            #     days_till_storm = 10
        row.append(days_till_storm)
        print row

def main():
    # read_data()
    get_storms("data/train2.csv")

if __name__ == '__main__':
    main()
