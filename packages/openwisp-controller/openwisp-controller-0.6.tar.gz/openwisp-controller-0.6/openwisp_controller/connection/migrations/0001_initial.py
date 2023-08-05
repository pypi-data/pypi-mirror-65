# Generated by Django 2.0.5 on 2018-05-05 17:33

import collections
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
import model_utils.fields
import openwisp_users.mixins
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('config', '0012_auto_20180219_1501'),
        ('openwisp_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(db_index=True, max_length=64, unique=True)),
                ('connector', models.CharField(choices=[('openwisp_controller.connection.connectors.ssh.Ssh', 'SSH')], db_index=True, max_length=128, verbose_name='connection type')),
                ('params', jsonfield.fields.JSONField(default=dict, dump_kwargs={'indent': 4}, help_text='global connection parameters', load_kwargs={'object_pairs_hook': collections.OrderedDict}, verbose_name='parameters')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='openwisp_users.Organization', verbose_name='organization')),
            ],
            options={
                'verbose_name_plural': 'Access credentials',
                'verbose_name': 'Access credentials',
            },
            bases=(openwisp_users.mixins.ValidateOrgMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DeviceConnection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('update_strategy', models.CharField(blank=True, choices=[('openwisp_controller.connection.connectors.openwrt.ssh.OpenWrt', 'OpenWRT SSH')], db_index=True, help_text='leave blank to determine automatically', max_length=128, verbose_name='update strategy')),
                ('enabled', models.BooleanField(db_index=True, default=True)),
                ('params', jsonfield.fields.JSONField(blank=True, default=dict, dump_kwargs={'indent': 4}, help_text='local connection parameters (will override the global parameters if specified)', load_kwargs={'object_pairs_hook': collections.OrderedDict}, verbose_name='parameters')),
                ('is_working', models.NullBooleanField(default=None)),
                ('last_attempt', models.DateTimeField(blank=True, null=True)),
                ('failure_reason', models.CharField(blank=True, max_length=128, verbose_name='reason of failure')),
                ('credentials', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='connection.Credentials')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='config.Device')),
            ],
            options={
                'verbose_name_plural': 'Device connections',
                'verbose_name': 'Device connection',
            },
        )
    ]
