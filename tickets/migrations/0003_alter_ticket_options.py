# Generated by Django 5.1.4 on 2025-01-07 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_problemtype_ticket_problem_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['status', '-created_at']},
        ),
    ]