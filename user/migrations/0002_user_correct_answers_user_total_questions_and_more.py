# Generated by Django 5.1.4 on 2024-12-21 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='correct_answers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='total_questions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='wrong_answers',
            field=models.IntegerField(default=0),
        ),
    ]
