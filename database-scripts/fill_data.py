from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import Company, TimePeriod, Metric, FinancialData, StatementType


import pickle
from indicators.warren_buffet import WarrenBuffets

if __name__ == "__main__":
    filename = "../data/solar_companies_data.pkl"
    with open(filename, "rb") as f:
        data = pickle.load(f)

    wb = WarrenBuffets()

    for symbol, values in data.items():
        for year in values:
            year = wb.applyAll(year)

    print(data['DQ'][4]['sgaRatio'], data['DQ'][4]['calendarYear'])
    print(data['DQ'][0]['randdRatio'])
    print(data['DQ'][0]['deprecationRatio'])
    print(data['DQ'][0]['interestExpenseRatio'], data['DQ'][0]['calendarYear'])
    print(data['DQ'][0]['netEarningsRatio'], data['DQ'][0]['calendarYear'])
    print(data['DQ'][1]['netEarningsRatio'], data['DQ'][1]['calendarYear'])


    times = [x['calendarYear'] for x in data['DQ']]

    print(times)

    #get company id
    DATABASE_URL = "mysql+pymysql://root:root@localhost/market"
    # Create the engine and session
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    #get metricids
    metric_names = ["sgaRatio",
                     "randdRatio", 
                     "deprecationRatio",
                     "interestExpenseRatio",
                     "netEarningsRatio"]
    metrics = []
    for metric_name in metric_names:
        metric = session.query(Metric).filter_by(MetricName=metric_name).first()
        metrics.append(metric)
        print(metric.MetricID, metric.MetricName)
    #get companyids
    companies = session.query(Company).all() 
    #get timeperiodids
    time_years = {}
    for time in times:
        time_year = session.query(TimePeriod).filter_by(Year=time).first()
        time_years[time_year.Year] = time_year.TimePeriodID
        print(time_year.Year, time_year.TimePeriodID)
    timeperiods = session.query(TimePeriod).all()
    #get statementtypeids
    statement_type_id = 1 # Income Statement

    for company in companies:
        company_id = company.CompanyID
        for metric in metrics:
            metric_id = metric.MetricID

            for value in data[company.Ticker]:
                year_id = time_years[int(value['calendarYear'])]
                print(company_id, statement_type_id, metric_id, year_id, value[metric.MetricName])
                print(company.Ticker, statement_type_id, metric.MetricName, [value['calendarYear']], value[metric.MetricName])
                financial_data = FinancialData(CompanyID=company_id,
                                               StatementTypeID=statement_type_id,
                                               MetricID=metric_id,
                                               TimePeriodID=year_id,
                                               Value=value[metric.MetricName])
                session.add(financial_data)

    session.commit()
    print("Content was added to database")