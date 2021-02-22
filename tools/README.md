所有代码文件的作用，及其产物。产物若无特殊说明均存储在cleaned_data文件夹下

sql环境是Microsoft SQL Server

## fence_position.py

将 gxdc_tcd.csv中的fence_loc(由五个点组成, 第五个点的坐标等于第一个点，相当于围成一个四边形)即停车栅栏坐标转换为八个Attribute（四边形四个点的经度，纬度）方便处理，并计算出栅栏中心点(Attribute: LATITUDE, LONGITUDE).并提取停车点所属的路名，Attribute：ROAD

**产物：fence_position.csv**

## road_grouping.py

将fence_position.csv中的数据按路名进行分类，将每一路中包括的停车点中心点坐标存储在dictionary内并输出位json文件

**产物：road_locs.json**

## sql/find_between_7_9

从gxdc_tcd.csv（已导入数据库）中提取出7点至9点之间的【锁车】数据

**产物：required_bike_order.csv**

## is_in.py

使用fence_position.csv和required_bike_order.csv计算出离required_bike_order.csv中离共享单车锁车点最近的停车点，并计算出距离

**产物：data文件夹中所有文件（使用了多进程并行计算，我自己只写过C下的openmp/mpi代码，为保险起见还是直接输出多个文件了）**

## get_together.py

简单的合并一下data文件夹中文件

**产物：gathered_bike_data.csv**

## sql/final.sql

将gathered_bike_data.csv导入到数据库中的table和fence_position.csv导入到数据库中的table做left join，形成最终整理后文件

**产物：bike_loc_final.csv**

## geo_visualize.ipynb

预览及聚类