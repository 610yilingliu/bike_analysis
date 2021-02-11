import os
import sys
import time
import multiprocessing
import pandas as pd
from math import sqrt
from collections import defaultdict



class Logger(object):
    """
    Logging module
    """
    def __init__(self, filename, stream=sys.stdout):
	    self.terminal = stream
	    self.log = open(filename, "wb", buffering=0)

    def write(self, *message):
        message = ",".join([str(it) for it in message])
        self.terminal.write(str(message))
        prefix = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']'
        self.log.write(prefix.encode('utf-8') + str(message).encode('utf-8'))

    def flush(self):
        pass

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
        curdis = sqrt((point[0] - p[0]) * (point[0] - p[0]) + (point[1] - p[1]) * (point[1] - p[1]))

        if curdis < min_dis:
            min_dis = curdis
            mi_point = point
            x1, y1, x2, y2, x3, y3, x4, y4 = df['LATITUDE_0'][i], df['LONGITUDE_0'][i], df['LATITUDE_1'][i], df['LONGITUDE_1'][i], df['LATITUDE_2'][i], df['LONGITUDE_2'][i], df['LATITUDE_3'][i], df['LONGITUDE_3'][i]
    return mi_point, (x1, y1, x2, y2, x3, y3, x4, y4)

def is_inside(point, region):
    def cross(x_1, y_1, x_2, y_2, xt, yt):
        return (x_2 - x_1) * (yt - y_1) - (xt - x_1) * (y_2 - y_1)
    x, y = point
    x1, y1, x2, y2, x3, y3, x4, y4 = region
    return cross(x1, y1, x2, y2, x, y) * cross(x3, y3, x4, y4, x, y) >= 0 and cross(x2, y2, x3, y3, x, y) * cross(x4, y4, x1, y1, x, y) >= 0


if not os.path.exists('./log'):
    os.mkdir('./log')
start_time = time_helper()
sys.stdout = Logger('./log/' + start_time + '.log')




def output_func(line_per_proc, proc_id, bikes, fences):
    l = line_per_proc if proc_id < proc_num - 1 else len(bikes) - (proc_num - 1) * line_per_proc
    shift = line_per_proc * proc_id
    out_bikes = defaultdict(list)
    for i in range(l):
        la = bikes.iloc[i + shift, 1]
        lo = bikes.iloc[i + shift, 2]
        point = (la, lo)
        nearist, fence_pos = find_nearest(point, fences)

        out_bikes['BIKE_ID'].append(bikes.iloc[i + shift, 0])
        out_bikes['BIKE_LATITUDE'].append(la)
        out_bikes['BIKE_LONGITUDE'].append(lo)
        out_bikes['TIME'].append(bikes.iloc[i + shift, 3])
        out_bikes['FENCE_LATITUDE'].append(nearist[0])
        out_bikes['FENCE_LONGITUDE'].append(nearist[1])
        out_bikes['FENCE_LATITUDE_0'].append(fence_pos[0])
        out_bikes['FENCE_LONGITUDE_0'].append(fence_pos[1])
        out_bikes['FENCE_LATITUDE_1'].append(fence_pos[2])
        out_bikes['FENCE_LONGITUDE_1'].append(fence_pos[3])
        out_bikes['FENCE_LATITUDE_2'].append(fence_pos[4])
        out_bikes['FENCE_LONGITUDE_2'].append(fence_pos[5])
        out_bikes['FENCE_LATITUDE_3'].append(fence_pos[6])
        out_bikes['FENCE_LONGITUDE_3'].append(fence_pos[7])
        if is_inside(point, fence_pos):
            out_bikes['IS_INSIDE'].append(1)
        else:
            out_bikes['IS_INSIDE'].append(0)
        print('row ' + str(i + shift) + ' finished')
    out_bikes = pd.DataFrame(out_bikes)
    return out_bikes

if __name__ == '__main__':
    fences = pd.read_csv('./cleaned_data/fence_position.csv')
    bikes = pd.read_csv('./cleaned_data/required_bike_order.csv')
    results = []
    proc_num = 10
    line_per_proc = len(bikes)//(proc_num - 1) 
    p = multiprocessing.Pool(proc_num)
    for i in range(proc_num):
        r = p.apply_async(output_func, args=(line_per_proc, i, bikes, fences))
        results.append(r)
    p.close()
    p.join()
    out_bikes = pd.concat(results, axis = 1)
    print(out_bikes.sample(5))
    out_bikes.to_csv('out_bikes.csv')
    


