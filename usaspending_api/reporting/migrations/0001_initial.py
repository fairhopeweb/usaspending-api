from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReportingAgencyTas',
            fields=[
                ('reporting_agency_tas_id', models.AutoField(primary_key=True, serialize=False)),
                ('toptier_code', models.TextField()),
                ('fiscal_year', models.IntegerField()),
                ('fiscal_period', models.IntegerField()),
                ('tas_rendering_label', models.TextField()),
                ('appropriation_obligated_amount', models.DecimalField(decimal_places=2, max_digits=23)),
                ('object_class_pa_obligated_amount', models.DecimalField(decimal_places=2, max_digits=23)),
                ('diff_approp_ocpa_obligated_amounts', models.DecimalField(decimal_places=2, max_digits=23)),
            ],
            options={
                'db_table': 'reporting_agency_tas',
            },
        ),
        migrations.AddIndex(
            model_name='reportingagencytas',
            index=models.Index(fields=['fiscal_year', 'fiscal_period', 'toptier_code'], name='reporting_agency_tas_group_idx'),
        ),
    ]
