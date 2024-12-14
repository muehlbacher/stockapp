from repos.metric_repos import MetricRepos
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import Company, TimePeriod, Metric, FinancialData, StatementType


""" 
- get the data from the database
    - get all the companies
    - get all the metrics 
    - get all the timeperiods
    - get all the financialdata for the metrics and the companies
    - calculate the indicators
    - save the indicators to the financialdata tables
"""


#company_symbol="RUN"
#timeperiod="2019"
#metric="netIncomeRatio"
#statementtype="Income Statement"
def get_company_data(company_symbol: str, timeperiod: int, metric: str, statementtype: str = None):
    #get company id
    DATABASE_URL = "mysql+pymysql://root:root@localhost/market"
    # Create the engine and session
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    company_raw = session.query(Company).filter_by(Ticker=company_symbol).first()
    company_id = company_raw.CompanyID

    print(company_id)

    timeperiod_raw = session.query(TimePeriod).filter_by(Year=timeperiod).first()
    timeperiod_id = timeperiod_raw.TimePeriodID
    print(timeperiod_id)

    metric_raw = session.query(Metric).filter_by(MetricName=metric).first()
    metric_id = metric_raw.MetricID
    print(metric_id)

    statementtype_raw = session.query(StatementType).filter_by(StatementName=statementtype).first()
    statementtype_id = statementtype_raw.StatementTypeID
    print(statementtype_id)

    financial_data_raw = session.query(FinancialData).filter_by(CompanyID=company_id,
                                                                StatementTypeID=statementtype_id,
                                                                MetricID=metric_id,
                                                                TimePeriodID=timeperiod_id
                                                            ).first()
    
    print(financial_data_raw)
    
    return financial_data_raw.Value


if __name__ =="__main__":



    print(get_company_data(
        company_symbol="CSIQ",
        timeperiod=2019,
        metric="netIncomeRatio",
        statementtype="Income Statement"
    ))



    # repos = MetricRepos()

    # metric = repos.retrieve_metric(metric_name="sgaRatio")
    # print(metric.MetricID)
    # print(metric.MetricName)


    # #sgaRatio
    # DATABASE_URL = "mysql+pymysql://root:root@localhost/market"
    # # Create the engine and session
    # engine = create_engine(DATABASE_URL)
    # Session = sessionmaker(bind=engine)
    # session = Session()
    
    # metric_sgae = repos.retrieve_metric(metric_name="sellingGeneralAndAdministrativeExpenses")
    # metric_gp = repos.retrieve_metric(metric_name="grossProfit")
    # print(metric_sgae.MetricID)
    # print(metric_gp.MetricID)

    # companies = session.query(Company).all()
    # print(companies)

    # timeperiods = session.query(TimePeriod).filter_by()
    # print(timeperiods)

    # data = session.qery().join(

    # )