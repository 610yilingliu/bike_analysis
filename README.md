# Python环境
Python 3.7

# 安装依赖库

`pip install -r requirements.txt` 或 `pip3 install -r requirements.txt`
若系统为windows, 请使用conda安装shapely库

# 文件说明:

## `./tools`
其中包括所有代码文件

### `./tools/SQL
数据挖掘时用到的SQL文件,运行环境为Microsoft SQL Server

#### `find_ubnormal_orders.sql`
各行代码功能见文件注释. bike_detail table 是由`./cleaned_data/bike_detail.csv`导入的. 输出为`./cleaned_data/middlewares/bikes_7-9.csv`

#### `seperate_by_day.sql`
将"日"维度加入数据 removed_abnormal 由`/cleaned_data/middlewares/removed_abnormal.csv`导入而成, 输出为`./cleaned_data/bikes_data.csv`

### './tools/fence_position.py
输入`gxdc_tcd.csv`, 输出`./cleaned_data/fence_position.csv`.

将停车围栏几何形状拆分为10个单独的特征,并加入中心坐标,面积,所属路名, 数字编号, 长, 宽

### `./tools/hashing.py`
输入`./cleaned_data/fence_position.csv`与`gxdc_dd.csv`. 输出`./cleaned_data/middlewares/fence_grids.json`, `./cleaned_data/middlewares/hashed_bikes.csv`

提取出每个围栏对应的geohash方格(9-36个), 用字典保存为json; 在单车数据中加入单车所处geohash方格和共享单车数字编号

### `tools/find_nearest.py`
输入: `./cleaned_data/middlewares/fence_grids.json`, `./cleaned_data/middlewares/hashed_bikes.csv`, `./cleaned_data/fence_position.csv`. 输出`./cleaned_data/middlewares/bike_detail.csv`

找出与每辆自行车距离最近的围栏, 并计算自行车到围栏边界的距离.若自行车离围栏153米-306米以上则无法找到最近围栏,直接当乱停车数据处理,最近围栏与距离都计为-1

### `tools/remove_abnormal_script.py`

输入: `./cleaned_data/middlewares/bikes_7-9.csv`. 输出`/cleaned_data/middlewares/removed_abnormal.csv`

移除异常开/关锁数据

### `tools/visualize.ipynb`

可视化长乐路,长浩路数据进行预览

### `tools/solution.ipynb`

**任务一解决方案主文件**

### `tools/suggestions.ipynb`

**任务二调度方案示例(使用地理距离, 因无法获得图数据所以暂不采用最短路算法)**



## `./data`

使用到的原始数据文件

## `./cleaned_data`

经过tools中SQL命令,python代码等处理原始数据文件后得到的文件, 各文件来源详见tools.
其中suggestions文件夹下文件为任务一输出, 来源可见,`./toools/solution.ipynb`