import urllib3 as ul
import bs4
import json
import pandas as pd
import numpy as np

csv_link = 'https://petition.parliament.uk/petitions.csv'
bulk_petition_data = pd.read_csv(csv_link)
bulk_petition_data = bulk_petition_data[bulk_petition_data['State'] == 'open'].reset_index(drop=True)

# %%
json_bulk_data = {}
for k, row in bulk_petition_data.iterrows():
    split_url = row['URL'].split('/')
    url_data_pull = ul.PoolManager().request('GET', row['URL'] + '.json')
    json_data = json.loads(url_data_pull.data)

    json_bulk_data[str(split_url[-1])] = json_data
    break


