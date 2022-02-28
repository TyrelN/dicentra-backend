# Generated by Django 3.2.10 on 2022-02-07 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0017_alter_articlepost_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='caption',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='caption_second',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='content',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='content_second',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='content_third',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='petpost',
            name='available',
            field=models.CharField(blank=True, choices=[('available', 'available'), ('not available', 'not available'), ('adopted', 'adopted')], default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='petpost',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]