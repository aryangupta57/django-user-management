# Generated by Django 4.2.2 on 2023-06-13 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.EmailField(db_index=True, max_length=254, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128)),
                ('full_name', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('profile_picture', models.ImageField(upload_to='images/profiles')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
