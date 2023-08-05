from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DatasetMetadata(Base):
    __tablename__ = 'dataset_metadata'

    id = Column(Integer, primary_key=True)
    dataset_name = Column(String, unique=True, index=True)
    data_folder_path = Column(String, unique=True)
    sql_server = Column(String)
    sql_db = Column(String)
    schema = Column(String)
    stored_in_data_db = Column(Boolean())


class TableMetadata(Base):
    __tablename__ = 'table_metadata'

    id = Column(Integer, primary_key=True)
    dataset_name = Column(String, index=True)
    table_name = Column(String, index=True)
    file = Column(String)
    num_records = Column(Integer)
    num_analyzed = Column(Integer)


class ColumnMetadata(Base):
    __tablename__ = 'column_metadata'

    id = Column(Integer, primary_key=True)
    dataset_name = Column(String, index=True)
    table_name = Column(String, index=True)
    column_source_name = Column(String, index=True)
    column_custom_name = Column(String)
    is_many = Column(Boolean())
    visible = Column(Boolean(), default=True)
    num_non_null = Column(Integer)
    data_type = Column(String)


class TableRelationship(Base):
    __tablename__ = 'table_relationship'

    id = Column(Integer, primary_key=True)
    dataset_name = Column(String, index=True)
    reference_table = Column(String, index=True)
    other_table = Column(String, index=True)
    reference_table_role = Column(String, index=True)
    reference_key = Column(String, index=True)
    other_key = Column(String, index=True)
