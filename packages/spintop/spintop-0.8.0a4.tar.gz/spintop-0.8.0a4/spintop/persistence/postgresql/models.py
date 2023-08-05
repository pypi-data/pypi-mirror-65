from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SQLTestRecord(Base):
    __tablename__ = 'test-records'
    test_uuid = Column(String, primary_key=True)
    data = Column(JSONB)