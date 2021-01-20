import urllib3 as ul
import bs4
import json
import pandas as pd
import numpy as np
import psycopg2

# %%
# I found it easier to just use the .csv link for all petitions
csv_link = 'https://petition.parliament.uk/petitions.csv'

# reading the bulk petitions and filtering it for only the 'open' petitions -- data was too massive
# to go through all of the available information
bulk_petition_data = pd.read_csv(csv_link)
bulk_petition_data = bulk_petition_data[bulk_petition_data['State'] == 'open'].reset_index(drop=True)

# %%
# this is the section to connect to Postgresql database
conn = psycopg2.connect(
    dbname='d7i9p9ekakqj4i',
    user='tnoeifjjdvhgnb',
    password='0bda6e63547e198aec6dd67d9e45c1bffde267a688ce53551550b72eda92d99b',
    host='ec2-54-237-135-248.compute-1.amazonaws.com',
    port='5432'
)

curr = conn.cursor()


def create_new_tables(curr):
    """
    :arg
    """
    return


# %%
# creating a dict for the bulk json data
json_bulk_data = {}
for k, row in bulk_petition_data.iterrows():
    split_url = row['URL'].split('/')
    url_data_pull = ul.PoolManager().request('GET', row['URL'] + '.json')
    json_data = json.loads(url_data_pull.data)

    json_bulk_data[str(split_url[-1])] = json_data
    break

# %%
data = pd.DataFrame(json_data['data']['attributes']['signatures_by_constituency'])
