from django.db import models


# Define the Company model
class Company(models.Model):
    CompanyID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, null=False)
    Industry = models.CharField(max_length=100, blank=True, null=True)
    Sector = models.CharField(max_length=20, blank=True, null=True)
    Country = models.CharField(max_length=100, blank=True, null=True)
    Ticker = models.CharField(max_length=20, unique=True, blank=True, null=True)
    Currency = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "Company"  # Explicitly set the table name

    def __str__(self):
        return str(self.Name)
