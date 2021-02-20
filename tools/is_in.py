import os
import time
import multiprocessing
import pandas as pd
from math import sqrt
from shapely import geometry
from collections import defaultdict
from geopy.distance import geodesic

def time_helper(seperator = '_', to_sec = True):
    """
    return a string like 2020_09_11_22_43_00 (if to_sec is True) or 2020_09_11_22_43 (if to_sec is False)
    """
    if to_sec:
        return time.strftime("%Y" + seperator + "%m" + seperator + "%d" + seperator + "%H" + seperator + "%M" + seperator + "%S", time.localtime()) 
    return time.strftime("%Y" + seperator + "%m" + seperator + "%d" + seperator + "%H" + seperator + "%M", time.localtime()) 

def find_nearest(p, df):
    min_dis = float('inf')
    mi_point = None
    x1, y1, x2, y2, x3, y3, x4, y4 = None, None, None, None, None, None, None, None
    for i in range(len(df)):
        point = (df['LATITUDE'][i], df['LONGITUDE'][i])
        curdis = geodesic(p, point).kilometers * 1000

        if curdis < min_dis:
            min_dis = curdis
            mi_point = point
            x1, y1, x2, y2, x3, y3, x4, y4 = df['LATITUDE_0'][i], df['LONGITUDE_0'][i], df['LATITUDE_1'][i], df['LONGITUDE_1'][i], df['LATITUDE_2'][i], df['LONGITUDE_2'][i], df['LATITUDE_3'][i], df['LONGITUDE_3'][i]
    return mi_point, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)], min_dis

def is_inside(polygon, Points):
    line = geometry.LineString(polygon)
    point = geometry.Point(Points)
    polygon = geometry.Polygon(line)
    return polygon.contains(point)

def output_func(line_per_proc, proc_id, bikes, fences, proc_num):
    l = line_per_proc if proc_id < proc_num - 1 else len(bikes) - (proc_num - 1) * line_per_proc
    shift = line_per_proc * proc_id
    out_bikes = defaultdict(list)
    for i in range(l):
        la = bikes.iloc[i + shift, 1]
        lo = bikes.iloc[i + shift, 2]
        point = (la, lo)
        nearest, fence_pos, dis = find_nearest(point, fences)
        out_bikes['BIKE_ID'].append(bikes['BICYCLE_ID'][i + shift])
        out_bikes['BIKE_LATITUDE'].append(la)
        out_bikes['BIKE_LONGITUDE'].append(lo)
        out_bikes['TIME'].append(bikes['UPDATE_TIME'][i + shift])
        out_bikes['FENCE_LATITUDE'].append(nearest[0])
        out_bikes['FENCE_LONGITUDE'].append(nearest[1])
        out_bikes['FENCE_LATITUDE_0'].append(fence_pos[0][0])
        out_bikes['FENCE_LONGITUDE_0'].append(fence_pos[0][1])
        out_bikes['FENCE_LATITUDE_1'].append(fence_pos[1][0])
        out_bikes['FENCE_LONGITUDE_1'].append(fence_pos[1][1])
        out_bikes['FENCE_LATITUDE_2'].append(fence_pos[2][0])
        out_bikes['FENCE_LONGITUDE_2'].append(fence_pos[2][1])
        out_bikes['FENCE_LATITUDE_3'].append(fence_pos[3][0])
        out_bikes['FENCE_LONGITUDE_3'].append(fence_pos[3][1])
        out_bikes['DISTANCE'].append(dis)
        if is_inside(fence_pos, point):
            out_bikes['IS_INSIDE'].append(1)
        else:
            out_bikes['IS_INSIDE'].append(0)
        if proc_id == 0:
            print('row ' + str(i + shift) + ' finished on process ' + str(proc_id))
    fname = './middleware/bike_detail' + str(proc_id) + '.csv'
    out_bikes = pd.DataFrame(out_bikes)
    out_bikes.to_csv(fname, index = False)

if __name__ == '__main__':
    if not os.path.exists('./middleware'):
        os.mkdir('./middleware')

    fences = pd.read_csv('./cleaned_data/fence_position.csv')
    bikes = pd.read_csv('./cleaned_data/required_bike_order.csv')

    out_bikes = pd.DataFrame()
    proc_num = 11
    line_per_proc = len(bikes)//(proc_num - 1) 
    pool = multiprocessing.Pool(processes = proc_num)
    for i in range(proc_num):
        pool.apply_async(output_func, args = (line_per_proc,i, bikes, fences, proc_num))

    pool.close()
    pool.join()
    


