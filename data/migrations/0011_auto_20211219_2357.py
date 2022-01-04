# Generated by Django 3.2.9 on 2021-12-19 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_auto_20211219_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='category',
            field=models.CharField(blank=True, choices=[('information', 'information'), ('news', 'news'), ('event', 'event'), ('seasonal', 'seasonal')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='petpost',
            name='available',
            field=models.CharField(blank=True, choices=[('available', 'available'), ('not available', 'not available'), ('adopted', 'adopted')], max_length=150, null=True),
        ),
    ]
