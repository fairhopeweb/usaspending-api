# Generated by Django 3.2.15 on 2023-01-13 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0098_auto_20221215_2029'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                'CREATE UNIQUE INDEX source_assistance_transaction_afa_generated_unique_upper_key ON raw.source_assistance_transaction (UPPER(afa_generated_unique))',
            ],
            reverse_sql=[
                'DROP INDEX source_assistance_transaction_afa_generated_unique_upper_key'
            ]
        ),
    ]

