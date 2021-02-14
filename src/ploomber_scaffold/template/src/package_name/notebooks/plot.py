"""
Generate plot
"""
import pandas as pd

# + tags=["parameters"]
upstream = ['add_column']
product = None
# -

df = pd.read_parquet(upstream['add_column'])
df.c.plot()
