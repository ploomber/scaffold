import pandas as pd


def remove_nas(upstream, product):
    df = pd.read_parquet(str(upstream['get']))
    df = df[~df.a.isna()]
    df.to_parquet(str(product))
