# Generated by Django 3.0.4 on 2020-03-16 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EinkaufsApp', '0002_person_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Einkauf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nachricht', models.TextField(max_length=200)),
                ('liste_text', models.TextField(max_length=500)),
                ('budget', models.CharField(default=30, max_length=4)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
