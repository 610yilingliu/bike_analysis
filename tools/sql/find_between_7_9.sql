-- lock_status = 0: 开锁, 1: 关锁
--​任务一：为更好地掌握早高峰潮汐现象的变化规律与趋势，参赛者需基于主办方提供的数据进行数据分析和计算模型构建等工作，识别出工作日早高峰07:00-09:00潮汐现象最突出的40个区域
--，列出各区域所包含的共享单车停车点位编号名称，并提供计算方法说明及计算模型，为下一步优化措施提供辅助支撑。 
--任务二：参赛者根据任务一Top40区域计算结果进一步设计高峰期共享单车潮汐点优化方案，通过主动引导停车用户到邻近停车点位停车，进行削峰填谷，缓解潮汐点停车位（如地铁口）的拥堵问题。
--允许参赛者自带训练数据，但需在参赛作品中说明所自带数据的来源及使用方式，并保证其合法合规。
--（城市公共自行车从业者将发生在早晚高峰时段共享单车“借不到、还不进”的问题称之为“潮汐”现象。本题涉及的“潮汐现象”聚焦“还不进”的问题，识别出早高峰共享单车最淤积的40个区域）
select top 1 * from (select convert(time, UPDATE_TIME) as dtime, * from gxdc_dd) as t1 where t1.LOCK_STATUS = 1 order by t1.dtime asc;
select top 1 * from (select convert(time, UPDATE_TIME) as dtime, * from gxdc_dd) as t1 where t1. LOCK_STATUS = 0 order by t1.dtime desc;
select BICYCLE_ID, LATITUDE, LONGITUDE, convert(smalldatetime, UPDATE_TIME) as UPDATE_TIME from (select *, datepart(hh, UPDATE_TIME) as happen_hour from gxdc_dd) as t1
where t1.happen_hour >= 7 and t1.happen_hour < 9 and LOCK_STATUS = 1;
select BICYCLE_ID, LATITUDE, LONGITUDE, convert(smalldatetime, UPDATE_TIME) as UPDATE_TIME from (select *, datepart(hh, UPDATE_TIME) as happen_hour from gxdc_dd) as t1
where t1.happen_hour >= 7 and t1.happen_hour < 9 and LOCK_STATUS = 0 ;