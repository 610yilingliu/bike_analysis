import os
import pandas as pd

root = './middleware/out/'
files = os.listdir(root)

out_data = pd.DataFrame()
for fname in files:
    if fname.endswith('.csv'):
        df = pd.read_csv(root +fname)
        out_data = pd.concat([out_data, df], ignore_index= True)

out_data.to_csv('./cleaned_data/gathered_out_bike_data.csv', index = False)