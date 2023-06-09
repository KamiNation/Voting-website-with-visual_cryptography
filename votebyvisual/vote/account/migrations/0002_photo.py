# Generated by Django 3.2.16 on 2023-01-19 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(upload_to='images')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
