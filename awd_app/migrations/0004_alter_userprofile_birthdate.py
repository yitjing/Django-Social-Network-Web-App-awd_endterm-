# Generated by Django 4.2 on 2023-09-08 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awd_app', '0003_alter_userprofile_bio_alter_userprofile_profileimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthDate',
            field=models.DateField(blank=True),
        ),
    ]
