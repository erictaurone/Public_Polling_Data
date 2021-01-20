#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
response  = requests.get('https://petition.parliament.uk/petitions/333869.json')
petition_data = response.json()
constituency_data = petition_data['data']['attributes']['signatures_by_constituency']
constituency_df = pd.DataFrame(constituency_data)
pop = pd.read_csv('West-m_pop.csv',  thousands=',')
petition_pop = pd.merge(pop, constituency_df, on='ons_code')
petition_pop["calc"] = (
    petition_pop["signature_count"] / petition_pop["population"]
)
petition_pop.head()
