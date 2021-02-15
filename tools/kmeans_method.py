import os
import sys
import time
import json
import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn import metrics
from sklearn.cluster import KMeans


df = pd.read_csv('./cleaned_data/fence_position.csv')
las, los = df['LATITUDE'].tolist(), df['LONGITUDE'].tolist()

def norm(ls, scaled_min = 0, scaled_max = 1):
    """
    Project whole list to [scaled_min, scaled_max]. Default normalization
    :type ls: List[int]
    :type scaled_min, scaled_max: int
    """
    ans = []
    mi, mx = min(ls), max(ls)
    for num in ls:
        cur = scaled_min + (mx - num)/(mx - mi) * (scaled_max - scaled_min)
        ans.append(cur)
    return ans

class Logger(object):
    """
    Logging module
    """
    def __init__(self, filename, stream=sys.stdout):
	    self.terminal = stream
	    self.log = open(filename, "wb", buffering=0)

    def write(self, *message):
        message = ",".join([str(it) for it in message])
        self.terminal.write(str(message))
        prefix = '[' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ']'
        self.log.write(prefix.encode('utf-8') + str(message).encode('utf-8'))

    def flush(self):
        pass

def time_helper(seperator = '_', to_sec = True):
    """
    return a string like 2020_09_11_22_43_00 (if to_sec is True) or 2020_09_11_22_43 (if to_sec is False)
    """
    if to_sec:
        return time.strftime("%Y" + seperator + "%m" + seperator + "%d" + seperator + "%H" + seperator + "%M" + seperator + "%S", time.localtime()) 
    return time.strftime("%Y" + seperator + "%m" + seperator + "%d" + seperator + "%H" + seperator + "%M", time.localtime()) 

if not os.path.exists('./log'):
    os.mkdir('./log')
start_time = time_helper()
sys.stdout = Logger('./log/' + start_time + '.log')

x = list(zip(norm(las), norm(los)))
ans = []
ans_clusters = 0
mx_score = 0
score_k = dict()
for i in range(40, 5000, 200):
    score = 0
    # for ran_seed in range(5):
        # too much calculations, require distributed system if you have
    y_pred = KMeans(n_clusters = i, random_state = 1).fit_predict(x)
    cur_score = metrics.calinski_harabasz_score(x, y_pred)
    score += cur_score
    # score = score/5
    print(round(score, 3), i)
    score_k[i] = score
    if score > mx_score:
        score = mx_score
        ans  = y_pred
        ans_clusters = i

jsobj = json.dumps(score_k)
f=open("./cleaned_data/kmeans_score.json","w")
f.write(json.dumps(jsobj))
f.close()

print("Maximum score happend in k = " + str(ans_clusters))
df["Group"] = ans
df.to_csv("./cleaned_data/grouped_data_after_kmeans.csv")
