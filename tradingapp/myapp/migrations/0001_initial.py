# Generated by Django 5.1.3 on 2025-02-07 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("CompanyID", models.AutoField(primary_key=True, serialize=False)),
                ("Name", models.CharField(max_length=255)),
                ("Industry", models.CharField(blank=True, max_length=100, null=True)),
                ("Sector", models.CharField(blank=True, max_length=20, null=True)),
                ("Country", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "Ticker",
                    models.CharField(blank=True, max_length=20, null=True, unique=True),
                ),
                ("Currency", models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                "db_table": "Company",
            },
        ),
        migrations.CreateModel(
            name="Metric",
            fields=[
                ("MetricID", models.AutoField(primary_key=True, serialize=False)),
                ("MetricName", models.CharField(max_length=100)),
                ("MetricType", models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                "db_table": "Metric",
            },
        ),
        migrations.CreateModel(
            name="StatementType",
            fields=[
                (
                    "StatementTypeID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("StatementName", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "StatementType",
            },
        ),
        migrations.CreateModel(
            name="TimePeriod",
            fields=[
                ("TimePeriodID", models.AutoField(primary_key=True, serialize=False)),
                ("Year", models.IntegerField()),
                ("Quarter", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("StartDate", models.DateField(blank=True, null=True)),
                ("EndDate", models.DateField(blank=True, null=True)),
            ],
            options={
                "db_table": "TimePeriod",
            },
        ),
        migrations.CreateModel(
            name="FinancialData",
            fields=[
                (
                    "FinancialDataID",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("Valuation", models.CharField(blank=True, max_length=255, null=True)),
                ("Value", models.DecimalField(decimal_places=2, max_digits=18)),
                (
                    "CompanyID",
                    models.ForeignKey(
                        db_column="CompanyID",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="financial_data",
                        to="myapp.company",
                    ),
                ),
                (
                    "MetricID",
                    models.ForeignKey(
                        db_column="MetricID",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="financial_data",
                        to="myapp.metric",
                    ),
                ),
                (
                    "StatementTypeID",
                    models.ForeignKey(
                        db_column="StatementTypeID",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="financial_data",
                        to="myapp.statementtype",
                    ),
                ),
                (
                    "TimePeriodID",
                    models.ForeignKey(
                        db_column="TimePeriodID",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="financial_data",
                        to="myapp.timeperiod",
                    ),
                ),
            ],
            options={
                "db_table": "FinancialData",
            },
        ),
    ]
