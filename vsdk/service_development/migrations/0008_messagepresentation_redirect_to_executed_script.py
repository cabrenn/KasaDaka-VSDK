# Generated by Django 2.0.4 on 2019-05-23 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_development', '0007_seedoffer_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagepresentation',
            name='redirect_to_executed_script',
            field=models.BooleanField(default=False, verbose_name='If true this element will redirect to the exec. script will post otherwise.'),
        ),
    ]
