# Generated by Django 3.2.3 on 2023-07-08 11:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('backend', '0003_auto_20230705_1642'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='time',
            new_name='end',
        ),
        migrations.RemoveField(
            model_name='trace',
            name='end',
        ),
        migrations.RemoveField(
            model_name='trace',
            name='start',
        ),
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=32, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='start',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='channel',
            name='path',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='corporation',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='x',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='y',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='z',
            field=models.FloatField(null=True),
        ),
    ]
