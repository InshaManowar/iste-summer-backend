# Generated by Django 3.1.7 on 2021-07-17 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_auto_20210715_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.ImageField(null=True, upload_to='icons'),
        ),
    ]