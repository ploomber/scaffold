import numpy as np
import pandas as pd


def get(product):
    df = pd.DataFrame(np.random.rand(100, 2), columns=['a', 'b'])
    df.loc[:10, 'a'] = np.nan
    df.to_parquet(str(product))
