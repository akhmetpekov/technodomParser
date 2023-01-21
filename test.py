import pandas as pd

# read json file
df = pd.read_json('data/products_data.json')

# write to excel file
df.to_csv('data/products_data.csv', index=False)
