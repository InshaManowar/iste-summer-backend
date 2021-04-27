# Generated by Django 3.1.7 on 2021-04-26 14:08

import course.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['startdate'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='resources',
            options={'verbose_name': 'Resources', 'verbose_name_plural': 'Resources'},
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='file',
            field=models.FileField(upload_to=course.models.upload_location_submission),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='course.category'),
        ),
    ]
