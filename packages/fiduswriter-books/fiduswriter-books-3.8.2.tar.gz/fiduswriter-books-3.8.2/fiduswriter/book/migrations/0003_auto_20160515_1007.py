# Generated by Django 1.9.5 on 2016-05-15 15:07
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20151226_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookaccessright',
            name='rights',
            field=models.CharField(choices=[('r', 'read'), ('w', 'read/write')], max_length=5),
        ),
    ]
