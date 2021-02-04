import pandas as pd

df = pd.read_csv('./cleaned_data/fance_position.csv')
points = []

for i in range(len(df)):
    la = df['LATITUDE'][i]
    lo = df['LONGITUDE'][i]
    points.append((la, lo))

points.sort()

def find_nearest(p, ls):
    




    


