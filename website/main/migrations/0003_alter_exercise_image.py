# Generated by Django 4.0.6 on 2022-07-14 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_userprofile_userwithprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
