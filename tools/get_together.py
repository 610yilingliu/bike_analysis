import os
import pandas as pd

files = os.listdir('./middleware')

out_data = pd.DataFrame()
for fname in files:
    if fname.endswith('.csv'):
        df = pd.read_csv('./middleware/' +fname)
        out_data = pd.concat([out_data, df], ignore_index= True)

out_data.to_csv('./cleaned_data/gathered_bike_data.csv', index = False)