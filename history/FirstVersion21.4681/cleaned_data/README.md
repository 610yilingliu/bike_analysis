# 数据说明

## fence_position.csv

FENCE_ID: 停车围栏名

LATITUDE: 停车围栏坐标中心点(用于可视化停车围栏)纬度

LONGITUDE: 停车围栏坐标中心点(用于可视化停车围栏)经度

ROAD: 所属路名(如:长乐路)

## road_locs.json

key: 路名

value: [(纬度,经度), (纬度,经度), (纬度,经度) ......]

读取后使用json.loads即可转换为字典.代码示例:

```
file=open("road_locs.json","r")
content=file.readline()
file.close()
print(json.loads(content))
```