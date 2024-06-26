# Generated by Django 5.0.6 on 2024-05-22 13:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.CharField(max_length=50, unique=True)),
                ('customer_name', models.CharField(max_length=75, null=True)),
                ('spoc', models.CharField(max_length=50, null=True)),
                ('email_id', models.EmailField(max_length=100, null=True)),
                ('contact_number', models.CharField(max_length=30, null=True)),
                ('location', models.CharField(max_length=70, null=True)),
                ('address', models.CharField(max_length=150, null=True)),
                ('creation_date', models.DateField(null=True)),
                ('flag', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HrTeam',
            fields=[
                ('employee_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('reference_number', models.IntegerField(null=True)),
                ('designation', models.CharField(max_length=100, null=True)),
                ('ctc', models.IntegerField(null=True)),
                ('job_location', models.CharField(max_length=100, null=True)),
                ('date_of_joining', models.DateField(null=True)),
                ('offer_validity_date', models.DateField(null=True)),
                ('system_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('flag', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('years_of_experience', models.FloatField(null=True)),
                ('user_id', models.IntegerField(null=True)),
                ('sub_business_unit', models.IntegerField(null=True)),
                ('skills', models.CharField(max_length=50, null=True)),
                ('request_raised_date', models.DateTimeField(null=True)),
                ('notice_period', models.DateField(null=True)),
                ('int_req_id', models.CharField(max_length=10, null=True)),
                ('flag', models.CharField(max_length=10, null=True)),
                ('employee_type', models.IntegerField(null=True)),
                ('date_of_joining', models.DateField(null=True)),
                ('cost_center_id', models.IntegerField(null=True)),
                ('business_unit', models.IntegerField(null=True)),
                ('budget', models.IntegerField(null=True)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='EmployeeDetails_hrteam', to='ctc.hrteam')),
            ],
        ),
    ]
