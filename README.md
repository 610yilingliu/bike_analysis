# 2021-04-23更新:

改为全python处理,增加preview.ipynb,逻辑更为清晰.并且将原始的看起来很恶心的python原生方式(我自己看了都觉得恶心那种)改为使用pandas去除异常数据,代码效率更高(pandas底层使用numpy,内置了多线程)

原先代码中存在轻微影响算法结论的bug(会使cluster1453取代cluster286成为第40拥挤的簇),现一并修复(不影响应用结论)

# Python环境
Python 3.7

# 安装依赖库

`pip install -r requirements.txt` 或 `pip3 install -r requirements.txt`
若系统为windows, 请使用conda安装shapely库

# 文件说明:

## `./tools`
其中包括所有代码文件

### './tools/fence_position.py
输入`gxdc_tcd.csv`, 输出`./cleaned_data/fence_position.csv`.

将停车围栏几何形状拆分为10个单独的特征,并加入中心坐标,面积,所属路名, 数字编号, 长, 宽

### './tools/preview.ipynb
数据的预览与异常数据清洗, 输出`./cleaned_data/middlewares/removed_abnormal.csv`

### `./tools/hashing.py`
输入`./cleaned_data/fence_position.csv`与`./cleaned_data/middlewares/removed_abnormal.csv`. 输出`./cleaned_data/middlewares/fence_grids.json`, `./cleaned_data/middlewares/hashed_bikes.csv`

提取出每个围栏对应的geohash方格(9-36个), 用字典保存为json; 在单车数据中加入单车所处geohash方格和共享单车数字编号

### `tools/find_nearest.py`
输入: `./cleaned_data/middlewares/fence_grids.json`, `./cleaned_data/middlewares/hashed_bikes.csv`, `./cleaned_data/fence_position.csv`. 输出`./cleaned_data/bikes_data.csv`

找出与每辆自行车距离最近的围栏, 并计算自行车到围栏边界的距离.若自行车离围栏153米-306米以上则无法找到最近围栏,直接当乱停车数据处理,最近围栏与距离都计为-1

### `tools/visualize.ipynb`

可视化长乐路,长浩路数据进行预览

### `tools/solution.ipynb`

**任务一解决方案主文件**

### bike_app
基于flask的调度算法DEMO,请参阅其中readme.md进行安装


## `./data`

使用到的原始数据文件

## `./cleaned_data`

经过tools中SQL命令,python代码等处理原始数据文件后得到的文件, 各文件来源详见tools.
其中suggestions文件夹下文件为任务一输出, 来源可见,`./toools/solution.ipynb`