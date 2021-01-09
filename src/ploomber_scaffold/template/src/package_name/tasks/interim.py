from pathlib import Path

import pandas as pd


def remove_nas(upstream, product):
    df = pd.read_parquet(str(upstream['get']))
    df = df[~df.a.isna()]
    Path(str(product)).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(str(product))
