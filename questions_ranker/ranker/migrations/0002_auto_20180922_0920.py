# Generated by Django 2.1 on 2018-09-22 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ranker', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rankingentry',
            options={'verbose_name': 'Ranking entry', 'verbose_name_plural': 'Ranking entries'},
        ),
    ]