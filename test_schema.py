from sqlalchemy import BigInteger, Column, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'es_users'

    id = Column(BigInteger, primary_key=True)
    email = Column(String(150), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
