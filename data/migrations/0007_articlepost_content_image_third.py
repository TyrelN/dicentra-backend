# Generated by Django 3.2.9 on 2021-12-15 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_alter_currentevent_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='content_image_third',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
