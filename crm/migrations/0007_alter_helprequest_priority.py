# Generated by Django 5.1.3 on 2025-01-06 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_remove_helprequest_date_requested_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helprequest',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=2),
        ),
    ]
