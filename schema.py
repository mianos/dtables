from sqlalchemy import BigInteger, Column, DateTime, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Radacct(Base):
    __tablename__ = 'radacct'

    radacctid = Column(BigInteger, primary_key=True)
    acctsessionid = Column(String(64), nullable=False, index=True, server_default=text("''"))
    acctuniqueid = Column(String(32), nullable=False, index=True, server_default=text("''"))
    username = Column(String(64), nullable=False, index=True, server_default=text("''"))
    groupname = Column(String(64), nullable=False, server_default=text("''"))
    realm = Column(String(64), server_default=text("''"))
    nasipaddress = Column(String(15), nullable=False, index=True, server_default=text("''"))
    nasportid = Column(String(15))
    nasporttype = Column(String(32))
    acctstarttime = Column(DateTime, index=True)
    acctstoptime = Column(DateTime, index=True)
    acctsessiontime = Column(Integer, index=True)
    acctauthentic = Column(String(32))
    connectinfo_start = Column(String(50))
    connectinfo_stop = Column(String(50))
    acctinputoctets = Column(BigInteger)
    acctoutputoctets = Column(BigInteger)
    calledstationid = Column(String(50), nullable=False, server_default=text("''"))
    callingstationid = Column(String(50), nullable=False, server_default=text("''"))
    acctterminatecause = Column(String(32), nullable=False, server_default=text("''"))
    servicetype = Column(String(32))
    framedprotocol = Column(String(32))
    framedipaddress = Column(String(15), nullable=False, index=True, server_default=text("''"))
    acctstartdelay = Column(Integer)
    acctstopdelay = Column(Integer)
    xascendsessionsvrkey = Column(String(10))
