# Generated by Django 2.2.6 on 2019-11-17 10:30

from django.db import migrations, models
import jsonfield.encoder
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('trionyx', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=128, unique=True)),
                ('value', jsonfield.fields.JSONField(dump_kwargs={'cls': jsonfield.encoder.JSONEncoder, 'separators': (',', ':')}, load_kwargs={})),
            ],
        ),
    ]
