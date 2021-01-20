# https://andydickinson.net/2019/03/27/quick-analalysis-of-petitions-data/
import requests
import pandas as pd
response  = requests.get('https://petition.parliament.uk/petitions/333869.json')
petition_data = response.json()
constituency_data = petition_data['data']['attributes']['signatures_by_constituency']
constituency_df = pd.DataFrame(constituency_data)
constituency_rank = constituency_df.sort_values(by=['signature_count'], ascending=False)
#(constituency_rank)
constituency_rank.head()