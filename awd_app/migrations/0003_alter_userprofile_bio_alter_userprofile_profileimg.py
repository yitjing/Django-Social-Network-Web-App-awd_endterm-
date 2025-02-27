# Generated by Django 4.2 on 2023-09-08 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awd_app', '0002_rename_appuser_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profileImg',
            field=models.ImageField(blank=True, default='icons8-user-96.png', null=True, upload_to='media/profileImg/'),
        ),
    ]
