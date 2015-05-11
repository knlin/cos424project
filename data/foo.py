import random
with open("features.csv") as f:
    content = f.readlines()
ftest = open("featurestest.csv", "w")
ftrain = open("featurestrain.csv", "w")
ftest.write(content[0].strip() + "\n")
ftrain.write(content[0].strip() + "\n")
content = content[1:]
for i in content:
    if random.random() > 0.85:
        ftest.write(i.strip() + "\n")
    else:
        ftrain.write(i.strip() + "\n")
