import pandas as pd
import os
import json
import urllib.request
from functools import lru_cache


eia_api_key = os.environ['EIA_KEY']
eia_series_url = 'http://api.eia.gov/series/?api_key={}&series_id={}'


@lru_cache(maxsize=None)
def symbols(symbollist):
    # symbols from
    # http://ir.eia.gov/wpsr/psw01.xls
    # http://ir.eia.gov/wpsr/psw04.xls

    u = eia_series_url.format(eia_api_key, ';'.join(symbollist))
    contents = urllib.request.urlopen(u)
    j = json.load(contents)
    dfs = []
    if 'series' in j:
        for series in j['series']:
            d = pd.DataFrame(series['data'], columns=['Date', series['series_id']]).set_index('Date')
            d.index = pd.to_datetime(d.index)
            dfs.append(d)

    df = pd.concat(dfs, 1)

    return df



def overview():
    sl = [
        'PET.WCESTUS1.W',
        'PET.WGTSTUS1.W',
        'PET.WDISTUS1.W',
    ]
    df = symbols(tuple(sl))
    return df


