import sqlalchemy as sqla

engine = sqla.create_engine('sqlite:///Public_Polling.db', echo=True)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class PetitionData(Base):
    """
    The MainData class houses the general petition data at a snapshot in time in a table.
    """
    __tablename__ = 'petition_level_data'

    id = sqla.Column(sqla.Integer, primary_key=True)
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