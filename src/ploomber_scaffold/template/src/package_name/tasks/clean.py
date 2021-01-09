from pathlib import Path

import pandas as pd


def add_column(upstream, product):
    df = pd.read_parquet(str(upstream['remove_nas']))
    df['c'] = df.a + df.b
    Path(str(product)).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(str(product))
