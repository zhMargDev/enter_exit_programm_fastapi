from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection details
DATABASE_URL = "sqlite:///database.db"  # Replace with your database file path

# Define database models
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True)
    pin = Column(Integer, unique=True)
    status = Column(String)
    workerName = Column(String)

class Monitoring(Base):
    __tablename__ = "monitoring"

    id = Column(Integer, primary_key=True)
    pin = Column(Integer)
    workerName = Column(String)
    time = Column(Integer)
    date = Column(Integer)
    type = Column(String)
    late = Column(String)
    recycling = Column(String)

class WorkingTimes(Base):
    __tablename__ = "workingTimes"

    id = Column(Integer, primary_key=True)
    workerId = Column(Integer)
    workingTimeFrom = Column(Integer)
    workingTimeTo = Column(Integer)

class BannedDays(Base):
    __tablename__ = "bannedDays"

    id = Column(Integer, primary_key=True)
    workerId = Column(Integer)
    bannedData = Column(Integer)

class BannedWeeks(Base):
    __tablename__ = "bannedWeeks"

    id = Column(Integer, primary_key=True)
    workerId = Column(Integer)
    bannedDay = Column(Integer)

class Registry(Base):
    __tablename__ = "registry"

    id = Column(Integer, primary_key=True)
    deviceType = Column(String)
    deviceIp = Column(String)


Base.metadata.create_all(engine)  # Create tables if they don't exist


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
