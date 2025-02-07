from django.db import models
from .metric_model import Metric


class MetricTooltip(models.Model):
    TooltipID = models.AutoField(primary_key=True)
    Metric = models.ForeignKey(Metric, on_delete=models.CASCADE, db_column="MetricID")
    Tooltip = models.TextField(null=False)

    class Meta:
        managed = False
        db_table = "MetricTooltip"
