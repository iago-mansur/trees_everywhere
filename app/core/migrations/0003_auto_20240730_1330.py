# Generated by Django 3.2.25 on 2024-07-30 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_tree'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tree',
            name='location',
        ),
        migrations.AddField(
            model_name='tree',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tree',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
            preserve_default=False,
        ),
    ]
