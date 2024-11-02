# Generated by Django 5.1.2 on 2024-10-31 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.CharField(choices=[('Working on It', 'Working on It'), ('Not Started', 'Not Started'), ('Completed', 'Completed'), ('Need Guidance', 'Need Guidance')], default='Not Started', max_length=50),
        ),
    ]