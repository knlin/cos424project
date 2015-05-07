with open("key.csv") as f:
    content = f.readlines()
stations = dict()
content = content[1:]
for i in content:
    a = i.split(",")
    stations[int(a[0])] = int(a[1])
print stations
