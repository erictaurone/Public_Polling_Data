import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import psycopg2

DB_NAME = 'd7i9p9ekakqj4i'
USER = 'tnoeifjjdvhgnb'
PASSWORD = '0bda6e63547e198aec6dd67d9e45c1bffde267a688ce53551550b72eda92d99b'
HOST = 'ec2-54-237-135-248.compute-1.amazonaws.com'
PORT = '5432'
eng_str = r'postgres://%s:%s@%s:%s/%s' % (USER, PASSWORD, HOST, PORT, DB_NAME)
# engine = sqla.create_engine(eng_str, echo=True)
engine = sqla.create_engine('sqlite:///Public_Polling.db')
Base = declarative_base()


class PetitionData(Base):
    """
    The MainData class houses the general petition data at a snapshot in time in a table.
    """
    __tablename__ = 'petition_level_data'

    id = sqla.Column(sqla.Integer, primary_key=True)
    petition_category = sqla.Column(sqla.String)
    petition_id = sqla.Column(sqla.Integer)
    petition_action = sqla.Column(sqla.String)
    petition_background = sqla.Column(sqla.String)
    petition_state = sqla.Column(sqla.String)
    create_time = sqla.Column(sqla.DateTime)
    update_time = sqla.Column(sqla.DateTime)
    open_time = sqla.Column(sqla.DateTime)
    signature_count = sqla.Column(sqla.Integer)


class RegionSpecificData(Base):
    """
    The RegionSpecificData class houses the drilldown of data specific to a given region at a snapshot in time
    """
    __tablename__ = 'region_level_data'

    id = sqla.Column(sqla.Integer, primary_key=True)
    ons_code = sqla.Column(sqla.Integer)
    signature_count = sqla.Column(sqla.Integer)
    proportion_of_total = sqla.Column(sqla.Float)
    petition_level_data_id = relationship('PetitionData', back_populates='region_level_data')


PetitionData.region_level_data = relationship('RegionSpecificData', order_by=RegionSpecificData.id,
                                              back_populates='petition_level_data_id')


class RegionStatistics(Base):
    """
    This houses the statistical data at the regional level (e.g. Essex) And ties that data back to
    """
    __tablename__ = 'region_level_statistics'

    id = sqla.Column(sqla.Integer, primary_key=True)
    statistic_name = sqla.Column(sqla.String)
    statistic_value = sqla.Column(sqla.Float)
    region_level_data_id = relationship('RegionSpecificData', back_populates='region_level_statistics')


RegionSpecificData.region_level_statistics = relationship('RegionStatistics', order_by=RegionStatistics.id,
                                                          back_populates='region_level_data_id')


class PetitionStatistics(Base):
    """
    This houses the statistical data at the regional level (e.g. Essex) And ties that data back to
    """
    __tablename__ = 'petition_level_statistics'

    id = sqla.Column(sqla.Integer, primary_key=True)
    statistic_name = sqla.Column(sqla.String)
    statistic_value = sqla.Column(sqla.Float)
    petition_level_data_id = relationship('PetitionData', back_populates='petition_level_statistics')


PetitionData.petition_level_statistics = relationship('RegionStatistics', order_by=PetitionStatistics.id,
                                                      back_populates='petition_level_data_id')

Base.metadata.create_all(engine)