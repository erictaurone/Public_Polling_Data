import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from models import PetitionData, PetitionStatistics, RegionStatistics, RegionSpecificData
import pandas as pd


engine = db.create_engine('sqlite:///Public_Polling.db')
connection = engine.connect()
metadata = db.MetaData()
petition_data = db.Table('petition_level_data', metadata, autoload=True, autoload_with=engine)

Session = sessionmaker(bind=engine)
session = Session()
result = session.query(PetitionData)

# %%

df = pd.read_csv('https://github.com/erictaurone/Public_Polling_Data/raw/master/210210%20Catagorised%20Petitions.csv')

