from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class BaseRepos:
    def __init__(self):
        DATABASE_URL = "mysql+pymysql://root:root@localhost/market"
        # Create the engine and session
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        self.session = Session()