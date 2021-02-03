import pandas as pd
import re

df = pd.read_csv("./data/gxdc_tcd.csv")

LATITUDE = []
LONGITUDE = []
road = []

def extract_chinese(txt):
    pattern = re.compile("[\u4e00-\u9fa5]")
    return "".join(pattern.findall(txt))

for i in range(len(df)):
    fc_name = df["FENCE_ID"][i]
    fc = df["FENCE_LOC"][i]
    a, b, c, d, e = fc.split('],')
    lo = 0
    la = 0
    for point_raw in (a, b, c, d):
        to_remove = '[] '
        for symb in to_remove:
            point_raw = point_raw.replace(symb, '')
        p1, p2 = point_raw.split(',')
        lo += float(p1)
        la += float(p2)
    LATITUDE.append(la/4)
    LONGITUDE.append(lo/4)
    road.append(extract_chinese(fc_name))


df['LATITUDE'] = LATITUDE
df['LONGITUDE'] = LONGITUDE
df['ROAD'] = road
df = df.drop("FENCE_LOC", axis = 1)

df.to_csv('./cleaned_data/fance_position.csv')
