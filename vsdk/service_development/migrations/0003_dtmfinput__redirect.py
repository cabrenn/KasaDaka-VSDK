# Generated by Django 2.0.4 on 2019-05-21 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service_development', '0002_dtmfinput'),
    ]

    operations = [
        migrations.AddField(
            model_name='dtmfinput',
            name='_redirect',
            field=models.ForeignKey(blank=True, help_text='The element to redirect to after the DTMF has been validated', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_development_dtmfinput_related', to='service_development.VoiceServiceElement', verbose_name='Redirect element'),
        ),
    ]