# Generated by Django 2.1 on 2018-09-29 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created at')),
                ('last_updated_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', null=True, verbose_name='Last updated at')),
                ('name', models.CharField(max_length=255, verbose_name='Category name')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(blank=True, default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created at')),
                ('last_updated_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', null=True, verbose_name='Last updated at')),
                ('content', models.TextField(verbose_name='Question content')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ranker.Category', verbose_name='Question category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Creation timestamp', verbose_name='Created at')),
                ('last_updated_at', models.DateTimeField(auto_now=True, help_text='Last update timestamp', null=True, verbose_name='Last updated at')),
                ('hash_id', models.CharField(max_length=255, unique=True, verbose_name='Unique hash')),
                ('stage', models.PositiveIntegerField(default=0, help_text='0 - not started, 1 - first set completed, 2 - second set completed', verbose_name='Completion stage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RankingEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(choices=[('essential', 'Essential'), ('worthwhile', 'Worthwhile'), ('unimportant', 'Unimportant'), ('unwise', 'Unwise'), ('dont_understand', "I don't understand")], max_length=255, verbose_name='Selected rank')),
                ('trial_stage', models.PositiveIntegerField(help_text='Number of round of questions', verbose_name='Trial stage')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ranker.Question', verbose_name='Question')),
                ('ranking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranker.Ranking', verbose_name='Ranking')),
            ],
            options={
                'verbose_name': 'Ranking entry',
                'verbose_name_plural': 'Ranking entries',
            },
        ),
        migrations.AddField(
            model_name='ranking',
            name='entries',
            field=models.ManyToManyField(through='ranker.RankingEntry', to='ranker.Question'),
        ),
        migrations.CreateModel(
            name='QuestionSummary',
            fields=[
            ],
            options={
                'verbose_name': 'Question summary',
                'verbose_name_plural': 'Questions summary',
                'proxy': True,
                'indexes': [],
            },
            bases=('ranker.question',),
        ),
    ]
