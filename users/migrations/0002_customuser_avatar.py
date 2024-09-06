# Generated by Django 4.2.14 on 2024-09-06 17:59

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=users.models.file_upload),
        ),
    ]
