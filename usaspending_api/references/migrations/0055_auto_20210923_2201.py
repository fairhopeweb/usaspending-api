# Generated by Django 2.2.23 on 2021-09-23 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0054_auto_20210923_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gtassf133balances',
            name='disaster_emergency_fund',
            field=models.ForeignKey(blank=True, db_column='disaster_emergency_fund_code', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='references.DisasterEmergencyFundCode'),
        ),
    ]
