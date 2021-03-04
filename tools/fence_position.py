import collections
import re
import pandas as pd
from area import area

df = pd.read_csv("./data/gxdc_tcd.csv")

lo_la = collections.defaultdict(list)
road = []
sq = []
center_la, center_lo = [], []
fid = []
def extract_chinese(txt):
    pattern = re.compile("[\u4e00-\u9fa5]")
    return "".join(pattern.findall(txt))

for i in range(len(df)):
    fc_name = df["FENCE_ID"][i]
    df["FENCE_LOC"][i] = pd.eval(df["FENCE_LOC"][i])
    fc = df["FENCE_LOC"][i]
    a, b, c, d, e = fc
    points = (a, b, c, d, e)
    curpos = [[0, 0] for _ in range(5)]
    for j in range(5):
        p1, p2 = points[j]
        curla = 'LATITUDE_' + str(j)
        curlo = 'LONGITUDE_' + str(j)
        
        lo_la[curlo].append(p1)
        lo_la[curla].append(p2)
        # 原为[纬度,经度].改为[经度,纬度]格式
        curpos[j][0] = p2
        curpos[j][1] = p1
    la = sum([x[1] for x in points[:4]])/4
    lo = sum(x[0] for x in points[:4])/4
    fid.append(i)
    obj = {'type':'Polygon','coordinates':[curpos]}
    ar = area(obj)
    sq.append(ar)
    center_la.append(la)
    center_lo.append(lo)
    road.append(extract_chinese(fc_name))

for k, v in lo_la.items():
    df[k] = v

df['LATITUDE'] = center_la
df['LONGITUDE'] = center_lo
df['ROAD'] = road
df['AREA'] = sq
df['FID'] = fid

df = df.drop("FENCE_LOC", axis = 1)

df.to_csv('./cleaned_data/fence_position.csv', index = False)
