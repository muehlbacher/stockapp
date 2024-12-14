from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import Metric

if __name__ == "__main__":
        #get company id
    DATABASE_URL = "mysql+pymysql://root:root@localhost/market"
    # Create the engine and session
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    metric_names = ["sgaRatio",
                     "randdRatio", 
                     "deprecationRatio",
                     "interestExpenseRatio",
                     "netEarningsRatio"]
    

    for metric_name in metric_names:
        session.query(Metric).filter_by(MetricName=metric_name).delete()

    session.commit()


