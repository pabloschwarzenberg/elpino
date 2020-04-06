# Generated by Django 2.2.5 on 2020-04-06 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0011_auto_20200405_2044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estadistica',
            old_name='casos_Chile',
            new_name='confirmados_Hospital',
        ),
        migrations.RenameField(
            model_name='estadistica',
            old_name='hospital_T1',
            new_name='hospital_BASICA',
        ),
        migrations.RenameField(
            model_name='estadistica',
            old_name='hospital_T2',
            new_name='hospital_TOTAL',
        ),
        migrations.RenameField(
            model_name='estadistica',
            old_name='hospital_T3',
            new_name='hospital_UPC',
        ),
        migrations.RenameField(
            model_name='estadistica',
            old_name='hospital_T4',
            new_name='hospital_VMI',
        ),
        migrations.AddField(
            model_name='estadistica',
            name='contagios_Chile',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='estadistica',
            name='examenes_Hospital',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]