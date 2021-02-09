-- lock_status = 0: ¿ªËø, 1: ¹ØËø
select top 1 * from (select convert(time, UPDATE_TIME) as dtime, * from gxdc_dd) as t1 where t1.LOCK_STATUS = 1 order by t1.dtime asc;
select top 1 * from (select convert(time, UPDATE_TIME) as dtime, * from gxdc_dd) as t1 where t1. LOCK_STATUS = 0 order by t1.dtime desc;
select BICYCLE_ID, LATITUDE, LONGITUDE, LOCK_STATUS, convert(smalldatetime, UPDATE_TIME) as UPDATE_TIME from (select *, datepart(hh, UPDATE_TIME) as happen_hour from gxdc_dd) as t1
where ((t1.happen_hour < 9 and LOCK_STATUS = 0) or (t1.happen_hour > 7 and LOCK_STATUS = 1));