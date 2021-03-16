-- 删除7点之前和9点之后的数据, 输出为bikes_7-9.csv
select BID, BICYCLE_ID, LATITUDE, LONGITUDE,LOCK_STATUS, UPDATE_TIME, GRID, NEAREST_FENCE, DISTANCE from 
(select *, datepart(hh, UPDATE_TIME) as happen_hour from bike_detail) as t1 where t1.happen_hour >= 7 and t1.happen_hour < 9 order by BICYCLE_ID, UPDATE_TIME

-- 观察一共有多少辆车
select distinct BICYCLE_ID from bike_detail

-- 观察开/关锁异常数据
select
distinct t1.BICYCLE_ID
from 
(select ROW_NUMBER() over (order by BICYCLE_ID, UPDATE_TIME) as row, * from bike_detail) as t1,  
(select ROW_NUMBER() over (order by BICYCLE_ID, UPDATE_TIME) as row, * from bike_detail) as t2 where
t1.BICYCLE_ID = t2.BICYCLE_ID
and t2.row = t1.row + 1
and t1.LOCK_STATUS = t2.LOCK_STATUS
and DATEDIFF(hour, t1.UPDATE_TIME, t2.UPDATE_TIME) < 5

-- lock_status = 0: 开锁, 1: 关锁
-- 选一个异常数据进行观察
select * from bike_detail where BICYCLE_ID = '001ca978928d0e762aaede9118e3c7e6' order by UPDATE_TIME;