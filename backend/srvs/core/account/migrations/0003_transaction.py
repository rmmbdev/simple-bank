# Generated by Django 5.0.3 on 2024-03-08 10:33

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('amount', models.DecimalField(decimal_places=1, max_digits=30)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='in_transaction', to='account.account')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='out_transaction', to='account.account')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
