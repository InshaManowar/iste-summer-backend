# Generated by Django 3.1.7 on 2021-05-07 03:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20210426_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned', to='course.task'),
        ),
    ]
