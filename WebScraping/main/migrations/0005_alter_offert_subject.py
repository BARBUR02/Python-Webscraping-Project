# Generated by Django 4.2 on 2023-04-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_offert_description_offert_link_offert_locations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offert',
            name='subject',
            field=models.CharField(choices=[('Język polski', 'Język polski'), ('Język angielski', 'Język angielski'), ('Matematyka', 'Matematyka'), ('Fizyka', 'Fizyka'), ('Chemia', 'Chemia')], max_length=255),
        ),
    ]