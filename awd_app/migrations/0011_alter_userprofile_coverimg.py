# Generated by Django 4.2 on 2023-09-12 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awd_app', '0010_alter_userprofile_coverimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='coverImg',
            field=models.ImageField(blank=True, default='defaultCover.jpg', null=True, upload_to='media/coverImg/'),
        ),
    ]
