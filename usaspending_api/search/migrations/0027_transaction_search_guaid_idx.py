# Generated by Django 3.2.15 on 2023-02-27 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0026_award_search_guaid_uq_idx'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                DROP INDEX ts_idx_award_key_pre2008;
                CREATE INDEX ts_idx_award_key ON rpt.transaction_search(generated_unique_award_id text_ops);
                -- Must rename the auto-named inherited indexes on child partitions of this parent partitioned table, 
                -- so that they follow the naming convention of the parent, and copy_table_metadata command will 
                -- continue to work
                ALTER INDEX rpt.transaction_search_fabs_generated_unique_award_id_idx RENAME TO ts_idx_award_key_fabs;
                ALTER INDEX rpt.transaction_search_fpds_generated_unique_award_id_idx RENAME TO ts_idx_award_key_fpds;
            """,
            reverse_sql="""
                DROP INDEX ts_idx_award_key;
                CREATE INDEX ts_idx_award_key_pre2008 ON rpt.transaction_search(generated_unique_award_id text_ops) WHERE action_date < '2007-10-01'::date;
                -- Must rename the auto-named inherited indexes on child partitions of this parent partitioned table, 
                -- so that they follow the naming convention of the parent, and copy_table_metadata command will 
                -- continue to work
                ALTER INDEX IF EXISTS rpt.transaction_search_fabs_generated_unique_award_id_idx RENAME TO ts_idx_award_key_pre2008_fabs;
                ALTER INDEX IF EXISTS rpt.transaction_search_fpds_generated_unique_award_id_idx RENAME TO ts_idx_award_key_pre2008_fpds;
            """,
            state_operations=[
                migrations.RemoveIndex(
                    model_name='transactionsearch',
                    name='ts_idx_award_key_pre2008',
                ),
                migrations.AddIndex(
                    model_name='transactionsearch',
                    index=models.Index(fields=['generated_unique_award_id'], name='ts_idx_award_key'),
                ),
            ],
        ),
    ]
