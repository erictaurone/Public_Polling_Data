import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from models import PetitionData, PetitionStatistics, RegionStatistics, RegionSpecificData
import pandas as pd
import json
import urllib3 as ul
from datetime import datetime as dt

engine = db.create_engine('sqlite:///Public_Polling.db')
connection = engine.connect()
metadata = db.MetaData()
petition_data = db.Table('petition_level_data', metadata, autoload=True, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()
result = session.query(PetitionData)

# %%

categorizedPetitionSample = pd.read_csv(
    'https://github.com/erictaurone/Public_Polling_Data/raw/master/210210%20Catagorised%20Petitions.csv')
# %%
for i, row in categorizedPetitionSample.iterrows():
    # connecting to the .json file from the government database
    url_data_pull = ul.PoolManager().request('GET', row['URL'] + '.json')

    # extracting the data and loading in a json format
    json_data = json.loads(url_data_pull.data)

    # initializing our PetitionData class (this gets loaded into our DB later)

    petition = PetitionData()
    # assigning the values for our particular petition
    petition.petition_id = json_data['data']['id']
    petition.petition_action = json_data['data']['attributes']['action']
    petition.petition_background = json_data['data']['attributes']['background'] + '\nAdditional Details: ' + \
                                   json_data['data']['attributes']['additional_details']
    petition.petition_state = json_data['data']['attributes']['state']
    petition.signature_count = json_data['data']['attributes']['signature_count']
    petition.update_time = dt.strptime(json_data['data']['attributes']['updated_at'][:19], '%Y-%m-%dT%H:%M:%S')
    petition.open_time = dt.strptime(json_data['data']['attributes']['opened_at'][:19], '%Y-%m-%dT%H:%M:%S')
    petition.create_time = dt.strptime(json_data['data']['attributes']['created_at'][:19], '%Y-%m-%dT%H:%M:%S')
    petition.petition_category = row[row == 1.0].index[0]
    session.add(petition)
    session.commit()

    for constituency_row in json_data['data']['attributes']['signatures_by_constituency']:
        petition_region = RegionSpecificData()

        petition_region.ons_code = constituency_row['ons_code']
        petition_region.signature_count = constituency_row['signature_count']
        petition_region.petition = petition
        petition_region.proportion_of_total = constituency_row['signature_count'] / petition.signature_count
        session.add(petition_region)
        session.commit()
    break

# %%

