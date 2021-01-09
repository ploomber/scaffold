"""
Generate plot
"""
import pandas as pd

# + tags=["parameters"]
upstream = ['add_column']
product = {'nb': 'products/plot.ipynb'}
# -

df = pd.read_parquet(upstream['add_column'])
df.c.plot()
