# Generated by Django 5.2 on 2025-04-18 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rename_creatorplayerid_event_creatorplayer'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicPoster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('Image', models.ImageField(upload_to='dynamic_posters/')),
            ],
        ),
    ]
