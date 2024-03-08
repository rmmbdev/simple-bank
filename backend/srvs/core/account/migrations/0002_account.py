# Generated by Django 5.0.3 on 2024-03-08 10:03

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


def add_data(apps, schema_editor):
    user_model = apps.get_model('account', 'User')
    account_model = apps.get_model('account', 'Account')
    account_model.objects.create(owner=user_model.objects.filter(username="banker").first())


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True,
                                        serialize=False)),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='accounts',
                                            to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(add_data),
    ]
