# Generated by Django 5.1.4 on 2024-12-16 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SpotifyToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=512)),
                ('expires_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
