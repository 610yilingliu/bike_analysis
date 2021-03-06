select BID, BICYCLE_ID, LATITUDE, LONGITUDE,LOCK_STATUS, UPDATE_TIME, GRID, NEAREST_FENCE, DISTANCE from 
(select *, datepart(hh, UPDATE_TIME) as happen_hour from bike_detail) as t1 where t1.happen_hour >= 7 and t1.happen_hour < 9 order by BICYCLE_ID, UPDATE_TIME

select distinct BICYCLE_ID from bike_detail

select distinct t1.BICYCLE_ID
--, t1.UPDATE_TIME, t1.LOCK_STATUS, t1.BID 
from 
(select * from bike_detail) as t1,  (select * from bike_detail) as t2 where
t1.BICYCLE_ID = t2.BICYCLE_ID 
and t1.LOCK_STATUS = t2.LOCK_STATUS
and DATEDIFF(minute, t1.UPDATE_TIME, t2.UPDATE_TIME) < 1
and DATEDIFF(second, t1.UPDATE_TIME, t2.UPDATE_TIME) > 1 order by BICYCLE_ID

-- lock_status = 0: ¿ªËø, 1: ¹ØËø
select * from bike_detail where BICYCLE_ID = '0045909aeab0de6d806a37505bd38a2d' order by UPDATE_TIME;