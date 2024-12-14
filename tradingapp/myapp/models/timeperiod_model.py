from django.db import models


# Define the TimePeriod model
class TimePeriod(models.Model):
    TimePeriodID = models.AutoField(primary_key=True)
    Year = models.IntegerField(null=False)
    Quarter = models.PositiveSmallIntegerField(blank=True, null=True)  # 1-4 for quarters, or NULL for annual data
    StartDate = models.DateField(blank=True, null=True)
    EndDate = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'TimePeriod'  # Explicitly set the table name


    def __str__(self):
        return f"{self.Year} Q{self.Quarter}" if self.Quarter else str(self.Year)
