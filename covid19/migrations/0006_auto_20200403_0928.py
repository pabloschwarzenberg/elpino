# Generated by Django 2.2.5 on 2020-04-03 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0005_contacto_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='link',
            field=models.CharField(max_length=256, null=True),
        ),
    ]