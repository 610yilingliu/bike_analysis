import collections
import json
import pandas as pd


df = pd.read_csv('./cleaned_data/fence_position.csv')

road_dic = collections.defaultdict(list)

for i in range(len(df)):
    name = df['ROAD'][i]
    lo = df['LONGITUDE'][i]
    la = df['LATITUDE'][i]
    road_dic[name].append((la, lo))

f = open("./cleaned_data/road_locs.json","w")
f.write(json.dumps(road_dic))
f.close()

# example to read
# file=open("./cleaned_data/road_locs.json","r")
# content=file.readline()
# file.close()
# print(json.loads(content))