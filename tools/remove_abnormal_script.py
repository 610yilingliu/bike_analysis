# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import time
import pandas as pd
# 禁用科学计数法
pd.set_option('display.float_format',lambda x : '%.2f' % x)


# %%
bikes = pd.read_csv('./cleaned_data/bikes_7-9.csv')


# %%
bikes.head()


# %%
def convert_time(time_str):
    """
    example: 2020-12-21 08:23:32.0000000
    """
    time_str = time_str.strip()
    ymd, hmis = time_str.split(' ')
    y, m, d = ymd.split('-')
    y, m, d = int(y), int(m), int(d)
    h, mi, s = hmis.split(':')
    h, mi, s = int(h), int(mi), int(float(s))
    time_tuple = (y, m, d, h, mi, s, 0, 0, 0)
    return time.mktime(time_tuple)


# %%
bikes['MKTIME'] = bikes['UPDATE_TIME'].apply(convert_time)


# %%
bikes.head()


# %%
cleaned_df = pd.DataFrame(columns = bikes.columns)
cleaned_df.loc[0] = bikes.iloc[0]


# %%
fast = 1
slow = 0
tmp_row = None
if bikes['LOCK_STATUS'][0] == 0:
    cleaned_df.loc[slow] = bikes.iloc[0]
    slow += 1
else:
    tmp_row = bikes.iloc[0]
# 对于连续的开锁数据,保留第一个(0)
# 对于连续的关锁数据,保留最后一个(1)
fast = 1
slow = 0
tmp_row = None
if bikes['LOCK_STATUS'][0] == 0:
    cleaned_df.loc[slow] = bikes.iloc[0]
    slow += 1
else:
    tmp_row = bikes.iloc[0]
# 对于连续的开锁数据,保留第一个(0)
# 对于连续的关锁数据,保留最后一个(1)
while fast < len(bikes):
    print(fast, slow)
    if bikes['BICYCLE_ID'][fast] != bikes['BICYCLE_ID'][fast - 1]:
        if tmp_row is not None:
            cleaned_df.loc[slow] = tmp_row
            slow += 1
            tmp_row = None
        if bikes['LOCK_STATUS'][fast] == 1:
            tmp_row = bikes.loc[fast]
            fast += 1
        else:
            cleaned_df.loc[slow] = bikes.loc[fast]
            print(fast, slow)
            slow += 1
            fast += 1
    else:
        # 间隔如果大于一天.这里是乱填的一个可用数字
        if bikes['MKTIME'][fast] - bikes['MKTIME'][fast - 1] > 20000:
            if tmp_row is not None:
                cleaned_df.loc[slow] = tmp_row
                slow += 1
                tmp_row = None
            if bikes['LOCK_STATUS'][fast] == 1:
                tmp_row = bikes.loc[fast]
                fast += 1
            else:
                cleaned_df.loc[slow] = bikes.loc[fast]
                print(fast, slow)
                slow += 1
                fast += 1
        # 间隔如果小于一天,那么判断是否为异常数据.
        else:
            if bikes['LOCK_STATUS'][fast] == 0:
                # 不异常时的开锁:如果temp中存了关锁,把temp中的关锁放出来加入到新的df,把当前的开锁也加入新的df
                if bikes['LOCK_STATUS'][fast - 1] == 1:
                    cleaned_df.loc[slow] = tmp_row
                    slow += 1
                    tmp_row = None
                    cleaned_df.loc[slow] = bikes.loc[fast]
                    fast += 1
                    slow += 1
                # 异常值, 跳过
                else:
                    fast += 1
            else:# if bikes['LOCK_STATUS'][fast] == 1, 开锁.无论如何直接关进tmp_row
                tmp_row= bikes.loc[fast]
                fast += 1
if tmp_row is not None:
    cleaned_df.loc[slow] = tmp_row

cleaned_df.to_csv('./cleaned_data/removed_abnormal.csv')
# %%



