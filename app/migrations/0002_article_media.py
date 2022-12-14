# Generated by Django 4.0.4 on 2022-05-07 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('date', models.CharField(max_length=50)),
                ('article_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img1', models.ImageField(upload_to='./Templates/media')),
                ('article_id', models.CharField(max_length=100)),
                ('img_count', models.IntegerField()),
            ],
        ),
    ]
