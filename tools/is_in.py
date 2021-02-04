import pandas as pd

df = pd.read_csv('./cleaned_data/fance_position.csv')
points = []

for i in range(len(df)):
    la = df['LATITUDE'][i]
    lo = df['LONGITUDE'][i]
    points.append((la, lo))

def find_nearest(p, df):
    min_dis = float('inf')
    mi_point = None
    x1, y1, x2, y2, x3, y3, x4, y4 = None, None, None, None, None, None, None, None
    for i in range(len(df)):
        point = points[i]
        curdis = (point[0] - p[0]) * (point[0] - p[0]) + (point[1] - p[1]) * (point[1] - p[1])
        x1, y1, x2, y2, x3, y3, x4, y4 = df['LATITUDE_0'], df['LONGITUDE_0'], df['LATITUDE_1'], df['LONGITUDE_1'], df['LATITUDE_2'], df['LONGITUDE_2'], df['LATITUDE_3'], df['LONGITUDE_3']
        if curdis < min_dis:
            min_dis = curdis
            mi_point = point
    return mi_point, (x1, y1, x2, y2, x3, y3, x4, y4)

def is_inside(point, region):
    x, y = point
    x1, y1, x2, y2, x3, y3, x4, y4 = region
    ab = x2 - x1
    ae = x - x1
    cd = 







    


