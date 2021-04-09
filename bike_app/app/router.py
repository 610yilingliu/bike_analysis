import json
import geohash
import requests
import pandas as pd
from app import app
from flask_wtf import FlaskForm
from flask import render_template, request, flash
# from wtforms import FloatField, SubmitField, IntegerField
# from geopy.distance import geodesic
# from shapely.geometry import Point
# from shapely.geometry.polygon import Polygon
# from shapely.ops import nearest_points

grid_fences_path = './app/source/grid_fences.json'
f=open(grid_fences_path,"r")
grid_json_content = f.readline()
f.close()
grid_fence = json.loads(grid_json_content)
fences = pd.read_csv('./app/source/fences_filled.csv')

dist_weight = 0.5
active_day_weight = 0.2
flow_weight = 0.3



def point_grids(point):
    """
    :type point: Tuple or List, format: (Latitude, Longitude)
    :rtype: List, related geohash grids to current point
    """
    center = geohash.encode(point[0], point[1], 7)
    # 将center扩展为九宫格,避免"错误最近点"现象出现
    nears = geohash.expand(center)
    return [center] + nears


@app.route('/', methods=['GET', 'POST'])
def index():
    def get_zscore(dfseries):
            return (dfseries - dfseries.mean())/dfseries.std()

    if request.method == 'POST':
        latitude = request.form['la']
        longitude = request.form['lo']
        max_dist = request.form['mx_dist']
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            max_dist = float(max_dist)
        except:
            flash('无效输入,请确保输入的都是半角数字')
            return render_template('index.html')
        if max_dist < 0:
            flash('最大距离不得小于0')
            return render_template('index.html')
        bike_pos = (round(latitude, 6), round(longitude,6))
        bike_grids = point_grids(bike_pos)
        near_fences = []
        for grid in bike_grids:
            if grid in grid_fence:
                near_fences += grid_fence[grid]
        near_fences = list(set(near_fences))
        if not near_fences:
            flash('您距离共享单车围栏太远了,无法匹配','warning')
            return render_template('index.html')
        near_f, mixed_score, active_days, distances, density, flow, las, los = [], [], [], [], [], [], [], []
        # point = Point(bike_pos)
        for fid in near_fences:
            fid = int(fid)
            curfence_mixed_score = fences.loc[fid, 'MIXED_SCORE']
            curfence_active_day = fences.loc[fid, 'ACTIVE_DAYS']
            # curfence_position = fences.iloc[fid, 2:12]
            curfence_density = fences.loc[fid, 'FLOW_DENSITY']
            curfence_flow = fences.loc[fid, 'FLOW']
            la = round(fences.loc[fid, 'F_LATITUDE'], 6)
            lo = round(fences.loc[fid, 'F_LONGITUDE'], 6)
            # polygon_data = []
            # for i in range(0, 10, 2):
            #     polygon_data.append((curfence_position[i], curfence_position[i + 1]))
            # polygon = Polygon(polygon_data)
            # boundary_obj = nearest_points(polygon, point)[0]
            # nearest_point = boundary_obj.bounds[:2]
            # dist = geodesic(bike_pos, nearest_point).meters
            r = requests.get("http://api.map.baidu.com/direction/v2/riding?origin={}, {}&destination={},{}&ak=你的百度api密钥".format(bike_pos[0], bike_pos[1], la, lo))
            if r.status_code != 200:
                continue
            r_text = r.text
            data = json.loads(r_text)
            try:
                dist = data['result']['routes'][0]['distance']
            except:
                continue
            if dist <= max_dist:
                mixed_score.append(curfence_mixed_score)
                active_days.append(curfence_active_day)
                distances.append(dist)
                near_f.append(fid)
                flow.append(curfence_flow)
                density.append(curfence_density)
                las.append(la)
                los.append(lo)
        if not mixed_score:
            flash(str(max_dist) + '米内没有找到共享单车围栏')
            return render_template('index.html')
        near_df = pd.DataFrame()
        near_df['FID'] = near_f
        near_df['ACTIVE_DAYS'] = active_days
        near_df['DENSITY'] = density
        near_df['FLOW'] = flow
        near_df['MIXED_SCORE'] = mixed_score
        near_df['DISTANCE'] = distances
        near_df['LATITUDE'] = las
        near_df['LONGITUDE'] = los
        near_df['SCORE'] = get_zscore(near_df['ACTIVE_DAYS']) * active_day_weight + get_zscore(near_df['MIXED_SCORE']) * flow_weight + get_zscore(near_df['DISTANCE']) * dist_weight
        sorted_df = near_df.sort_values("SCORE")
        # near_fence_todraw = [(x, y) for x, y in zip(sorted_df['LATITUDE'].iloc[1:], sorted_df['LONGITUDE'].iloc[1:])]
        target_fence = (sorted_df['LATITUDE'].iloc[0], sorted_df['LONGITUDE'].iloc[0])
        idx = sorted_df['FID'].iloc[0]
        fence_name = fences['FENCE_ID'][idx]
        dist = sorted_df['DISTANCE'].iloc[0]
        flow_there = sorted_df['FLOW'].iloc[0]
        density_there = sorted_df['DENSITY'].iloc[0]
        baidu_map = "http://api.map.baidu.com/direction?origin=latlng:{},{}|name:当前坐标&destination=latlng:{},{}|name:{}&mode=walking&region=厦门&output=html&src=webapp.baidu.openAPIdemo".format(bike_pos[0], bike_pos[1], target_fence[0], target_fence[1], '目标停车点')

        return render_template('index.html', m = baidu_map, flow = flow_there, density = density_there, fence_name = fence_name, dist = dist, table = sorted_df.to_html(classes='sorted_df'), titles=sorted_df.columns.values)
    return render_template('index.html')
        







