from django.contrib import admin

# Register your models here.
from .models.company_model import Company
from .models.financialdata_model import FinancialData
from .models.metric_model import Metric
from .models.statementtype_model import StatementType
from .models.timeperiod_model import TimePeriod

admin.site.register(Company)
admin.site.register(StatementType)
admin.site.register(Metric)
admin.site.register(TimePeriod)
admin.site.register(FinancialData)
