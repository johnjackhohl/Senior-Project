# Generated by Django 4.2.4 on 2023-10-31 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OverWatch_2', '0003_player_is_defense'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('hero_name', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('map_name', models.CharField(max_length=100)),
                ('map_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sub_Map',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sub_map_name', models.CharField(max_length=100)),
                ('map_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverWatch_2.map')),
            ],
        ),
        migrations.CreateModel(
            name='Sub_Map_Image',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sub_map_image', models.ImageField(upload_to='images/')),
                ('sub_map_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverWatch_2.sub_map')),
            ],
        ),
        migrations.CreateModel(
            name='Map_Image',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('map_image', models.ImageField(upload_to='images/')),
                ('map_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverWatch_2.map')),
            ],
        ),
        migrations.CreateModel(
            name='Hero_Image',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('hero_image', models.ImageField(upload_to='images/')),
                ('hero_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OverWatch_2.hero')),
            ],
        ),
    ]
