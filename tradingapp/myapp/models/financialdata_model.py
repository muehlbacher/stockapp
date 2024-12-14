from django.db import models
from .company_model import Company
from .metric_model import Metric
from .statementtype_model import StatementType
from .timeperiod_model import TimePeriod


# Define the FinancialData model
class FinancialData(models.Model):
    FinancialDataID = models.AutoField(primary_key=True)
    CompanyID = models.ForeignKey(Company, 
                                  on_delete=models.CASCADE, 
                                  related_name='financial_data', 
                                  db_column='CompanyID'  # Use the existing column name
                                  )
    StatementTypeID = models.ForeignKey(StatementType, 
                                        on_delete=models.CASCADE, 
                                        related_name='financial_data',
                                        db_column='StatementTypeID'  # Use the existing column name#
                                        )
    MetricID = models.ForeignKey(Metric, 
                                 on_delete=models.CASCADE, 
                                 related_name='financial_data',
                                 db_column='MetricID'
                                 )
    TimePeriodID = models.ForeignKey(TimePeriod, 
                                     on_delete=models.CASCADE, 
                                     related_name='financial_data',
                                     db_column='TimePeriodID'
                                     )
    Valuation = models.CharField(max_length=255, blank=True, null=True)
    Value = models.DecimalField(max_digits=18, decimal_places=2, null=False)

    class Meta:
        db_table = 'FinancialData'  # Explicitly set the table name


    def __str__(self):
        return f"{self.CompanyID} | {self.StatementTypeID} | {self.MetricID} | {self.TimePeriodID} | {self.Value}"
