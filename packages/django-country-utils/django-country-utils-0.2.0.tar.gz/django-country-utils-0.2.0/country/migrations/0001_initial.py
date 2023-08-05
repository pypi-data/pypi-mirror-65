# Generated by Django 3.0.4 on 2020-04-02 18:16

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=45, unique=True)),
                ('language', models.CharField(max_length=45)),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='countries', to='currency.Currency')),
            ],
            options={
                'verbose_name_plural': 'countries',
                'db_table': 'country',
            },
        ),
    ]
