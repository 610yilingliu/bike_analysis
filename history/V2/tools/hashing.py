import geohash
# Reference
# https://www.movable-type.co.uk/scripts/geohash.html
# https://pypi.org/project/python-geohash/
import json
import pandas as pd


def point_grids(point):
    """
    type point: Tuple or List, format: (Latitude, Longitude)
    """
    center = geohash.encode(point[0], point[1], 7)
    nears = geohash.expand(center)
    return [center] + nears

def fence_grids(points):
    """
    type points: List[(Float, Float)], with 4 tuples: p1, p2, p3, p4: position or 4 corner points of a polygon(fence)
    """
    p1, p2, p3, p4 = points
    p1_g, p2_g, p3_g, p4_g = point_grids(p1), point_grids(p2), point_grids(p3), point_grids(p4)
    return list(set(p1_g + p2_g + p3_g + p4_g))

def export_fence_grids(df, fname):
    """
    df: pandas DataFrame from fence_position.csv
    fname: String, name of binary file
    export: binary file
    """
    json_dic = dict()
    for i in range(len(df)):
        points = []
        la_prefix = 'LATITUDE'
        lo_prefix = 'LONGITUDE'
        for num in range(4):
            suffix = '_' + str(num)
            la_key = la_prefix + suffix
            lo_key = lo_prefix + suffix
            points.append((df[la_key][i], df[lo_key][i]))
        grids = fence_grids(points)
        json_dic[int(df['FID'][i])] = grids

    f = open('./cleaned_data/' + fname, 'w')
    f.write(json.dumps(json_dic))
    f.close()

def hash_bikes(bike_data, outpath):
    df = pd.read_csv(bike_data)
    bike_grid = []
    bike_name = []
    for i in range(len(df)):
        la = df['LATITUDE'][i]
        lo = df['LONGITUDE'][i]
        curgrid = geohash.encode(la, lo, 7)
        bike_grid.append(curgrid)
        bike_name.append(i)
    df['GRID'] = bike_grid
    df['BID'] = bike_name
    df.to_csv(outpath, index = False)



if __name__ == '__main__':
    df = pd.read_csv('./cleaned_data/fence_position.csv')
    export_fence_grids(df, 'fence_grids.json')
    hash_bikes('./data/gxdc_dd.csv', './cleaned_data/hashed_bikes.csv')

