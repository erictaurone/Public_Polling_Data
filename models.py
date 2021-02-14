import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import psycopg2

DB_NAME = 'd7i9p9ekakqj4i'
USER = 'tnoeifjjdvhgnb'
PASSWORD = '0bda6e63547e198aec6dd67d9e45c1bffde267a688ce53551550b72eda92d99b'
HOST = 'ec2-54-237-135-248.compute-1.amazonaws.com'
PORT = '5432'
eng_str = r'postgres://%s:%s@%s:%s/%s' % (USER, PASSWORD, HOST, PORT, DB_NAME)
# engine = db.create_engine(eng_str, echo=True)
engine = db.create_engine('sqlite:///Public_Polling.db')
Base = declarative_base()


class PetitionData(Base):
    """
    The MainData class houses the general petition data at a snapshot in time in a table.
    """
    __tablename__ = 'petition_level_data'

    id = db.Column(db.Integer, primary_key=True)
    petition_category = db.Column(db.String)
    petition_id = db.Column(db.Integer)
    petition_action = db.Column(db.String)
    petition_background = db.Column(db.String)
    petition_state = db.Column(db.String)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    open_time = db.Column(db.DateTime)
    signature_count = db.Column(db.Integer)


class RegionSpecificData(Base):
    """
    The RegionSpecificData class houses the drilldown of data specific to a given region at a snapshot in time
    """
    
    __tablename__ = 'region_level_data'

    id = db.Column(db.Integer, primary_key=True)
    ons_code = db.Column(db.Integer)
    signature_count = db.Column(db.Integer)
    proportion_of_total = db.Column(db.Float)
    # petition_level_data_id = relationship('PetitionData', back_populates='region_level_data')
    petition = db.Column('petition', db.String, db.ForeignKey('petition_level_data.id'))


# PetitionData.region_level_data = relationship('RegionSpecificData', order_by=RegionSpecificData.id,
#                                               back_populates='petition_level_data_id')


class RegionStatistics(Base):
    """
    This houses the statistical data at the regional level (e.g. Essex) And ties that data back to
    """
    __tablename__ = 'region_level_statistics'

    id = db.Column(db.Integer, primary_key=True)
    statistic_name = db.Column(db.String)
    statistic_value = db.Column(db.Float)
    # region_level_data_id = relationship('RegionSpecificData', back_populates='region_level_statistics')
    region = db.Column('region', db.String, db.ForeignKey('region_level_data.id'))


# RegionSpecificData.region_level_statistics = relationship('RegionStatistics', order_by=RegionStatistics.id,
#                                                           back_populates='region_level_data_id')


class PetitionStatistics(Base):
    """
    This houses the statistical data at the regional level (e.g. Essex) And ties that data back to
    """
    __tablename__ = 'petition_level_statistics'

    id = db.Column(db.Integer, primary_key=True)
    statistic_name = db.Column(db.String)
    statistic_value = db.Column(db.Float)
    # petition_level_data_id = relationship('PetitionData', back_populates='petition_level_statistics')
    petition = db.Column('petition', db.String, db.ForeignKey('petition_level_data.id'))


# PetitionData.petition_level_statistics = relationship('RegionStatistics', order_by=PetitionStatistics.id,
                                                    #   back_populates='petition_level_data_id')

Base.metadata.create_all(engine)