# Generated by Django 5.0.3 on 2024-03-08 12:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')], db_index=True, default='PENDING', max_length=25),
        ),
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('INCREMENT', 'Increment'), ('TRANSFER', 'Transfer')], db_index=True, default='INCREMENT', max_length=25),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='in_transactions', to='account.account'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='out_transactions', to='account.account'),
        ),
    ]
