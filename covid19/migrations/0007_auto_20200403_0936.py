# Generated by Django 2.2.5 on 2020-04-03 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0006_auto_20200403_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='link',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
