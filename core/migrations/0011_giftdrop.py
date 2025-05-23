# Generated by Django 5.2 on 2025-04-19 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_equipment'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftDrop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Context', models.IntegerField(choices=[(-1, 'None '), (0, 'Default'), (1, 'Daily Login'), (2, 'Game Drop'), (3, 'Daily Challenges Complete'), (4, 'Weekly Challenge Complete'), (10, 'Unassigned Equipment'), (11, 'Unassigned Avatar'), (100, 'Levelup'), (102, 'Levelup 2'), (103, 'Levelup 3'), (104, 'Levelup 4'), (105, 'Levelup 5'), (106, 'Levelup 6'), (107, 'Levelup 7'), (108, 'Levelup 8'), (109, 'Levelup 9'), (110, 'Levelup 10'), (111, 'Levelup 11'), (112, 'Levelup 12'), (113, 'Levelup 13'), (114, 'Levelup 14'), (115, 'Levelup 15'), (116, 'Levelup 16'), (117, 'Levelup 17'), (118, 'Levelup 18'), (119, 'Levelup 19'), (120, 'Levelup 20'), (121, 'Levelup 21'), (122, 'Levelup 22'), (123, 'Levelup 23'), (124, 'Levelup 24'), (125, 'Levelup 25'), (126, 'Levelup 26'), (127, 'Levelup 27'), (128, 'Levelup 28'), (129, 'Levelup 29'), (130, 'Levelup 30'), (1000, 'Event Rawdata'), (1001, 'Sfvrcc Promo'), (1002, 'Helixxvr Promo'), (2000, 'Paintball Clearcut'), (2001, 'Paintball Homestead'), (2002, 'Paintball Quarry'), (2003, 'Paintball River'), (2004, 'Paintball Dam'), (3000, 'Discgolf Propulsion'), (3001, 'Discgolf Lake'), (3500, 'Discgolf Mode Coopcatch'), (4000, 'Quest Goblin A'), (4001, 'Quest Goblin B'), (4002, 'Quest Goblin C'), (4003, 'Quest Goblin S'), (4010, 'Quest Cauldron A'), (4011, 'Quest Cauldron B'), (4012, 'Quest Cauldron C'), (4013, 'Quest Cauldron S'), (4500, 'Quest Scifi A'), (4501, 'Quest Scifi B'), (4502, 'Quest Scifi C'), (4503, 'Quest Scifi S'), (5000, 'Charades'), (6000, 'Soccer'), (7000, 'Paddleball'), (8000, 'Dodgeball')], default=-1)),
                ('Rarity', models.IntegerField(choices=[(-1, 'None '), (0, 'Common'), (10, 'Uncommon'), (20, 'Rare'), (30, 'Epic'), (50, 'Legendary')], default=0)),
                ('Xp', models.IntegerField(default=0)),
                ('Equipment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.equipment')),
            ],
        ),
    ]
