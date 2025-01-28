from django.db import models


# Define the StatementType model
class StatementType(models.Model):
    StatementTypeID = models.AutoField(primary_key=True)
    StatementName = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = "StatementType"  # Explicitly set the table name

    def __str__(self):
        return self.StatementName
