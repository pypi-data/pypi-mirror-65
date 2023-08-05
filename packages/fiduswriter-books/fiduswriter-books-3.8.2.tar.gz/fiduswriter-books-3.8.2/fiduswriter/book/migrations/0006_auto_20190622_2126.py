# Generated by Django 2.2.2 on 2019-06-22 21:26
import json
from django.db import migrations

def add_bibliography_header(apps, schema_editor):
    Book = apps.get_model('book', 'Book')
    for book in Book.objects.all():
        settings = json.loads(book.settings)
        if not 'bibliography_header' in settings:
            settings['bibliography_header'] = 'Bibliography'
            book.settings = json.dumps(settings)
            book.save()


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_auto_20160515_1013'),
    ]

    operations = [
        migrations.RunPython(add_bibliography_header),
    ]
