import django_tables2 as tables
from .models import Company

class CompanyTable(tables.Table):
    #when used with pandas df -> fields have to be defined here
    # todo: save data in DB model and use it with model class
    name = tables.Column()
    calendarYear = tables.Column()
    revenue = tables.Column()
    class Meta:
        #model = Company  # Link the table to the Employee model
        template_name = "django_tables2/bootstrap4.html"  # Choose a template for styling
        #fields = ("name", "revenue")  # Specify fields to include