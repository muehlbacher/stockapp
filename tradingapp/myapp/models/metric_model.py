from django.db import models


# Define the Metric model
class Metric(models.Model):
    MetricID = models.AutoField(primary_key=True)
    MetricName = models.CharField(max_length=100, null=False)
    MetricType = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "Metric"  # Explicitly set the table name

    def __str__(self):
        return self.MetricName
