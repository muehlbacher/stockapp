from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.mysql import TINYINT


# Define the base class for the models
Base = declarative_base()

# Define the Company table
class Company(Base):
    __tablename__ = 'Company'
    CompanyID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Industry = Column(String(100))
    Country = Column(String(100))
    Ticker = Column(String(20), unique=True)

# Define the StatementType table
class StatementType(Base):
    __tablename__ = 'StatementType'
    StatementTypeID = Column(Integer, primary_key=True, autoincrement=True)
    StatementName = Column(String(50), nullable=False)

# Define the Metric table
class Metric(Base):
    __tablename__ = 'Metric'
    MetricID = Column(Integer, primary_key=True, autoincrement=True)
    MetricName = Column(String(100), nullable=False)
    MetricType = Column(String(50))

# Define the TimePeriod table
class TimePeriod(Base):
    __tablename__ = 'TimePeriod'
    TimePeriodID = Column(Integer, primary_key=True, autoincrement=True)
    Year = Column(Integer, nullable=False)
    Quarter = Column(TINYINT)  # 1-4 for quarters, or NULL for annual data
    StartDate = Column(Date)
    EndDate = Column(Date)

# Define the FinancialData table
class FinancialData(Base):
    __tablename__ = 'FinancialData'
    FinancialDataID = Column(Integer, primary_key=True, autoincrement=True)
    CompanyID = Column(Integer, ForeignKey('Company.CompanyID'), nullable=False)
    StatementTypeID = Column(Integer, ForeignKey('StatementType.StatementTypeID'), nullable=False)
    MetricID = Column(Integer, ForeignKey('Metric.MetricID'), nullable=False)
    TimePeriodID = Column(Integer, ForeignKey('TimePeriod.TimePeriodID'), nullable=False)
    Value = Column(DECIMAL(18, 2), nullable=False)

    # Define relationships (optional, for ORM navigation)
    company = relationship('Company', backref='financial_data')
    statement_type = relationship('StatementType', backref='financial_data')
    metric = relationship('Metric', backref='financial_data')
    time_period = relationship('TimePeriod', backref='financial_data')

# Define the database URL
DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1/market"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

print("Tables created successfully!")