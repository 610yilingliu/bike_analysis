import json
import collections
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.ops import nearest_points
from geopy.distance import geodesic

def grid_dict(jsonpath):
    """
    type jsonpath: String, the path where stores fenceID and its grids
    """
    f=open(jsonpath,"r")
    content=f.readline()
    f.close()
    fence_grid = json.loads(content)
    grid_fence = collections.defaultdict(set)
    for k, v in fence_grid.items():
        for grid in v:
            grid_fence[grid].add(k)
    return grid_fence

def load_bikes(fpath):
    df = pd.read_csv(fpath)
    info = dict()
    for i in range(len(df)):
        bike_id = df["BID"][i]
        lat = df["LATITUDE"][i]
        lon = df["LONGITUDE"][i]
        grid = df["GRID"][i]
        info[bike_id] = (grid, (lat, lon))
    return info

def comp_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)

def nearest_fence(bike_info, grid_fence, fence_path, bike_path, target_path):
    bike_detail = pd.read_csv(bike_path)
    fence_detail = pd.read_csv(fence_path)
    bike_fence = dict()
    for k in bike_info:
        print("Processing Nearest Fence of Bike " + str(k))
        curgrid, pos = bike_info[k]
        if curgrid not in grid_fence:
            bike_fence[k] = -1
        else:
            fences = grid_fence[curgrid]
            ans_fence = -1
            min_dist = float('inf')
            for f in fences:
                idx = int(f)
                fence_latitude = fence_detail["LATITUDE"][idx]
                fence_longitude = fence_detail["LONGITUDE"][idx]
                fence_pos = (fence_latitude, fence_longitude)
                curdist = comp_distance(pos, fence_pos)
                if curdist < min_dist:
                    min_dist = curdist
                    ans_fence = idx
            bike_fence[k] = ans_fence
    related_fence = [-1] * len(bike_detail)
    distance = [-1] * len(bike_detail)
    for bike in bike_fence:
        print("Counting Distance For Bike " + bike)
        bike_index = int(bike)
        fence = bike_fence[bike]
        if fence == -1:
            continue
        related_fence[bike_index] = fence
        la0, lo0, la1, lo1, la2, lo2, la3, lo3, la4, lo4 = fence_detail['LATITUDE_0'][fence], fence_detail['LONGITUDE_0'][fence], fence_detail['LATITUDE_1'][fence], fence_detail['LONGITUDE_1'][fence], fence_detail['LATITUDE_2'][fence], fence_detail['LONGITUDE_2'][fence], fence_detail['LATITUDE_3'][fence], fence_detail['LONGITUDE_3'][fence], fence_detail['LATITUDE_4'][fence], fence_detail['LONGITUDE_4'][fence]
        polygon_data = [[la0, lo0], [la1, lo1], [la2, lo2], [la3, lo3], [la4, lo4]]
        point_data = [bike_detail['LATITUDE'][bike_index], bike_detail['LONGITUDE'][bike_index]]
        polygon = Polygon(polygon_data)
        point = Point(point_data)
        boundary_obj = nearest_points(polygon, point)[0]
        nearest_point = boundary_obj.bounds[:2]
        dist = geodesic(point_data, nearest_point).meters
        distance[bike_index] = dist
    bike_detail['NEAREST_FENCE'] = related_fence
    bike_detail['DISTANCE'] = distance
    bike_detail.to_csv(target_path)

if __name__ == '__main__':
    jspath = "./cleaned_data/middlewares/fence_grids.json"
    grid_fence = grid_dict(jspath)
    bike_path = './cleaned_data/middlewares/hashed_bikes.csv'
    bike_info = load_bikes(bike_path)
    fence_path = './cleaned_data/fence_position.csv'
    target_path = './cleaned_data/middlewares/bike_detail.csv'
    nearest_fence(bike_info, grid_fence, fence_path, bike_path, target_path)
