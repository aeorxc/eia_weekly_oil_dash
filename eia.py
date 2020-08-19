import pandas as pd
import os
import json
import urllib.request
from functools import lru_cache
import logging
import symbols


eia_api_key = os.environ['EIA_KEY']
eia_series_url = 'http://api.eia.gov/series/?api_key={}&series_id={}'


data_last_update_time = {}


@lru_cache(maxsize=None)
def get_symbols(symbollist):
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
            data_last_update_time[series['series_id']] = pd.to_datetime(series['updated'])
            dfs.append(d)

    df = pd.concat(dfs, 1)

    return df


def last_update_tag():
    if data_last_update_time is None or len(data_last_update_time) == 0:
        return ''

    t = data_last_update_time[list(data_last_update_time.keys())[0]]
    t = t.strftime('%d %b %y %H:%m')
    return t


def clear_cache():
    logging.info(get_symbols.cache_info())
    get_symbols.cache_clear()
    logging.info(get_symbols.cache_info())

