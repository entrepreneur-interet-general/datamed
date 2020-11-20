# Generated by Django 3.1.3 on 2020-11-19 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='ComponentRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosage', models.CharField(max_length=512)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bdpm.component')),
            ],
        ),
        migrations.CreateModel(
            name='CompositionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='GenericGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='Presentations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2048)),
                ('cip_7', models.IntegerField()),
                ('cip_13', models.IntegerField()),
                ('marketing_start_date', models.DateField()),
                ('marketing_stop_date', models.DateField()),
                ('price', models.IntegerField()),
                ('refund_rate', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('bdpm_id', models.IntegerField()),
                ('cis_code', models.IntegerField()),
                ('authorization_holder', models.CharField(max_length=512)),
                ('composition_quantity', models.CharField(max_length=1024)),
                ('composition_components', models.ManyToManyField(through='bdpm.ComponentRelation', to='bdpm.Component')),
                ('composition_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bdpm.compositiontype')),
            ],
        ),
        migrations.CreateModel(
            name='SMR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abstract', models.CharField(max_length=2048)),
                ('advice', models.CharField(max_length=2048)),
                ('reason', models.CharField(max_length=2048)),
                ('value', models.CharField(max_length=2048)),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdpm.specialty')),
            ],
        ),
        migrations.AddField(
            model_name='componentrelation',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdpm.specialty'),
        ),
        migrations.CreateModel(
            name='ASMR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abstract', models.CharField(max_length=2048)),
                ('advice', models.CharField(max_length=2048)),
                ('reason', models.CharField(max_length=2048)),
                ('value', models.CharField(max_length=2048)),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdpm.specialty')),
            ],
        ),
    ]
