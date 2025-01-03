import logging
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from db.models import Company, FinancialData, Metric, TimePeriod, StatementType

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DataLoader:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.metrics = [
            "revenue",
            "costOfRevenue",
            "grossProfit",
            "grossProfitRatio",
            "researchAndDevelopmentExpenses",
            "generalAndAdministrativeExpenses",
            "sellingAndMarketingExpenses",
            "sellingGeneralAndAdministrativeExpenses",
            "otherExpenses",
            "operatingExpenses",
            "costAndExpenses",
            "interestIncome",
            "interestExpense",
            "depreciationAndAmortization",
            "ebitda",
            "ebitdaratio",
            "operatingIncome",
            "operatingIncomeRatio",
            "totalOtherIncomeExpensesNet",
            "incomeBeforeTax",
            "incomeBeforeTaxRatio",
            "incomeTaxExpense",
            "netIncome",
            "netIncomeRatio",
            "eps",
            "epsdiluted",
            "weightedAverageShsOut",
            "weightedAverageShsOutDil",
            "sgaRatio",
            "randdRatio",
            "deprecationRatio",
            "interestExpenseRatio",
            "netEarningsRatio",
        ]

    def load_companies(self, company_data: pd.DataFrame):
        statement_type = (
            self.db_session.query(StatementType)
            .filter_by(StatementName="Income Statement")
            .first()
        )
        statement_type_id = statement_type.StatementTypeID
        try:
            # check if company is already in load_companies
            for index, entry in company_data.iterrows():
                company_id = self.get_company_id(entry["symbol"])
                print(company_id)
                time_period_id = self.get_time_period_id(entry["calendarYear"])
                if time_period_id is None:
                    raise SQLAlchemyError(
                        f"TimePeriod: {entry['calendarYear']} not in database!"
                    )

                for metric_name in self.metrics:
                    metric_id = self.get_metric_id(metric_name)
                    valuation = None
                    if f"{metric_name}_valuation" in company_data.columns:
                        valuation = entry[f"{metric_name}_valuation"]
                        print(valuation)
                    value = entry[metric_name]
                    self.check_financial_data(
                        company_id,
                        statement_type_id,
                        time_period_id,
                        metric_id,
                        value,
                        valuation,
                    )
                    print("added")

                self.db_session.commit()

        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Error loading company data: {e}")
            raise

    def get_company_id(self, symbol: str):
        """
        returns company id if exists, returns None if company not in database
        """
        try:
            company = self.db_session.query(Company).filter_by(Ticker=symbol).first()
            if company:
                return company.CompanyID

            new_company = Company(Ticker=symbol, Name=symbol)
            self.db_session.add(new_company)
            self.db_session.commit()
            return new_company.CompanyID
        except SQLAlchemyError as e:
            logger.error(f"company could not be added: {symbol} {e}")
            self.db_session.rollback()
            return None

    def get_time_period_id(self, year: str):
        timeperiod = self.db_session.query(TimePeriod).filter_by(Year=year).first()
        if timeperiod:
            return timeperiod.TimePeriodID
        return timeperiod

    def get_metric_id(self, metric_name: str):
        try:
            metric = (
                self.db_session.query(Metric).filter_by(MetricName=metric_name).first()
            )
            if metric:
                return metric.MetricID
            new_metric = Metric(MetricName=metric_name)
            self.db_session.add(new_metric)
            self.db_session.commit()
            return new_metric.MetricID

        except SQLAlchemyError as e:
            logger.error(f"metric could not be added: {metric_name}{e}")
            self.db_session.rollback()
            return None

    def check_financial_data(
        self, company_id, statement_type_id, time_period_id, metric_id, value, valuation
    ):
        try:
            print("adding financial_Data")
            print(
                company_id,
                statement_type_id,
                time_period_id,
                metric_id,
                value,
                valuation,
            )
            financial_data = (
                self.db_session.query(FinancialData)
                .filter_by(
                    CompanyID=company_id,
                    StatementTypeID=statement_type_id,
                    MetricID=metric_id,
                    TimePeriodID=time_period_id,
                )
                .first()
            )
            if financial_data:
                financial_data.Value = value
                financial_data.Valuation = valuation
                self.db_session.commit()
            else:
                new_financialdata = FinancialData(
                    CompanyID=company_id,
                    StatementTypeID=statement_type_id,
                    TimePeriodID=time_period_id,
                    MetricID=metric_id,
                    Value=value,
                    Valuation=valuation,
                )
                self.db_session.add(new_financialdata)
                self.db_session.commit()
                print("added the finanecial_Data")
                print(new_financialdata.__str__)
        except SQLAlchemyError as e:
            logger.error(f"error in th financial_data adding: {e}")
            self.db_session.rollback()
