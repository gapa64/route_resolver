# Generated by Django 3.2.10 on 2022-12-13 21:04

from django.db import migrations, models
import prefixes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IPv4prefix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.GenericIPAddressField()),
                ('nexthop', models.GenericIPAddressField()),
                ('metric', models.IntegerField(default=100, validators=[prefixes.validators.metric_validator])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IPv6prefix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.GenericIPAddressField()),
                ('nexthop', models.GenericIPAddressField()),
                ('metric', models.IntegerField(default=100, validators=[prefixes.validators.metric_validator])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='ipv6prefix',
            index=models.Index(fields=['prefix'], name='prefixes_ip_prefix_5bcf15_idx'),
        ),
        migrations.AddIndex(
            model_name='ipv4prefix',
            index=models.Index(fields=['prefix'], name='prefixes_ip_prefix_2fac09_idx'),
        ),
    ]