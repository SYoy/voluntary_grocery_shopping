# Generated by Django 3.0.4 on 2020-03-16 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EinkaufsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='group',
            field=models.CharField(choices=[('Helfer', 'H'), ('Empfaenger', 'E'), ('default', 'D')], default='D', max_length=12),
        ),
    ]
