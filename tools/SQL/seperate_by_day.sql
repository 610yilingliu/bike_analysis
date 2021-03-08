select datepart(dd, UPDATE_TIME) as DAY, * from removed_abnormal order by NEAREST_FENCE, UPDATE_TIME

select * from (select datepart(dd, UPDATE_TIME) as DAY, * from removed_abnormal) as t1
where
t1.LOCK_STATUS = 0 and t1.DAY = 21

select * from (select datepart(dd, UPDATE_TIME) as DAY, * from removed_abnormal) as t1
where
t1.LOCK_STATUS = 1 and t1.DAY = 21

select * from (select datepart(dd, UPDATE_TIME) as DAY, * from removed_abnormal) as t1
where
t1.LOCK_STATUS = 0 and t1.DAY = 22

select * from (select datepart(dd, UPDATE_TIME) as DAY, * from removed_abnormal) as t1
where
t1.LOCK_STATUS = 1 and t1.DAY = 22