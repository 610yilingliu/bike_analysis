import collections
import re
import pandas as pd
from geopy.distance import geodesic

df = pd.read_csv("./data/gxdc_tcd.csv")

lo_la = collections.defaultdict(list)
road = []
sq = []
center_la, center_lo = [], []
fid = []
lengths, widths = [], []
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
        
        lo_la[curla].append(p2)
        lo_la[curlo].append(p1)
        # 原为[纬度,经度].改为[经度,纬度]格式
        curpos[j][0] = p2
        curpos[j][1] = p1

    p_1 = (lo_la['LATITUDE_0'][-1], lo_la['LONGITUDE_0'][-1])
    p_2 = (lo_la['LATITUDE_1'][-1], lo_la['LONGITUDE_1'][-1])
    p_3 = (lo_la['LATITUDE_2'][-1], lo_la['LONGITUDE_2'][-1])
    dist1 = geodesic(p_1, p_2).meters
    dist2 = geodesic(p_2, p_3).meters
    length = max(dist1, dist2)
    width = min(dist1, dist2)
    lengths.append(length)
    widths.append(width)

    la = sum([x[1] for x in points[:4]])/4
    lo = sum(x[0] for x in points[:4])/4
    fid.append(i)

    
    ar = width * length
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
df['LENGTH'] = lengths
df['WIDTH'] = widths

df = df.drop("FENCE_LOC", axis = 1)

df.to_csv('./cleaned_data/fence_position.csv', index = False)
# obj = {'type':'Polygon', 'coordinates':[[24.4928789919, 118.1112102522],[24.4929066503, 118.1111994658],[24.492907902, 118.1112032986],[24.4928802436, 118.111214085],[24.4928789919, 118.1112102522]]}

