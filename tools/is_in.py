import pandas as pd

fences = pd.read_csv('./cleaned_data/fance_position.csv')
bikes = pd.read_csv('./data/gxdc_dd.csv')


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
    def cross(x_1, y_1, x_2, y_2, xt, yt):
        return (x_2 - x_1) * (yt - y_1) - (xt - x_1) * (y_2 - y_1)
    x, y = point
    x1, y1, x2, y2, x3, y3, x4, y4 = region
    return cross(x1, y1, x2, y2, x, y) * cross(x3, y3, x4, y4, x, y) >= 0 and cross(x2, y2, x3, y3, x, y) * cross(x4, y4, x1, y1, x, y) >= 0







    


